import cv2
import numpy as np
import imutils
import time
from DirectKeys import PressKey, ReleaseKey
from DirectKeys import W,A,S,D
from imutils.video import VideoStream

yellowLower = np.array([23,107,111])
yellowUpper = np.array([33,255,255])

cap = VideoStream(src=0).start()
time.sleep(2.0)
current_key_pressed = set()
circle_radius = 30
windowSize = 160

while True:
    keyPressed = False
    keyPressed_lr = False

    frame = cap.read()
    height, width = frame.shape[:2]

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    left_mask = mask[:, 0:width // 2, ]
    right_mask = mask[:, width // 2:, ]

    cnts_left = cv2.findContours(left_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_left = imutils.grab_contours(cnts_left)
    center_left = None

    cnts_right = cv2.findContours(right_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_right = imutils.grab_contours(cnts_right)
    center_right = None

    if len(cnts_left) > 0:
        c = max(cnts_left, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        center_left = (int(M["m10"] / (M["m00"] + 0.000001)), int(M["m01"] / (M["m00"] + 0.000001)))

        if(radius > circle_radius):

            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center_left, 5, (0, 0, 255), -1)
            if(center_left[1] < (height / 2 - windowSize // 2)):
                cv2.putText(frame, 'LEFT', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                PressKey(A)
                current_key_pressed.add(A)
                keyPressed = True
                keyPressed_lr = True
            elif(center_left[1] > (height / 2 + windowSize // 2)):
                cv2.putText(frame, 'RIGHT', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                PressKey(D)
                current_key_pressed.add(D)
                keyPressed = True
                keyPressed_lr = True

    if(len(cnts_right) > 0):
        c2 = max(cnts_right, key=cv2.contourArea)
        ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
        M2 = cv2.moments(c2)
        center_right = (int(M2["m10"] / (M2["m00"] + 0.000001)), int(M2["m01"] / (M2["m00"] + 0.000001)))
        center_right = (center_right[0] + width // 2, center_right[1])

        if(radius2 > circle_radius):
            cv2.circle(frame, (int(x2) + width // 2, int(y2)), int(radius2),
                       (0, 255, 255), 2)
            cv2.circle(frame, center_right, 5, (0, 0, 255), -1)
            if(center_right[1] < (height // 2 - windowSize // 2)):
                cv2.putText(frame, 'UP', (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                PressKey(W)
                keyPressed = True
                current_key_pressed.add(W)
            elif(center_right[1] > (height // 2 + windowSize // 2)):
                cv2.putText(frame, 'DOWN', (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                PressKey(S)
                keyPressed = True
                current_key_pressed.add(S)

    frame_copy = frame.copy()
    frame_copy = cv2.rectangle(frame_copy, (0, height // 2 - windowSize // 2), (width, height // 2 + windowSize // 2),
                               (255, 0, 0), 2)
    cv2.imshow("Frame", frame_copy)

    if(not keyPressed and len(current_key_pressed) != 0):
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()

    if(not keyPressed_lr and ((A in current_key_pressed) or (D in current_key_pressed))):
        if(A in current_key_pressed):
            ReleaseKey(A)
            current_key_pressed.remove(A)
        elif(D in current_key_pressed):
            ReleaseKey(D)
            current_key_pressed.remove(D)

    key = cv2.waitKey(1) & 0xFF

    if(key == ord("q")):
        break

cap.stop()
# close all windows
cv2.destroyAllWindows()