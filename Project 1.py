import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from ultralytics import YOLO

# Function to load colour names and RGB values from CSV
def load_colour_data():
    colour_data = pd.read_csv('colors.csv')
    names = colour_data.iloc[:, 0].values
    rgb_values = colour_data.iloc[:, 2:5].values
    return rgb_values, names

def main():
    # Load the colour data
    rgb_values, colour_names = load_colour_data()

    # Create the KNN classifier and train it
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(rgb_values, colour_names)

    # Load the YOLOv8 model
    model = YOLO("yolov8n.pt")

    # Start the webcam
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break  # Stop if webcam doesn't return a frame

        # Detect objects using YOLO
        results = model(frame, verbose=False)[0]

        # Draw YOLO detection boxes and labels
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            label = model.names[class_id]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Get the colour at the centre of the frame
        height, width = frame.shape[:2]
        centre_x = width // 2
        centre_y = height // 2
        pixel = frame[centre_y, centre_x]
        blue, green, red = int(pixel[0]), int(pixel[1]), int(pixel[2])

        # Predict the name of the colour using KNN
        input_colour = np.array([[red, green, blue]])
        predicted_name = knn.predict(input_colour)[0]

        # Create a colour mask around the detected colour (±20 range)
        lower_bound = np.array([max(blue - 20, 0), max(green - 20, 0), max(red - 20, 0)], dtype=np.uint8)
        upper_bound = np.array([min(blue + 20, 255), min(green + 20, 255), min(red + 20, 255)], dtype=np.uint8)
        mask = cv2.inRange(frame, lower_bound, upper_bound)

        # If no matching pixels are found, skip drawing
        if cv2.countNonZero(mask) == 0:
            cv2.putText(frame, "No colour detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('Colour Detector', frame)
            continue

        # Find contours of the masked colour area
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            # Only draw if it's a decent-sized area
            if cv2.contourArea(largest_contour) > 500:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, predicted_name, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"RGB: {red},{green},{blue}", (x, y + h + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Show the final frame
        cv2.imshow('Colour Detector', frame)

        # Exit the loop if ESC is pressed
        if cv2.waitKey(1) == 27:
            break

    # Clean up
    camera.release()
    cv2.destroyAllWindows()

main()
