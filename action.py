import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

# Variables for motion detection
prev_hand_landmarks = None
motion_detected = ""
last_motion_time = 0  # Timestamp of the last detected motion
linger_duration = 2  # Seconds to linger the detected motion

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video.")
        break

    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for hand landmarks
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            # Extract landmark positions
            landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

            # Detect motions
            if prev_hand_landmarks:
                # Compute distances or patterns
                current_motion = ""

                # Detect grabbing motion
                finger_tip_ids = [4, 8, 12, 16, 20]  # Thumb and fingers
                palm_id = 0  # Wrist as palm reference
                is_grabbing = all(
                    np.linalg.norm(np.array(landmarks[finger_id][:2]) - np.array(landmarks[palm_id][:2])) < 0.1
                    for finger_id in finger_tip_ids
                )
                if is_grabbing:
                    current_motion = "Grabbing"

                # Detect waving motion
                wrist = landmarks[0]
                prev_wrist = prev_hand_landmarks[0]
                if abs(wrist[0] - prev_wrist[0]) > 0.05:  # Horizontal motion
                    current_motion = "Waving"

                # Detect punching motion
                if abs(wrist[2] - prev_wrist[2]) > 0.1:  # Forward motion (depth)
                    current_motion = "Punching"

                # Update motion if detected
                if current_motion:
                    motion_detected = current_motion
                    last_motion_time = time.time()

            # Update previous landmarks
            prev_hand_landmarks = landmarks

    # Check if the motion should still linger
    if motion_detected and time.time() - last_motion_time > linger_duration:
        motion_detected = ""

    # Display detected motion on the frame
    if motion_detected:
        cv2.putText(
            frame, motion_detected, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )

    # Display the frame
    cv2.imshow("Hand Motion Detection", frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
