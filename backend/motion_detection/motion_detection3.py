import cv2
import numpy as np
from ultralytics import YOLO

# Initialize webcam
cap = cv2.VideoCapture(0)
# Load YOLO model for pose detection
model = YOLO("yolov8n-pose.pt")

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Process the frame with YOLO
    results = model(frame, verbose=False)
    
    # Visualize the results on the frame
    annotated_frame = results[0].plot()
    
    # Display the annotated frame
    cv2.imshow('YOLOv8 Pose Detection', annotated_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
