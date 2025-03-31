import cv2
import numpy as np
import time
import os
import threading
import random
import pygame

AUDIO_DIR = "audio_clips"

class RedLightGreenLightGame:
    def __init__(self, cap, model, movement_threshold=10.0):
        self.cap = cap
        self.model = model
        self.movement_threshold = movement_threshold
        self.prev_centers = {}
        self.player_names = []
        self.player_status = {}
        self.player_embeddings = {}  # name → pose embedding
        self.state = "Green"
        self.red_duration = 3
        self.green_duration = 3
        self.last_switch = time.time()
        self.red_audio_thread = None
        self.playing_red_audio = False
        self.pose_id_to_name = {}      # YOLO ID → name
        self.name_to_pose_id = {}      # name → YOLO ID
        self.pose_disappear_counter = {}  # track lost detections
        self.max_disappear_frames = 5  # allow some dropout before breaking match


        pygame.mixer.init()

    def play_audio(self, filename):
        try:
            full_path = os.path.join(AUDIO_DIR, filename)
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
            print(f"[Audio] Playing {filename}")
        except Exception as e:
            print(f"[Audio Error] Could not play {filename}: {e}")

    def play_loop_audio(self, filename):
        while self.playing_red_audio:
            self.play_audio(filename)
            time.sleep(3)

    def start_red_audio(self):
        self.playing_red_audio = True
        self.red_audio_thread = threading.Thread(target=self.play_loop_audio, args=("redlight_countdown.mp3",), daemon=True)
        self.red_audio_thread.start()

    def stop_red_audio(self):
        self.playing_red_audio = False
        if self.red_audio_thread is not None:
            self.red_audio_thread.join()

    def detect_pose_embedding(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model(frame_rgb, verbose=False)
            keypoints = results[0].keypoints
            if keypoints is None:
                continue
            keypoints = keypoints.data.cpu().numpy()
            if len(keypoints) > 0:
                # Use first detected person
                valid = keypoints[0][keypoints[0][:, 2] > 0.5]
                if len(valid) > 0:
                    embedding = np.mean(valid[:, :2], axis=0)
                    return embedding

    def register_players(self):
        print("🎮 Starting player registration...")
        print("Each player, when prompted, please step close to the camera and enter your name.")

        num_players = int(input("How many players will be playing? "))

        for i in range(num_players):
            input(f"\nPlayer {i+1}, press Enter and come close to the camera...")
            name = input("Enter your name: ")
            print("Capturing your pose... Please stand still.")
            embedding = self.detect_pose_embedding()
            self.player_names.append(name)
            self.player_status[name] = "alive"
            self.player_embeddings[name] = embedding
            print(f"✅ Registered {name}!")

    def match_players(self, current_embeddings):
        matched = {}
        used_names = set()

        for pid, embedding in current_embeddings.items():
            # Check if this PID was seen before and mapped
            if pid in self.pose_id_to_name:
                name = self.pose_id_to_name[pid]
                matched[pid] = name
                self.pose_disappear_counter[name] = 0
                used_names.add(name)
            else:
                # New or mismatched — try to match
                best_match = None
                best_dist = float("inf")
                for name, stored_embedding in self.player_embeddings.items():
                    if name in used_names:
                        continue
                    dist = np.linalg.norm(embedding - stored_embedding)
                    if dist < best_dist:
                        best_dist = dist
                        best_match = name

                if best_match and best_dist < 50:  # tighter threshold
                        matched[pid] = best_match
                        self.pose_id_to_name[pid] = best_match
                        self.name_to_pose_id[best_match] = pid
                        self.pose_disappear_counter[best_match] = 0
                        used_names.add(best_match)

        # Handle disappeared poses
        for name in self.player_names:
            if name not in used_names:
                if name in self.pose_disappear_counter:
                    self.pose_disappear_counter[name] += 1
                    if self.pose_disappear_counter[name] >= self.max_disappear_frames:
                        # Reset mappings
                        pid = self.name_to_pose_id.get(name)
                        if pid in self.pose_id_to_name:
                            del self.pose_id_to_name[pid]
                        if name in self.name_to_pose_id:
                            del self.name_to_pose_id[name]
                else:
                    self.pose_disappear_counter[name] = 1

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
                    print(f"❌ {name} moved during RED LIGHT and is ELIMINATED! (Movement: {movement:.2f})")
                    self.play_audio("eliminated.mp3")
                elif self.state == "Green":
                    print(f"✅ {name} is moving freely. (Movement: {movement:.2f})")
            else:
                print(f"{name} is standing still.")

            self.prev_centers[name] = center

    def switch_light(self):
        now = time.time()
        if self.state == "Green" and now - self.last_switch > self.green_duration:
            self.state = "Red"
            self.last_switch = now
            self.red_duration = random.randint(10, 15)
            print(f"\n🔴 RED LIGHT for {self.red_duration} seconds! DO NOT MOVE!")
            self.start_red_audio()
        elif self.state == "Red" and now - self.last_switch > self.red_duration:
            self.state = "Green"
            self.last_switch = now
            self.green_duration = random.randint(10, 15)
            print(f"\n🟢 GREEN LIGHT for {self.green_duration} seconds! YOU CAN MOVE!")
            self.stop_red_audio()

    def is_game_over(self):
        alive = [s for s in self.player_status.values() if s == "alive"]
        return len(alive) <= 1 and len(self.player_status) > 0

    def print_winner(self):
        for name, status in self.player_status.items():
            if status == "alive":
                print(f"\n🏆 {name} is the WINNER!")
                self.play_audio("game_end.mp3")
                return
        print("\n😢 No winners. Everyone got eliminated.")
        self.play_audio("game_end.mp3")

    def run(self):
        self.register_players()

        print("\nGet ready to play!")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        solo_mode = len(self.player_names) == 1
        red_green_cycles = 0

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

            if solo_mode:
                if red_green_cycles >= 3 or self.is_game_over():
                    break
            else:
                if self.is_game_over():
                    break

        self.stop_red_audio()
        self.print_winner()
        self.cap.release()
        cv2.destroyAllWindows()
