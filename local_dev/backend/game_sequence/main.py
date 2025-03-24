import cv2
from ultralytics import YOLO
from game_sequence import RedLightGreenLightGame

def get_player_names(max_players=5):
    print("🎮 Enter up to 5 player names. Press Enter to skip a slot.")
    names = []
    for i in range(1, max_players + 1):
        name = input(f"Player {i} name: ").strip()
        if name == "":
            continue
        names.append(name)
    if not names:
        print("❗️At least 1 player is required.")
        exit(1)
    return names

def main():
    cap = cv2.VideoCapture("http://10.0.0.34:5000/video")  # Update with your webcam stream URL
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam stream.")

    model = YOLO("yolov8n-pose.pt")
    player_names = get_player_names()
    game = RedLightGreenLightGame(cap, model, player_names=player_names)
    game.run()

if __name__ == "__main__":
    main()
