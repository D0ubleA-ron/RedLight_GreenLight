
# RedLight_GreenLight

This project contains the code for the red light green light game from Squid Games. Based on the YOLO model, this code is built to be run on a raspberry PI or your local device.

## How does this work?
System overview:
   Video Processing: Using the lightweight YOLOv8n model, the system continuously captures and processes video streams in real time from a camera attached to the Raspberry Pi. This allows for accurate detection of human movement and position, which is critical to the gameplay. Continually monitoring the user allows us to avoid latency issues that we ran into if we started and stopped the camera based on red or green light situation.

   Game Mechanics: The game begins when the user starts the code. They then have 5 seconds to move back as far as they can in the camera frame before the red light-green light portion of the game begins. During the green light phase, the user is free to move. The system does track their motion but it ignores any movement as the user is allowed to move in this time. During the red light phase, the user is not allowed to move. The system now becomes sensitive to any movement and will end the game if it detects any movement past the threshold.

   Output components: This project hsa two output componenents. The first is an audio integration streamed by the raspberry Pi to a bluetooth speaker. This feature provides start cues to the user so that if they cannot see the lights or the screen, they can still play the game. The second output components are the red and green lights which are connected to the raspberry Pi via GPIO pins and act as a quick visual guide to the user.

   User interaction: The goal for the user is to successfully get to the computer without moving during the red light phase and clicking on the spacebar. Once they click on the spaebar, the game ends and the user wins. 

   Broader outcomes: While this project was built for fun, the fundamental technology implemented to detect and track humans has huge real world applications. This can be used to enhance security cameras, track public pedestrian movement to improve infrastructure and predict traffic, track pedestrians in an automated vechicle, detect if a patient has fallen in a healthcare setting, and in home automation.

   Reflection: Overall we were pretty happy with the project, and pretty hapy with the fact that we could get quite computationally heavy code working on a raspberry Pi in real time. We could have explored other ways to make the computation faster, however we couldn't due to time restrictions. If we were to do it again, we would definetly implement this with edge computing as it would enable us to do real time computing while improving computing performance, and enabling us to use the GPIO connections for auditory and visual outputs. We think remote computing wouldn't work in this case as the lag may be too high for the game to work in real time, however edge computing wouldn't have that problem.

## How to run this locally?

1. Clone this github repo.
2. Open terminal and run the following command `pip install numpy==1.26.0 opencv-python==4.11.0.86 ultralytics==8.3.88 pygame --system-break-packages`
3. Once the packages are done installing, open the terminal and navigate to the REDLIGHT_GREENLIGHT folder. Then enter the following commands one by one.
   a. `cd local_dev`
   b. `cd backend`
   c. `cd motion_detection`
4. Now you are in the right folder. Start the game using the following command `python motion_detection.py` and have fun!

### Demo Video

[![Watch my video](https://img.youtube.com/vi/2emOTJnwu4c/0.jpg)](https://youtu.be/2emOTJnwu4c)

   



### Hardware Schematic
![Screenshot 2025-04-02 at 11 22 52 PM](https://github.com/user-attachments/assets/80bccf1c-a986-430a-accd-d78733c23369)

