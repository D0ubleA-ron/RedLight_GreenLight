import time
import random
#from gpiozero import LED, Buzzer
import keyboard
import pygame



#redLED = LED(17)
#greenLED = LED(27)
#buzzer = Buzzer(22)

def play_sound(audio_file):
    sound1 = pygame.mixer.Sound(audio_file)
    sound1.play()
    
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


def red_light_green_light_loop(duration, on_green, on_red, players):
    print("\n🔫 Game Start!")
    start_time = time.time()
    eliminated_players = set()  # Track eliminated players

    while time.time() - start_time < duration:
        if len(eliminated_players) == len(players):  # Check if all are eliminated
            #buzzer.on()
            time.sleep(0.1)
            #buzzer.off()
            #buzzer.on()
            time.sleep(0.1)
            #buzzer.off()
            #buzzer.on()
            time.sleep(0.5)
            #buzzer.off()
            print("\n🚨 All players eliminated! Game Over!")
            play_sound('game_end.mp3')
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
    play_sound('game_end.mp3')