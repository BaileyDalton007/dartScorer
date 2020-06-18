from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import screenshot
import time

camera = cv2.VideoCapture(0)
(grabbed, frame) = camera.read()
cv2.imwrite('assets/screenshot.png', frame)

errorMargin = 2000

#gives a array of background to compare to
initArr1 = screenshot.beforeDart()
time.sleep(0.5)
initArr2 = screenshot.beforeDart()
time.sleep(0.5)
initArr3 = screenshot.beforeDart()

initArr = list(set().union(initArr1, initArr2, initArr3))


while True:
    (grabbed, frame) = camera.read()

    compArr = screenshot.afterDart(initArr)
    if len(compArr) > errorMargin:
        print('found!')
        screenshot.showResult(compArr)
        break
    
    print('curr len' + str(len(compArr)))
    cv2.imwrite('assets/screenshot.png', frame)