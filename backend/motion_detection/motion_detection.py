import cv2
print(cv2.__version__)


tracker = cv2.legacy.TrackerKCF_create()
    
# Initialize the HOG person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Open video capture (0 for default webcam, or replace with video file path)
cap = cv2.VideoCapture(0)

tracker_initialized = False
tracker = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if not tracker_initialized:
        # Detect people in the frame
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
        if len(boxes) > 0:
            # For simplicity, pick the first detected person
            bbox = boxes[0]
            # Initialize the tracker (KCF in this case)
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, tuple(bbox))
            tracker_initialized = True
    else:
        # Update tracker and get updated position
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            # If tracking fails, reinitialize detection
            tracker_initialized = False

    # Display the frame with the tracking rectangle
    cv2.imshow("Person Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()