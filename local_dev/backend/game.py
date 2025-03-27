import time
import random
from gpiozero import LED, Buzzer

redLED = LED(17)
greenLED = LED(27)
buzzer = Buzzer(22)

def get_player_names(num_players):
    players = {}
    print("\nEnter player names:")
    for i in range(num_players):
        name = input(f"Player {i+1} Name: ")
        players[i] = name
    return players

def countdown(seconds=5):
    # Play game start countdown audio
    play_sound('/mnt/data/game_start_countdown.mp3')
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
            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
            print("\n🚨 All players eliminated! Game Over!")
            play_sound('/mnt/data/game_end.mp3')
            return

        # GREEN LIGHT
        redLED.off()
        green_duration = random.uniform(5, 10)
        print("\n🟢 GREEN LIGHT! (Move!)")
        greenLED.on()
        on_green()
        buzzer.on()
        time.sleep(0.1)
        buzzer.off()
        time.sleep(green_duration)
        greenLED.off()

        # RED LIGHT
        red_duration = random.uniform(3, 7)
        print("\n🔴 RED LIGHT! (Stop!)")
        redLED.on()
        # Play red light countdown sound at the start of red light
        play_sound('/mnt/data/redlight_countdown.mp3')
        buzzer.on()
        time.sleep(0.1)
        buzzer.off()
        time.sleep(red_duration)
        
        eliminated_players.update(on_red(players, red_duration))  # Update eliminated players

    print("\n🏁 Game Over!")
    play_sound('/mnt/data/game_end.mp3')