import time
import random

def red_light_green_light(duration=600): 
    print("Game starting in...")

    for i in range (5, 0, -1):
        print(i)
        time.sleep(1)

    print("\n Game Start!")
    start_time = time.time()  
    

    while time.time() - start_time < duration:
        
        green_duration = random.uniform(5, 15)   
        print("\n🟢 GREEN LIGHT! (Move!)")
        time.sleep(green_duration)

        
        red_duration = random.uniform(2, 7)  
        print("\n🔴 RED LIGHT! (Stop!)")
        time.sleep(red_duration)

    print("\nGame Over!")

if __name__ == "__main__":
    red_light_green_light()