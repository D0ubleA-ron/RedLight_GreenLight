import cv2
import numpy as np
from ultralytics import YOLO
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game import countdown, red_light_green_light_loop, get_player_names

class MotionDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("yolov8n-pose.pt")
        self.movement_threshold =10.0
        self.prev_centers = {}
        self.red_light = False
        self.players = {}  # Store player names
        self.eliminated = set()  # Track eliminated players

    def get_pose_estimation(self, frame):
        results = self.model(frame, verbose=False)
        return results

    def extract_keypoints(self, results):
        if results[0].keypoints is not None:
            keypoints = results[0].keypoints.data if hasattr(results[0].keypoints, 'data') else results[0].keypoints
            if hasattr(keypoints, 'cpu'):
                keypoints = keypoints.cpu().numpy()
            return keypoints
        return None

    def filter_valid_keypoints(self, person, conf_threshold=0.5):
        return [kp for kp in person if kp[2] > conf_threshold]

    def compute_center(self, person, valid_keypoints):
        if valid_keypoints:
            valid_keypoints = np.array(valid_keypoints)
            center = np.mean(valid_keypoints[:, :2], axis=0)
        else:
            center = np.mean(person[:, :2], axis=0)
        return center

    def process_keypoints(self, results, players):
        keypoints = self.extract_keypoints(results)
        if keypoints is None:
            return {}, set()

        current_centers = {}
        eliminated_this_round = set()

        for i, person in enumerate(keypoints):
            if i in self.eliminated:  # Skip eliminated players
                continue

            valid_kp = self.filter_valid_keypoints(person)
            center = self.compute_center(person, valid_kp)
            current_centers[i] = center

            if self.red_light and i in self.prev_centers:
                movement = np.linalg.norm(center - self.prev_centers[i])
                print(movement)
                if movement > self.movement_threshold:
                    player_name = players.get(i, f"Player {i+1}")
                    print(f"❌ {player_name} MOVED during RED LIGHT! ({movement:.2f} pixels)")
                    eliminated_this_round.add(i)

        self.prev_centers = current_centers
        return current_centers, eliminated_this_round

    def draw_keypoints(self, results):
        annotated_frame = results[0].plot()
        cv2.imshow("Red Light, Green Light", annotated_frame)
        cv2.waitKey(1)

    def on_green(self):
        self.red_light = False
    
    def on_red(self, players, red_duration):
        self.red_light = True

        # Capture baseline positions immediately when red light starts.
        ret, frame = self.cap.read()
        if not ret:
            return set()
        results = self.get_pose_estimation(frame)
        baseline_centers = {}
        keypoints = self.extract_keypoints(results)
        if keypoints is not None:
            for i, person in enumerate(keypoints):
                if i in self.eliminated:
                    continue
                valid_kp = self.filter_valid_keypoints(person)
                center = self.compute_center(person, valid_kp)
                baseline_centers[i] = center

        eliminated_this_round = set()
        start_time = time.time()

        # Continuously capture frames during the red light period.
        while time.time() - start_time < red_duration:
            ret, frame = self.cap.read()
            if not ret:
                continue

            results = self.get_pose_estimation(frame)
            keypoints = self.extract_keypoints(results)
            if keypoints is not None:
                for i, person in enumerate(keypoints):
                    if i in self.eliminated:
                        continue
                    valid_kp = self.filter_valid_keypoints(person)
                    center = self.compute_center(person, valid_kp)
                    if i in baseline_centers:
                        movement = np.linalg.norm(center - baseline_centers[i])
                        if movement > self.movement_threshold:
                            player_name = players.get(i, f"Player {i+1}")
                            print(f"❌ {player_name} MOVED during RED LIGHT! ({movement:.2f} pixels)")
                            eliminated_this_round.add(i)
            time.sleep(0.1)  # Check approximately every 0.1 seconds

        self.eliminated.update(eliminated_this_round)
        return eliminated_this_round




    def run(self):
        print("\nDetecting number of players...")
        ret, frame = self.cap.read()
        if not ret:
            print("❌ Camera not available")
            return

        results = self.get_pose_estimation(frame)
        keypoints = self.extract_keypoints(results)
        num_players = len(keypoints) if keypoints is not None else 1
        print(f"\nDetected {num_players} players.")

        # Get player names
        self.players = get_player_names(num_players)

        # Start the game
        countdown()
        red_light_green_light_loop(
            duration=60,
            on_green=self.on_green,
            on_red=self.on_red,
            players=self.players
        )

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    detector = MotionDetector()
    detector.run()
