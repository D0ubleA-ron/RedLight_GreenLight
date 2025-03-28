import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2

# Function to get pose estimation from the model
def get_pose_estimation(frame, model):
    results = model(frame, verbose=False)
    return results

# Function to extract keypoints from the results
def extract_keypoints(results):
    if results[0].keypoints is not None:
        keypoints = results[0].keypoints.data if hasattr(results[0].keypoints, 'data') else results[0].keypoints
        if hasattr(keypoints, 'cpu'):
            keypoints = keypoints.cpu().numpy()
        return keypoints
    return None

# Function to filter valid keypoints
def filter_valid_keypoints(person, conf_threshold=0.5):
    return [kp for kp in person if kp[2] > conf_threshold]

# Function to compute center of the person
def compute_center(person, valid_keypoints):
    if valid_keypoints:
        valid_keypoints = np.array(valid_keypoints)
        center = np.mean(valid_keypoints[:, :2], axis=0)
    else:
        center = np.mean(person[:, :2], axis=0)
    return center

# Function to compare movement of the person
def compare_movement(i, center, prev_centers, movement_threshold):
    if i in prev_centers:
        movement = np.linalg.norm(center - prev_centers[i])
        if movement > movement_threshold:
            print(f"Person {i} has moved {movement:.2f} pixels")
        else:
            print(f"Person {i} movement insignificant: {movement:.2f} pixels")
    else:
        print(f"Person {i} detected for the first time.")

# Function to process keypoints
def process_keypoints(results, prev_centers, movement_threshold):
    current_centers = {}
    keypoints = extract_keypoints(results)
    if keypoints is None:
        return current_centers

    for i, person in enumerate(keypoints):
        valid_keypoints = filter_valid_keypoints(person)
        center = compute_center(person, valid_keypoints)
        current_centers[i] = center
        print(f"Person {i} center at: {center}")
        compare_movement(i, center, prev_centers, movement_threshold)
    
    return current_centers

# Function to process bounding boxes
def process_boxes(results):
    if hasattr(results[0], 'boxes') and results[0].boxes is not None:
        boxes = (results[0].boxes.xyxy.data 
                 if hasattr(results[0].boxes.xyxy, 'data') 
                 else results[0].boxes.xyxy)
        if hasattr(boxes, 'cpu'):
            boxes = boxes.cpu().numpy()
        for i, box in enumerate(boxes):
            print(f"Person {i} bounding box: {box.tolist()}")

# Function to initialize the tracker        
def initialize_tracker():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()
    model = YOLO("yolov8n-pose.pt")
    movement_threshold = 60.0
    prev_centers = {}
    return picam2, model, movement_threshold, prev_centers

# Function to end the tracker
def end_tracker(picam2):
    picam2.stop()
    cv2.destroyAllWindows()

# Function to draw keypoints
def draw_keypoints(results):
    annotated_frame = results[0].plot()
    cv2.imshow('YOLOv8 Pose Detection', annotated_frame)

def run():
    picam2, model, movement_threshold, prev_centers = initialize_tracker()
    while True:
        # Capture a frame using picamera2
        frame = picam2.capture_array()

        # Convert the frame from 4 channels (RGBA) to 3 channels (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        # Perform pose estimation
        results = get_pose_estimation(frame, model)
        draw_keypoints(results)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Process keypoints and bounding boxes
        current_centers = process_keypoints(results, prev_centers, movement_threshold)
        process_boxes(results)
        prev_centers = current_centers

    end_tracker(picam2)

if __name__ == '__main__':
    run()