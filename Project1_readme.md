# Real-time Object & Color Detection System  


**A computer vision project combining YOLOv8 object detection with KNN color classification**  

As a graduate Robotics Engineer passionate about perception systems, I developed this application to demonstrate real-time object detection with precise color identification. The system uses a webcam feed to detect objects (via YOLOv8) while simultaneously classifying colors at the frame's center point (using KNN trained on RGB values).


## Key Features  
- **Dual Detection Pipeline**:  
  - Object detection with pre-trained YOLOv8n (80 COCO classes)  
  - Color classification using K-Nearest Neighbors (trained on 865 color names)  

- **Interactive Visualization**:  
  - Bounding boxes for detected objects with labels  
  - Dynamic color recognition with ±20 RGB tolerance range  
  - Contour detection for dominant color regions  

- **Modular Architecture**:  
  - Separates color data loading (CSV) from ML inference  
  - Configurable KNN parameters for color matching  


## Tech Stack  
- **Computer Vision**: OpenCV  
- **Object Detection**: Ultralytics YOLOv8  
- **Machine Learning**: scikit-learn KNN  
- **Data Handling**: pandas, numpy  


## Usage  
1. Install dependencies:  
   ```bash
   pip install opencv-python numpy pandas scikit-learn ultralytics