import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
frameCounter = 0

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,480)
cv2.createTrackbar("HUE MIN","HSV",0,179,empty)
cv2.createTrackbar("HUE MAX","HSV",179,179,empty)
cv2.createTrackbar("SAT MIN","HSV",0,255,empty)
cv2.createTrackbar("SAT MAX","HSV",255,255,empty)
cv2.createTrackbar("VAL MIN","HSV",0,255,empty)
cv2.createTrackbar("VAL MAX","HSV",255,255,empty)

while(True):
    frameCounter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0

    success, img = cap.read()
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HUE MIN", "HSV")
    h_max = cv2.getTrackbarPos("HUE MAX", "HSV")
    s_min = cv2.getTrackbarPos("SAT MIN", "HSV")
    s_max = cv2.getTrackbarPos("SAT MAX", "HSV")
    v_min = cv2.getTrackbarPos("VAL MIN", "HSV")
    v_max = cv2.getTrackbarPos("VAL MAX", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Colors', hStack)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cv2.release()
cv2.destroyAllWindows()
