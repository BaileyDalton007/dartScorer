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

errorMargin = 400

#gives a array of background to compare to
initArr1 = screenshot.beforeDart()
time.sleep(0.2)

(grabbed, frame) = camera.read()
cv2.imwrite('assets/screenshot.png', frame)
initArr2 = screenshot.beforeDart()
time.sleep(0.2)

(grabbed, frame) = camera.read()
cv2.imwrite('assets/screenshot.png', frame)
initArr3 = screenshot.beforeDart()

initArr = list(set().union(initArr1, initArr2, initArr3))

addArr = []
while True:
    (grabbed, frame) = camera.read()

    compArr = screenshot.afterDart(initArr)
    if len(compArr) > errorMargin:
        print('found!')
        print(len(compArr))
        time.sleep(2)
        (grabbed, frame) = camera.read()
        cv2.imwrite('assets/screenshot.png', frame)
        screenshot.showResult(compArr)
        
        break
    else:
        addArr.append(compArr)
        print('curr ' + str(len(compArr)))
        cv2.imwrite('assets/screenshot.png', frame)
        for i in range(len(addArr)):
            initArr = list(set().union(initArr, addArr[i]))
