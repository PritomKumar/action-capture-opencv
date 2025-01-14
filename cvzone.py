import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize the webcam and Hand Detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Function to detect gestures based on fingers up
def detect_gesture(fingers):
    if fingers == [0, 1, 0, 0, 0]:  # Only index finger up
        return "Pointing"
    elif fingers == [1, 1, 1, 1, 1]:  # All fingers up
        return "Open Palm"
    elif fingers == [0, 0, 0, 0, 0]:  # No fingers up
        return "Fist"
    elif fingers == [0, 1, 1, 0, 0]:  # Index and middle fingers up
        return "Peace Sign"
    elif fingers == [1, 0, 0, 0, 0]:  # Only thumb up
        return "Thumbs Up"
    else:
        return "Unknown Gesture"

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video.")
        break

    # Detect hands in the frame
    hands, img = detector.findHands(img)  # Returns hand details and the updated image

    if hands:
        hand = hands[0]  # Process the first detected hand
        fingers = detector.fingersUp(hand)  # Get which fingers are up
        gesture = detect_gesture(fingers)  # Recognize the gesture

        # Display the gesture on the screen
        cv2.putText(
            img, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )

    # Show the video feed
    cv2.imshow("Gesture Recognition", img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
