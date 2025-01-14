import cv2
import mediapipe as mp

# Initialize MediaPipe Holistic
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video.")
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for holistic detection
    results = holistic.process(frame_rgb)

    # Draw face landmarks
    if results.face_landmarks:
        mp_drawing.draw_landmarks(
            frame, 
            results.face_landmarks, 
            mp_holistic.FACEMESH_TESSELATION,  # Dense face mesh
            landmark_drawing_spec=None,  # No points, just mesh
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 0), thickness=1, circle_radius=1
            ),
        )

    # Draw pose landmarks
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, 
            results.pose_landmarks, 
            mp_holistic.POSE_CONNECTIONS
        )

    # Draw hand landmarks
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, 
            results.left_hand_landmarks, 
            mp_holistic.HAND_CONNECTIONS
        )
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, 
            results.right_hand_landmarks, 
            mp_holistic.HAND_CONNECTIONS
        )

    # Display the frame
    cv2.imshow("Detailed Contours (Face, Hands, Body)", frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
