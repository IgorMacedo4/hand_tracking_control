import cv2
import mediapipe as mp
import pyautogui

# Class for detecting and tracking hands
class HandDetector:
    def __init__(self, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        # Initialize the MediaPipe hand detection module with customizable parameters
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=max_hands, min_detection_confidence=detection_confidence, min_tracking_confidence=tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        # Convert the BGR image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image to find hands
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Draw hand landmarks and connections on the image
                self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []  # List to store landmark positions
        x_max, y_max = 0, 0
        x_min, y_min = img.shape[1], img.shape[0]

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])  # Add ID and coordinates to the list
                if draw:
                    x_min, y_min = min(x_min, cx), min(y_min, cy)
                    x_max, y_max = max(x_max, cx), max(y_max, cy)

        if draw and lm_list:
            # Draw a rectangle around the hand
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        return lm_list

    def count_fingers(self, lm_list):
        fingers = []  # List to identify raised fingers
        # Thumb
        if lm_list[4][1] < lm_list[3][1]:
            fingers.append(1)  # Thumb is up
        else:
            fingers.append(0)  # Thumb is down

        # Other fingers
        for id in [8, 12, 16, 20]:
            if lm_list[id][2] < lm_list[id - 2][2]:
                fingers.append(1)  # Finger is up
            else:
                fingers.append(0)  # Finger is down
        
        return sum(fingers)  # Return the total count of raised fingers

    def get_index_finger_position(self, lm_list):
        """
        Returns the position (x, y) of the index finger tip.
        """
        return lm_list[8][1], lm_list[8][2]

# Main function
def main():
    # Initialize video capture from the webcam
    cap = cv2.VideoCapture(0)
    detector = HandDetector()  # Initialize the hand detector
    screenWidth, screenHeight = pyautogui.size()
    frameWidth, frameHeight = 640, 480
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Hand Tracking", frameWidth, frameHeight)

    while True:
        success, img = cap.read()  # Read a frame from the webcam
        if not success:
            continue

        img = cv2.flip(img, 1)  # Flip the image horizontally to reflect hand movement
        img = detector.find_hands(img)  # Find and draw hands on the image
        lm_list = detector.find_position(img, draw=True)  # Find positions of hand landmarks

        if lm_list:
            finger_count = detector.count_fingers(lm_list)  # Count raised fingers
            color = (0, 255, 0)

            if finger_count == 4:
                x, y = detector.get_index_finger_position(lm_list)
                pyautogui.moveTo(screenWidth * (x / frameWidth), screenHeight * (y / frameHeight))
                cv2.circle(img, (x, y), 15, (0, 0, 255), cv2.FILLED)

            elif finger_count == 5:
                pyautogui.click()  # Mouse click

            elif finger_count == 2:
                pyautogui.scroll(-1)  # Scroll up

            elif finger_count == 3:
                pyautogui.scroll(1)  # Scroll down

            cv2.putText(img, str(finger_count), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

        cv2.imshow("Hand Tracking", img)  # Display the image with hand tracking
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()  # Release video capture
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    main()  # Call the main function when the script is executed
