import time
import random

def get_player_names(num_players):
    players = {}
    print("\nEnter player names:")
    for i in range(num_players):
        name = input(f"Player {i+1} Name: ")
        players[i] = name
    return players

def countdown(seconds=5):
    print("Game starting in...")
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)

def red_light_green_light_loop(duration, on_green, on_red, players):
    print("\n🔫 Game Start!")
    start_time = time.time()
    eliminated_players = set()  # Track eliminated players

    while time.time() - start_time < duration:
        if len(eliminated_players) == len(players):  # Check if all are eliminated
            print("\n🚨 All players eliminated! Game Over!")
            return

        # GREEN LIGHT
        green_duration = random.uniform(5, 10)
        print("\n🟢 GREEN LIGHT! (Move!)")
        on_green()
        time.sleep(green_duration)

        # RED LIGHT
        red_duration = random.uniform(3, 7)
        print("\n🔴 RED LIGHT! (Stop!)")
        eliminated_players.update(on_red(players, red_duration))  # Update eliminated players
        

    print("\n🏁 Game Over!")
