import cv2 as cv
import mediapipe as mp
import pyautogui

screen_w, screen_h = pyautogui.size()
cap = cv.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()

# for detecting hands in image , set static_image_mode in Hands() to true
mp_drawing = mp.solutions.drawing_utils
index_y = 0
index_x = 0
while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    if hands:
        for hand in hands:
            mp_drawing.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_w)
                y = int(landmark.y*frame_h)
                if id == 8:
                    cv.circle(frame, center=(x,y), radius=10, color=(0, 255, 255))
                    index_x = screen_w/frame_w*x
                    index_y = screen_h/frame_h*y
                    pyautogui.moveTo(index_x, index_y)
                if id == 4:
                    cv.circle(frame, center=(x,y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_w/frame_w*x
                    thumb_y = screen_h/frame_h*y
                    if abs(index_y - thumb_y) < 20 and (abs(index_x - thumb_x) < 20):
                        pyautogui.click()
                        pyautogui.sleep(1)
                        print("click")
    cv.imshow('virtual mouse', frame)
    cv.waitKey(1)