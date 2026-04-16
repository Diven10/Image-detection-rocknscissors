# Rock Paper Scissors using Hand Gesture Detection

A computer vision based Rock Paper Scissors game built using Python, OpenCV, and MediaPipe.

The project uses your webcam to detect hand gestures in real time and automatically identifies whether the player is showing Rock, Paper, or Scissors.

---

## Features

* Real-time hand tracking using webcam
* Finger counting using MediaPipe hand landmarks
* Automatic gesture recognition:

  * Rock
  * Paper
  * Scissors
* Countdown before each round
* Computer-generated random move
* Score tracking for player and computer
* Simple keyboard controls

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* Random module
* Time module

---

## Project Structure

```text
project-folder/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/Diven10/Image-detection-rocknscissors.git
cd Image-detection-rocknscissors
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Requirements

```txt
opencv-python
mediapipe==0.10.14
```

---

## How to Run

```bash
python app.py
```

---

## Controls

* Press `S` to start a new round
* Show your hand gesture before the countdown ends
* Press `ESC` to exit the game

---

## Gesture Mapping

| Finger Count | Gesture  |
| ------------ | -------- |
| 0 Fingers    | Rock     |
| 2 Fingers    | Scissors |
| 5 Fingers    | Paper    |

---

## How It Works

1. The webcam captures live video.
2. MediaPipe detects hand landmarks.
3. The number of fingers shown is counted.
4. Based on the finger count, the gesture is identified.
5. The computer randomly selects Rock, Paper, or Scissors.
6. The winner is displayed and scores are updated.

---

## Future Improvements

* Add better gesture accuracy
* Add sound effects
* Add GUI buttons
* Add multiplayer mode
* Add difficulty levels
* Store match history

---

## Author

Developed by Deven and Pradnya
