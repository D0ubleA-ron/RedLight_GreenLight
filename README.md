# RedLight_GreenLight

## Table of Contents
- [Introduction](#introduction)
- [How Does This Work?](#how-does-this-work)
- [Project Planning](#project-planning)
- [Credits](#credits)
- [Design Process](#design-process)
- [Hardware Decisions](#hardware-decisions)
- [Conclusions](#conclusions)
- [How to Run This Locally](#how-to-run-this-locally)
- [Demo Video](#demo-video)
- [Hardware Schematic](#hardware-schematic)
- [UML Diagram](#uml-diagram)

## Introduction
This project contains the code for the Red Light, Green Light game inspired by *Squid Games*. It leverages the YOLOv8n model and is designed to run on a Raspberry Pi or a local device. The project not only serves as an interactive game but also demonstrates real-time video processing and human motion detection.

## How Does This Work?

**System Overview:**

- **Video Processing:**  
  Using the lightweight YOLOv8n model, the system continuously captures and processes video streams in real time from a camera attached to the Raspberry Pi. This allows for accurate detection of human movement and position, which is critical to the gameplay. Continual monitoring of the user helps avoid the latency issues that would arise if the camera was started and stopped based on the red or green light situation.

- **Game Mechanics:**  
  The game starts when the user initiates the code. The user is given 5 seconds to move back as far as possible within the camera frame before the red light-green light phase begins.  
  - **Green Light Phase:** The user is free to move; the system tracks their motion but ignores any movement during this period.
  - **Red Light Phase:** The user must remain completely still. The system becomes sensitive to any movement and will end the game if it detects motion beyond a preset threshold.

- **Output Components:**  
  - **Audio Integration:**  
    Audio is streamed from the Raspberry Pi to a connected Bluetooth speaker. This provides start cues and other audio feedback, ensuring that the user can follow the game even if visual cues are missed.
  - **LED Visual Indicators:**  
    Red and green LEDs connected via GPIO pins serve as quick visual indicators:
    - **Green Light:** Indicates the user is allowed to move.
    - **Red Light:** Signals that the user must remain still.

- **User Interaction:**  
  The objective for the user is to successfully get to the computer without moving during the red light phase and then press the spacebar. Once the spacebar is pressed, the game ends, and the user wins.

- **Broader Outcomes:**  
  Although built for fun, the underlying technology of real-time human detection and motion tracking has significant real-world applications. This technology can enhance security cameras, monitor pedestrian movement to optimize infrastructure and traffic flow, assist in self-driving vehicle navigation, detect falls in healthcare settings, and contribute to more intuitive home automation systems.

## Project Planning

Team composition:
| Name | Major | Year
|-------|------|-------|
| Ved Ballary | Computer Science | 5th Year
| Aaron Deo | Computer Science | 5th Year
| Ian Park | Computer Engineering | 2nd Year
| Souvik Mazumder | Computer Engineering | 2nd Year
| Aryan Roshan | Computer Engineering | 2nd Year
| Siam Ibne Nasir | Computer Engineering | 2nd Year

Team responsibilities:
| Name              | Role                      | Responsibilities                                                                                                                                                                            |
|-------------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ian Park          | Embedded Systems Engineer | Handles microcontroller programming, sensor integration and real-time system control. Ensures hardware-software communication is seamless.                                                 |
| Siam Ibne Nasir   | Embedded Systems Engineer | Develops and manages complex electrical applications and circuits to ensure compatibility. Will be integrating the speaker/buzzer for game signals.                                       |
| Souvik Mazumder   | Embedded Systems Engineer | Will be managing hardware parts and making sure all parts are compatible with each other. And integrating the Camera’s sensing algorithm in order to detect motion.                       |
| Aryan Roshan      | Software Developer        | Developing core game systems and game states like Game Start & End sequences, Red light/Green light functionality, Win and Lose States etc.                                              |
| Ved Ballary       | Software Developer        | Implement multiple human detection using OpenCV library and python.                                                                                                                       |
| Aaron Deo         | Software Developer        | Research and Implement human motion detection through OpenCV and how to detect movement with each separate person.                                                                          |

Planning:
We decided that the best approach for this project would be agile due to it's develop and reiterate approach. To execute this, we split the project into 5 sprints. We would meet on that start of each sprint to decide the tasks, point them, and split them evenly. We used miro to organize our tasks, github to host our codebase, and discord for instant communication.

<img width="1010" alt="Screenshot 2025-04-08 at 12 11 45 PM" src="https://github.com/user-attachments/assets/a9b8ac70-6254-4c7a-bd49-27636796e209" />



## Credits

## Design Process


## Hardware Decisions
### Demo Video
[![Watch my video](https://img.youtube.com/vi/2emOTJnwu4c/0.jpg)](https://youtu.be/2emOTJnwu4c)

### Hardware Schematic
![Screenshot 2025-04-02 at 11 22 52 PM](https://github.com/user-attachments/assets/80bccf1c-a986-430a-accd-d78733c23369)

### UML Diagram
![UML Diagram](https://github.com/user-attachments/assets/f6052a6a-2f70-4928-a99e-6a956c922210)

## Conclusions


## How to Run This Locally

1. Clone this github repo.
2. Open terminal and run the following command `pip install numpy==1.26.0 opencv-python==4.11.0.86 ultralytics==8.3.88 pygame --system-break-packages`
3. Once the packages are done installing, open the terminal and navigate to the REDLIGHT_GREENLIGHT folder. Then enter the following commands one by one.
   a. `cd local_dev`
   b. `cd backend`
   c. `cd motion_detection`
4. Now you are in the right folder. Start the game using the following command `python motion_detection.py` and have fun!


