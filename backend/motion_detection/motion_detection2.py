import cv2
import imutils
import numpy as np

# Initialize the HOG descriptor/person detector
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect(frame):
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)
    person = 1
    
    # Set a confidence threshold (higher value = less sensitive)
    confidence_threshold = 0.7
    
    # Create lists to store filtered detections
    filtered_boxes = []
    filtered_weights = []
    
    # Filter detections based on confidence
    for i, (x, y, w, h) in enumerate(bounding_box_cordinates):
        if weights[i] > confidence_threshold:
            filtered_boxes.append((x, y, w, h))
            filtered_weights.append(weights[i])
    
    # Draw only high-confidence detections
    for (x, y, w, h) in filtered_boxes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.imshow('output', frame)
    
    return frame

def detectByCamera():
    video = cv2.VideoCapture(1)
    print('Detecting people...')
    
    while True:
        check, frame = video.read()
        if check:
            frame = imutils.resize(frame, width=min(800, frame.shape[1]))
            frame = detect(frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        else:
            print("Failed to capture video from camera")
            break
    
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print('[INFO] Opening Web Cam.')
    detectByCamera()
