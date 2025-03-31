import time
import random
import pygame
from pynput import keyboard
from gpiozero import LED  # Import gpiozero for LED control

# Initialize LED objects on the specified GPIO pins
red_led = LED(17)
green_led = LED(22)

# Global flag to detect game win
game_won = False

def play_sound(audio_file, wait=False):
    sound = pygame.mixer.Sound(audio_file)
    channel = sound.play()
    if wait:
        # Wait until the sound finishes playing
        while channel.get_busy():
            time.sleep(0.1)
    return channel
    
def get_player_names(num_players):
    players = {}
    print("\nEnter player names:")
    for i in range(num_players):
        name = input(f"Player {i+1} Name: ")
        players[i] = name
    return players

def countdown(seconds=5):
    # Play game start countdown audio
    play_sound('game_start_countdown.mp3')

def on_press(key):
    global game_won
    if key == keyboard.Key.space:
        # Set flag and stop listener
        game_won = True
        return False  # Stop the listener

def interruptible_sleep(duration):
    """Sleep in small increments, checking for the spacebar press."""
    start = time.time()
    while time.time() - start < duration:
        if game_won:
            return False  # Interrupted by spacebar press
        time.sleep(0.1)
    return True

def red_light_green_light_loop(duration, on_green, on_red, players):
    global game_won
    print("\n🔫 Game Start!")
    start_time = time.time()
    eliminated_players = set()  # Track eliminated players

    # Start the keyboard listener in a non-blocking way
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while time.time() - start_time < duration:
        if game_won:
            print("\n🏁 Game Won!")
            play_sound('game_end.mp3')
            # Ensure LEDs are off
            red_led.off()
            green_led.off()
            return

        if len(eliminated_players) == len(players):  # Check if all are eliminated
            if len(players) == 1:
                print("\n🏆 Player {} wins!".format(list(players.keys())[0]))
                play_sound('game_end.mp3')
                red_led.off()
                green_led.off()
                return
            print("\n🚨 All players eliminated! Game Over!")
            play_sound('game_end.mp3')
            red_led.off()
            green_led.off()
            return

        # GREEN LIGHT phase
        
        green_duration = random.uniform(2, 5)
        print("\n🟢 GREEN LIGHT! (Move!)")
        green_led.on()   # Turn on green LED
        red_led.off()    # Ensure red LED is off
        on_green()       # Call your green light callback
        time.sleep(0.1)
        if not interruptible_sleep(green_duration):
            green_led.off()
            print("\nSpacebar pressed during GREEN LIGHT. Ending game!")
            play_sound('game_end.mp3')
            time.sleep(3)
            return
        green_led.off()  # Turn off green LED after phase

        # RED LIGHT phase
        red_duration = random.uniform(2, 5)
        play_sound('red_lightcountdown.mp3', wait=True)
        
        print("\n🔴 RED LIGHT! (Stop!)")
        red_led.on()     # Turn on red LED
        green_led.off()  # Ensure green LED is off
        time.sleep(0.1)
        if not interruptible_sleep(red_duration):
            red_led.off()
            print("\nSpacebar pressed during RED LIGHT. Ending game!")
            play_sound('game_end.mp3')
            time.sleep(3)
            return
        red_led.off()    # Turn off red LED after phase

        # Call red light callback with red_duration as argument.
        on_red(red_duration)

    print("\n🏁 Game Over!")
    play_sound('game_end.mp3')
    red_led.off()
    green_led.off()
