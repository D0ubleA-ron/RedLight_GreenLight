import cv2
import numpy as np
import time
import random
import os
import threading
from playsound import playsound

AUDIO_DIR = "Audio Files"

class RedLightGreenLightGame:
    def __init__(self, cap, model, player_names, movement_threshold=10.0):
        self.cap = cap
        self.model = model
        self.movement_threshold = movement_threshold
        self.prev_centers = {}  # {player_name: center}
        self.player_names = player_names  # List of names
        self.player_status = {name: "alive" for name in player_names}
        self.player_ids = {}  # YOLO ID → player_name (based on matching)
        self.state = "Green"
        self.red_duration = 3
        self.green_duration = 3
        self.last_switch = time.time()
        self.red_audio_thread = None
        self.playing_red_audio = False

    def play_audio(self, filename):
        path = os.path.join(AUDIO_DIR, filename)
        if os.path.exists(path):
            playsound(path, block=True)

    def play_loop_audio(self, filename):
        path = os.path.join(AUDIO_DIR, filename)
        while self.playing_red_audio:
            playsound(path, block=True)

    def start_red_audio(self):
        self.playing_red_audio = True
        self.red_audio_thread = threading.Thread(target=self.play_loop_audio, args=("redlight_countdown.mp3",), daemon=True)
        self.red_audio_thread.start()

    def stop_red_audio(self):
        self.playing_red_audio = False
        if self.red_audio_thread is not None:
            self.red_audio_thread.join()

    def switch_light(self):
        now = time.time()
        if self.state == "Green" and now - self.last_switch > self.green_duration:
            self.state = "Red"
            self.last_switch = now
            print("\nRED LIGHT! DO NOT MOVE!")
            self.start_red_audio()
        elif self.state == "Red" and now - self.last_switch > self.red_duration:
            self.state = "Green"
            self.last_switch = now
            print("\nGREEN LIGHT! YOU CAN MOVE!")
            self.stop_red_audio()

    def match_players(self, centers):
        matched = {}
        used = set()

        for name in self.player_names:
            if self.player_status[name] == "out":
                continue
            prev = self.prev_centers.get(name)
            if prev is None:
                for pid, center in centers.items():
                    if pid not in used:
                        matched[pid] = name
                        used.add(pid)
                        break
            else:
                best_pid = None
                best_dist = float("inf")
                for pid, center in centers.items():
                    if pid in used:
                        continue
                    dist = np.linalg.norm(center - prev)
                    if dist < best_dist:
                        best_dist = dist
                        best_pid = pid
                if best_pid is not None:
                    matched[best_pid] = name
                    used.add(best_pid)

        return matched

    def update_players(self, centers):
        matched = self.match_players(centers)

        for pid, name in matched.items():
            if self.player_status[name] == "out":
                continue

            center = centers[pid]
            prev_center = self.prev_centers.get(name)

            if prev_center is not None:
                movement = np.linalg.norm(center - prev_center)
                if self.state == "Red" and movement > self.movement_threshold:
                    self.player_status[name] = "out"
                    print(f"{name} moved during RED LIGHT and is ELIMINATED! (Movement: {movement:.2f})")
                    self.play_audio("eliminated.mp3")
                elif self.state == "Green":
                    print(f"{name} is moving freely. (Movement: {movement:.2f})")
            else:
                print(f"{name} is standing still.")

            self.prev_centers[name] = center

    def is_game_over(self):
        alive = [s for s in self.player_status.values() if s == "alive"]
        return len(alive) <= 1 and len(self.player_status) > 0

    def print_winner(self):
        for name, status in self.player_status.items():
            if status == "alive":
                print(f"\n{name} is the WINNER!")
                self.play_audio("game_end.mp3")
                return
        print("\nNo winners. Everyone got eliminated.")
        self.play_audio("game_end.mp3")

    def run(self):
        print("Game Started: Red Light, Green Light!\n")
        self.play_audio("game_start_countdown.mp3")
        print("GREEN LIGHT! YOU CAN MOVE!")

        red_green_cycles = 0
        force_min_cycles = len(self.player_names) == 1

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame.")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model(frame, verbose=False)
            keypoints = results[0].keypoints
            if keypoints is None:
                continue

            keypoints = keypoints.data.cpu().numpy()
            centers = {}
            for i, person in enumerate(keypoints):
                valid = person[person[:, 2] > 0.5] if person.ndim == 2 else person
                center = np.mean(valid[:, :2], axis=0) if len(valid) > 0 else None
                if center is not None:
                    centers[i] = center

            prev_state = self.state
            self.switch_light()

            if prev_state == "Red" and self.state == "Green":
                red_green_cycles += 1

            self.update_players(centers)

            if force_min_cycles:
                if red_green_cycles >= 2:
                    break
            else:
                if self.is_game_over():
                    break

        self.stop_red_audio()
        self.print_winner()
        self.cap.release()
        cv2.destroyAllWindows()
