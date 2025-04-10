# Young Hee Robot/Squid Game Robot

## Table of Contents
- [Introduction](#introduction)
- [How Does This Work?](#how-does-this-work)
- [Project Planning](#project-planning)
- [Credits](#credits)
- [Design Process](#design-process)
- [Hardware Decisions](#hardware-decisions)
- [Software Decisions](#software-decisions)
- [Youtube/Public Video](#youtubepublic-video)
- [Hardware Schematic](#hardware-schematic)
- [UML Diagram](#uml-diagram)
- [How to Run This Locally](#how-to-run-this-locally)
- [Conclusions](#conclusions)

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
| Name | Major | Email
|-------|------|-------|
| Ved Ballary | Computer Science | vedb44@proton.me
| Aaron Deo | Computer Science | aarondeo14@gmail.com
| Ian Park | Computer Engineering | ianpark115@gmail.com
| Souvik Mazumder | Computer Engineering | souvikmazumder2002@gmail.com
| Aryan Roshan | Computer Engineering | arynrosh@gmail.com
| Siam Ibne Nasir | Computer Engineering | siamibne1512@gmail.com

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
- https://www.youtube.com/watch?v=EPuyPuyS-F0 (Tutorial for redlight greenlight on arduino)
- https://anytool.in/blog/post/build-your-own-red-light-green-light-with-python/ (Helped us with logic)
- https://courses.ece.cornell.edu/ece5990/ECE5725_Spring2022_Projects/Wednesday%20May%2018/Squid%20Game/project_website/index.html (Similar project done at Cornell, helped with ideation)

## Design Process
Developing the Young-hee doll replica started with making UML diagrams to define the system's structure and behavior. We used the diagrams to develop and test isolated software modules, which verified that essential functions like game logic and motion detection operated correctly. After achieving software stability, we started working on hardware implementation. The Raspberry Pi 4 served as the main component for an uncomplicated circuit arrangement that included two LEDs for visual indication purposes on a breadboard. The first hardware tests used a buzzer to confirm the system's audio performance and timing accuracy. Once we verified that the system operated correctly, we swapped out the buzzer for a Bluetooth speaker to deliver synchronized game audio during gameplay.

## Hardware Decisions
-Raspberry Pi 4 (central controller)
-Breadboard
-Two LEDs (red and green to provide visual cues of red light and green light)
-Two resistors (to prevent damaging the LEDs)
-MM and MF wires (connections within the breadboard and to the GPIO and power pins of the Raspberry Pi 4)
-Initially a buzzer, later changed to a Bluetooth speaker integrated with in-game audio.
-Motion camera (to detect the presence of a player)

## Software Decisions

### Libraries
- **Pygame**: Used for playing sounds at different phases of the game (e.g., game start, end, red light, and elimination events). It provides crucial audio feedback to enhance player immersion.
- **Pynput**: Handles keyboard input, specifically monitoring for spacebar presses to detect player interaction or premature movement.
- **GPIOZero**: Controls GPIO pins on the Raspberry Pi for LED output, signaling Red Light and Green Light states with physical lights.
- **OpenCV (cv2)**: Captures and processes video input from the webcam. It is essential for real-time player movement tracking and frame annotation.
- **YOLO (Ultralytics)**: A pose estimation model used to detect and track player skeletons for motion validation during Red Light phases.
- **NumPy**: Powers vector math and data operations for calculating player center points and detecting movement thresholds.

### Language and IDE
  - **Language**: Python was selected for its rich ecosystem, rapid prototyping capability and hardware library support (e.g., GPIOZero).
  - **IDE**: Visual Studio Code was used for development due to its Python support, integrated terminal, debugging tools and GitHub integration.

### Team Collaboration Tools
  - **Discord**: Used for daily communication, team check-ins and sharing updates asynchronously.
  - **Miro**: Employed for sprint planning, task mapping and brainstorming ideas visually.
  - **Planning Poker**: Utilized during sprint planning sessions to assign story points to tasks which balanced workload distribution across the team.

## Youtube/Public Video
### Click on the image to watch the video
[![Watch my video](https://img.youtube.com/vi/2emOTJnwu4c/0.jpg)](https://youtu.be/2emOTJnwu4c)

## Hardware Schematic
![Screenshot 2025-04-02 at 11 22 52 PM](https://github.com/user-attachments/assets/80bccf1c-a986-430a-accd-d78733c23369)

## UML Diagram
![UML Diagram](https://github.com/user-attachments/assets/f6052a6a-2f70-4928-a99e-6a956c922210)


## How to Run This Locally

1. Clone this github repo.
2. Open terminal and run the following command `pip install numpy==1.26.0 opencv-python==4.11.0.86 ultralytics==8.3.88 pygame --system-break-packages`
3. Once the packages are done installing, open the terminal and navigate to the REDLIGHT_GREENLIGHT folder. Then enter the following commands one by one.
   a. `cd local_dev`
   b. `cd backend`
   c. `cd motion_detection`
4. Now you are in the right folder. Start the game using the following command `python motion_detection.py` and have fun!


## Conclusions
Due to the low processing power of the Raspberry Pi, our ability to integrate many features was limited, like running the motion detection smoothly with multiple people. However, through continuous software optimization and knowledge gained throughout the course and labs, we were able to mitigate these hardware limitations and have our vision model detect an individual’s movement more accurately and faster. With further innovation, our project has the potential to be applied in automated surveillance of homes and AI-driven training simulations for athletes.

Siam - Working on the project proposal for building a Young-hee robot inspired from the Netflix series “Squid Game” has been a challenging and exciting ride. I was responsible for identifying and defining the UML class diagram and UML use-case diagram. Identifying and defining the right classes for motion detection, movement control, and system flow required intense thinking and teamwork. Despite this complexity, my team’s dedication and working together made the process more fun and rewarding. We learned about new ideas, how to make this bot more interesting with added features, and pinpoint accuracy. Even though we haven’t started making the bot yet, it’s a great step towards understanding the system design. 

Souvik - Working in this project allowed me to learn more about microcontrollers, particularly the Raspberry Pi 4. This has been an exciting and challenging experience designing the whole Young Hee robot. The goal was to keep the design simple while ensuring functionality, which required thoughtful decision making about hardware components and software implementation. Beyond the technical aspects, this project reinforced the importance of efficient coding practices, hardware-software integration and problem-solving.Overall, this project has been an engaging learning experience, strengthening my skills in embedded systems, real-time computing, and AI-based vision processing. 

Ved - Working on the software requirements for the red light green light bot tested my problem solving skills. I started off my research with an incredibly open-ended question, “How do we detect multiple people, and track them, and detect their movement?”. After a lot of brainstorming with the team, we figured we could use a motion sensor and write some code to detect movement. However, that would have only worked for one person, and wouldn’t have embodied the multiplayer nature of the original game. So I got to researching, and I found out that YOLO with Python, and a camera sensor is a better solution for this implementation, as we can use pre-trained YOLO models to detect people within a frame. Overall, this was an incredibly tough problem to figure out because I have never worked on real time motion detection before, but eventually we managed to figure it out.

Ian - While working on the proposal for the Young-Hee Robot, I was given the opportunity to research and write about the hardware requirements that would be needed to design and build the robot. After brainstorming a list of components that would entail building the project, I compared that list with references of the robot as shown on the TV show as well as many scaled-down versions of the robot built by fans that were shared on the internet so that I could get a better understanding of what hardware resources would be necessary so that our robot could be very similar to what was shown on the show and based on what would be feasible in our limited time. By narrowing down our available resources, I completed the hardware requirements in the proposal by detailing how each component would be implemented and connect with one another to create a system that fulfills our design objectives.

Aryan - The Young-Hee Robot presents an enticing challenge as it is both ambitious and technically demanding. Through my preliminary research, I found that there are several challenges that require a lot of effort like sourcing the necessary components, learning new libraries for image recognition and programming the Raspberry Pi 4 for seamless system integration. Despite these challenges, our team is committed to learning, innovating and collaborating to bring this project to life. By leveraging our passion and knowledge, we aim to develop a fully functional system that showcases our technical skills while also having some fun!

Aaron - I found the research portion of this project very interesting. At first, I did not believe we could run a motion detection system on a Raspberry Pi given the amount of RAM, however I did notice that there were lightweight models that could be run on a Raspberry Pi. Also, integrating the software and hardware portions of this project took some thought since it is something I have never really done.  I think that the project idea is pretty interesting and fun since it takes a fictional idea and makes it into reality. I am interested to see how this progresses!




