import time
import random
#from gpiozero import LED, Buzzer
import keyboard
import pygame
from pynput import keyboard

pygame.mixer.init(frequency=22050, size=-8, channels=2, buffer=512)
game_start_countdown_sound = pygame.mixer.Sound('game_start_countdown.mp3')
game_end_sound = pygame.mixer.Sound('game_end.mp3')

#redLED = LED(17)
#greenLED = LED(27)
#buzzer = Buzzer(22)

def play_sound(sound):
    sound.play()
    
def get_player_names(num_players):
    players = {}
    print("\nEnter player names:")
    for i in range(num_players):
        name = input(f"Player {i+1} Name: ")
        players[i] = name
    return players

def countdown(seconds=5):
    # Play game start countdown audio
    play_sound(game_start_countdown_sound)

def on_press(key):
    global game_won
    if key == keyboard.Key.space:
        # Set flag and stop listener
        game_won = True
        return False  # Stop the listener

def red_light_green_light_loop(duration, on_green, on_red, players):
    print("\n🔫 Game Start!")
    start_time = time.time()
    eliminated_players = set()  # Track eliminated players

    while time.time() - start_time < duration:
        if game_won:
            print("\n🏁 Game Won!")
            play_sound(game_end_sound)
            return

        if len(eliminated_players) == len(players):  # Check if all are eliminated
            if len(players) == 1:
                print("\n🏆 Player {} wins!".format(list(players.keys())[0]))
                play_sound(game_end_sound)
                return
            print("\n🚨 All players eliminated! Game Over!")
            play_sound(game_end_sound)
            return
        
        # GREEN LIGHT
        #redLED.off()
        green_duration = random.uniform(2, 5)
        print("\n🟢 GREEN LIGHT! (Move!)")
        #greenLED.on()
        on_green()
        #buzzer.on()
        time.sleep(0.1)
        #buzzer.off()
        time.sleep(green_duration)
        #greenLED.off()

        # RED LIGHT
        red_duration = random.uniform(2, 5)
        print("\n🔴 RED LIGHT! (Stop!)")
        #redLED.on()
        # Play red light countdown sound at the start of red light
        #play_sound('redlight_countdown.mp3')
        #buzzer.on()
        time.sleep(0.1)
        #buzzer.off()
        time.sleep(red_duration)
        
        eliminated_players.update(on_red(players, red_duration))  # Update eliminated players

    print("\n🏁 Game Over!")
    play_sound(game_end_sound)
