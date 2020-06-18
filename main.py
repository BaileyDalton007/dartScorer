from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import screenshot

errorMargin = 10

#gives a array of background to compare to
initArr = screenshot.beforeDart()
print(initArr)

while True:
    compArr = screenshot.afterDart(initArr)
    if len(compArr) > errorMargin:
        print('found!')
        break
    else:
        print(len(compArr))