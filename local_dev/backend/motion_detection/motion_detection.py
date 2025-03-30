import cv2
import numpy as np
from ultralytics import YOLO
import sys
import os
import time
import pygame
import threading

# Add parent directory to sys.path to import game utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game import countdown, red_light_green_light_loop, get_player_names

def play_sound(audio_file):
    sound1 = pygame.mixer.Sound(audio_file)
    channel = sound1.play()
    


class MotionDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("yolov8n-pose.pt")
        self.movement_threshold = 100.0
        self.red_light = False
        self.players = {}         # Store player names
        self.eliminated = set()   # Track eliminated players
        pygame.mixer.init()
        # Attributes for continuous baseline detection
        self.baseline_captured = False
        self.baseline_centers = {}

    def get_pose_estimation(self, frame):
        results = self.model(frame, verbose=False)
        return results

    def extract_keypoints(self, results):
        if results[0].keypoints is not None:
            keypoints = (
                results[0].keypoints.data
                if hasattr(results[0].keypoints, "data")
                else results[0].keypoints
            )
            if hasattr(keypoints, "cpu"):
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

    def draw_keypoints(self, results):
        """Display the annotated frame with keypoints overlay."""
        annotated_frame = results[0].plot()
        cv2.imshow("Red Light, Green Light", annotated_frame)
        cv2.waitKey(1)

    def set_green(self):
        self.red_light = False
        print("Green Light")

    def set_red(self, red_duration):
        self.red_light = True
        self.baseline_captured = False  # Ensure new baseline is captured
        print("Red Light")
        time.sleep(red_duration)
        self.red_light = False

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

        # Start the game with a countdown that plays an audio file
        countdown()

        # Start red light green light loop in a daemon thread
        game_thread = threading.Thread(
            target=red_light_green_light_loop,
            args=(60, self.set_green, self.set_red, self.players)
        )
        game_thread.daemon = True
        game_thread.start()

        try:
            # Continuous frame capture loop regardless of light state
            while game_thread.is_alive():
                ret, frame = self.cap.read()
                if not ret:
                    continue

                results = self.get_pose_estimation(frame)
                self.draw_keypoints(results)

                if self.red_light:
                    # On red light: capture baseline positions if not yet captured
                    if not self.baseline_captured:
                        self.baseline_centers = {}
                        keypoints = self.extract_keypoints(results)
                        if keypoints is not None:
                            for i, person in enumerate(keypoints):
                                if i in self.eliminated:
                                    continue
                                valid_kp = self.filter_valid_keypoints(person)
                                center = self.compute_center(person, valid_kp)
                                self.baseline_centers[i] = center
                        self.baseline_captured = True
                    else:
                        # Compare current positions against the baseline
                        keypoints = self.extract_keypoints(results)
                        if keypoints is not None:
                            for i, person in enumerate(keypoints):
                                if i in self.eliminated:
                                    continue
                                valid_kp = self.filter_valid_keypoints(person)
                                center = self.compute_center(person, valid_kp)
                                if i in self.baseline_centers:
                                    movement = np.linalg.norm(center - self.baseline_centers[i])
                                    if movement > self.movement_threshold:
                                        player_name = self.players.get(i, f"Player {i+1}")
                                        print(f"❌ {player_name} MOVED during RED LIGHT! ({movement:.2f} pixels)")
                                        self.eliminated.add(i)
                                        play_sound('eliminated.mp3')
                else:
                    # Reset the baseline once green light returns
                    self.baseline_captured = False

                # Check if all players have been eliminated
                if len(self.eliminated) == len(self.players):
                    print("\n🚨 All players eliminated! Game Over!")
                    play_sound('game_end.mp3')
                    break

                cv2.waitKey(1)
        except KeyboardInterrupt:
            print("Game cancelled by user.")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    detector = MotionDetector()
    detector.run()
