import cv2
import mediapipe as mp
import random
import time
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
tip_ids = [4, 8, 12, 16, 20]

game_data = {"player_score": 0, "computer_score": 0}
game_state = "IDLE" 
start_time = 0
result_text = ""
computer_move = ""
player_move_locked = ""

def count_fingers(landmarks):
    fingers = []
    if landmarks[tip_ids[0]][0] > landmarks[tip_ids[0]-1][0]: fingers.append(1)
    else: fingers.append(0)
    for i in range(1, 5):
        if landmarks[tip_ids[i]][1] < landmarks[tip_ids[i]-2][1]: fingers.append(1)
        else: fingers.append(0)
    return fingers.count(1)

def get_gesture(finger_count):
    if finger_count == 0: return "Rock"
    elif finger_count == 2: return "Scissors"
    elif finger_count == 5: return "Paper"
    return None

def get_winner(player, computer):
    if player == computer: return "Draw"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Scissors" and computer == "Paper") or \
         (player == "Paper" and computer == "Rock"):
        return "You Win"
    else:
        return "Computer Wins"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset')
def reset():
    global game_data, game_state
    game_data["player_score"] = 0
    game_data["computer_score"] = 0
    game_state = "IDLE"
    return jsonify({"status": "success"})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global game_state, start_time, result_text, computer_move, player_move_locked, game_data
    
    font = cv2.FONT_HERSHEY_DUPLEX
    NEON_GREEN = (50, 255, 50)
    NEON_YELLOW = (0, 200, 255)
    NEON_RED = (0, 0, 255)

    # Decode image from browser
    data = request.json['image']
    header, encoded = data.split(',', 1)
    nparr = np.frombuffer(base64.b64decode(encoded), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img = cv2.flip(img, 1)
    h, w, c = img.shape
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    display_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    player_move = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                display_img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=NEON_GREEN, thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=(0, 200, 0), thickness=2)
            )
            landmarks = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))
            
            finger_count = count_fingers(landmarks)
            player_move = get_gesture(finger_count)

    current_time = time.time()
    cv2.rectangle(display_img, (0, 0), (w, 140), (10, 15, 10), -1)
    cv2.rectangle(display_img, (0, h - 60), (w, h), (10, 15, 10), -1)

    if game_state == "IDLE":
        cv2.putText(display_img, "RAISE HAND TO START", (50, 60), font, 1.2, NEON_GREEN, 2)
        if player_move:
            game_state = "COUNTDOWN"
            start_time = current_time

    elif game_state == "COUNTDOWN":
        remaining = 3 - int(current_time - start_time)
        if remaining > 0:
            cv2.putText(display_img, f"SCANNING... {remaining}", (50, 60), font, 1.2, NEON_RED, 2)
            if player_move:
                cv2.putText(display_img, f"DETECTED: {player_move}", (50, 110), font, 1, NEON_YELLOW, 2)
        else:
            game_state = "RESULT"
            start_time = current_time
            computer_move = random.choice(["Rock", "Paper", "Scissors"])
            
            if player_move:
                player_move_locked = player_move
                result_text = get_winner(player_move_locked, computer_move)
                if result_text == "You Win": game_data["player_score"] += 1
                elif result_text == "Computer Wins": game_data["computer_score"] += 1
            else:
                player_move_locked = "NONE"
                result_text = "NO HAND DETECTED"

    elif game_state == "RESULT":
        elapsed = current_time - start_time
        if elapsed < 4: 
            cv2.putText(display_img, f"P1: {player_move_locked} vs CPU: {computer_move}", (30, 60), font, 1.0, NEON_GREEN, 2)
            res_col = NEON_GREEN if result_text == "You Win" else NEON_RED if result_text == "Computer Wins" else NEON_YELLOW
            cv2.putText(display_img, f"STATUS: {result_text}", (30, 110), font, 1.2, res_col, 2)
        else:
            game_state = "IDLE" 

    cv2.putText(display_img, f"P1 SCORE: {game_data['player_score']} | CPU SCORE: {game_data['computer_score']}", (30, h - 20), font, 1.0, NEON_GREEN, 2)

    # Encode back to browser
    _, buffer = cv2.imencode('.jpg', display_img)
    encoded_out = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')
    return jsonify({'image': encoded_out})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
