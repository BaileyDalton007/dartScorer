from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import screenshot

camera = cv2.VideoCapture(0)
(grabbed, frame) = camera.read()
cv2.imwrite('assets/screenshot.png', frame)

errorMargin = 10

#gives a array of background to compare to
initArr = screenshot.beforeDart()

while True:
    (grabbed, frame) = camera.read()

    compArr = screenshot.afterDart(initArr)
    if len(compArr) > errorMargin:
        print('found!')
        break
    
    print(len(compArr))
    cv2.imwrite('assets/screenshot.png', frame)