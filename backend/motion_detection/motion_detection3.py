import cv2
import numpy as np
from ultralytics import YOLO

# Initialize webcam
cap = cv2.VideoCapture(0)

# Load YOLO model for pose detection
model = YOLO("yolov8n-pose.pt")

# Dictionary to store previous center positions for each person
prev_centers = {}
# Set a movement threshold in pixels (you can adjust this value)
movement_threshold = 10.0

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
    
    # Dictionary to store current centers
    current_centers = {}
    
    # Print coordinates for each detected person and detect movement
    if results[0].keypoints is not None:
        # Get keypoints; use .data if available and convert to NumPy array if needed
        keypoints = results[0].keypoints.data if hasattr(results[0].keypoints, 'data') else results[0].keypoints
        if hasattr(keypoints, 'cpu'):
            keypoints = keypoints.cpu().numpy()
        
        # Iterate over each detected person
        for i, person in enumerate(keypoints):
            # Optionally, filter keypoints based on confidence (here we use 0.5 as threshold)
            valid_keypoints = [kp for kp in person if kp[2] > 0.5]
            if valid_keypoints:
                valid_keypoints = np.array(valid_keypoints)
                # Compute the center from valid keypoints
                center = np.mean(valid_keypoints[:, :2], axis=0)
            else:
                # Fallback: use all keypoints if none pass the confidence threshold
                center = np.mean(person[:, :2], axis=0)
            
            current_centers[i] = center
            print(f"Person {i} center at: {center}")
            
            # If we have a previous center for this person, check movement
            if i in prev_centers:
                # Calculate Euclidean distance between current and previous center
                movement = np.linalg.norm(center - prev_centers[i])
                if movement > movement_threshold:
                    print(f"Person {i} has moved {movement:.2f} pixels")
                else:
                    print(f"Person {i} movement insignificant: {movement:.2f} pixels")
            else:
                print(f"Person {i} detected for the first time.")
    
    # Update previous centers for next frame
    prev_centers = current_centers
    
    # Optionally, print bounding boxes if available
    if hasattr(results[0], 'boxes') and results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.data if hasattr(results[0].boxes.xyxy, 'data') else results[0].boxes.xyxy
        if hasattr(boxes, 'cpu'):
            boxes = boxes.cpu().numpy()
        for i, box in enumerate(boxes):
            print(f"Person {i} bounding box: {box.tolist()}")
    
    # Display the annotated frame
    cv2.imshow('YOLOv8 Pose Detection', annotated_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
