
import cv2
from ultralytics import YOLO
from game_sequence import RedLightGreenLightGame

def main():
    cap = cv2.VideoCapture("http://10.0.0.34:5000/video")  # Update with your webcam stream URL
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam stream.")

    model = YOLO("yolov8n-pose.pt")
    game = RedLightGreenLightGame(cap, model, player_names=player_names)
    game.run()

if __name__ == "__main__":
    main()
