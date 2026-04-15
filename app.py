import cv2
import mediapipe as mp
import random
import time

# Initialize
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

tip_ids = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

# Game variables
start_time = 0
countdown = 5
result = ""
player_score = 0
computer_score = 0
round_active = False

def count_fingers(landmarks):
    fingers = []

    # Thumb
    if landmarks[tip_ids[0]][0] > landmarks[tip_ids[0]-1][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1, 5):
        if landmarks[tip_ids[i]][1] < landmarks[tip_ids[i]-2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def get_gesture(finger_count):
    if finger_count == 0:
        return "Rock"
    elif finger_count == 2:
        return "Scissors"
    elif finger_count == 5:
        return "Paper"
    return None

def get_winner(player, computer):
    if player == computer:
        return "Draw"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Scissors" and computer == "Paper") or \
         (player == "Paper" and computer == "Rock"):
        return "You Win"
    else:
        return "Computer Wins"

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    player_move = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))

            finger_count = count_fingers(landmarks)
            player_move = get_gesture(finger_count)

    # Start round with 's'
    key = cv2.waitKey(1)

    if key == ord('s'):
        start_time = time.time()
        round_active = True
        result = ""

    if round_active:
        elapsed = int(time.time() - start_time)
        remaining = countdown - elapsed

        cv2.putText(img, f'Show your move: {remaining}', (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if remaining <= 0:
            round_active = False

            computer_move = random.choice(["Rock", "Paper", "Scissors"])

            if player_move:
                result = get_winner(player_move, computer_move)

                if result == "You Win":
                    player_score += 1
                elif result == "Computer Wins":
                    computer_score += 1
            else:
                result = "No Move Detected"
    else:
        cv2.putText(img, "Press 'S' to Start", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Display info
    cv2.putText(img, f'Your Move: {player_move}', (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if not round_active and 'computer_move' in locals():
        cv2.putText(img, f'Computer: {computer_move}', (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(img, f'Result: {result}', (50, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.putText(img, f'You: {player_score}  Computer: {computer_score}', (50, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Rock Paper Scissors", img)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()