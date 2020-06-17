from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# use bgr_hsv_converter.py to get upper and lower values
colorLower = (-5, 100, 100)
colorUpper = (15, 255, 255)
pts = deque(maxlen=args["buffer"])
 
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

else:
    camera = cv2.VideoCapture(args["video"])

#main loop, 'q' to break
status = ('Lost', (0, 0, 255))
lastCoords = (0 ,0)
while True:

    # grab the current frame
    (grabbed, frame) = camera.read()
    
    frame = imutils.resize(frame, width=600)
    frame = imutils.rotate(frame, angle=180)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # (x, y) center of the point
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    
    # If tracking an object
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            
            #cv2.circle(frame, center, 5, (0, 0, 255), -1)

            lastCoords = center
            
            #how far back the comparison goes 
            compIndex = 50
            if len(pts) > compIndex:
                compArr = [] #test how many of last 10 frames where within the range of curr point, put in array, the see if that array is mostly true/false
                for i in range(compIndex):
                    if pts[-1] != None and pts[-1*i] != None:
                        # displays if dart is moving or not (within a range)
                        errorRange = 3
                        if (pts[-1*i][0] - pts[-1][0])^2 + (pts[-1*i][1] - pts[-1][0])^2 < errorRange^2:
                            compArr.append(1)
                        else:
                            compArr.append(0)
                sum = 0
                for i in range(0, len(compArr)):
                    sum = sum + compArr[i]
                
                # percent out of compIndex that decides if an object is still or not
                passingScore = 0.6
                if sum >= (passingScore * compIndex):             
                    status = ('Still', (0, 255, 0))
                    cv2.imwrite('assets/screenshot.png', frame)
                else:
                    status = ('Moving', (255, 0, 0))
    else:
        status = ('Lost', (0, 0, 255))

    
    image = cv2.putText(frame, status[0], (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, status[1], 2, cv2.LINE_AA)
    image = cv2.putText(frame, str(lastCoords), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,  
            1, (0, 255, 0), 2, cv2.LINE_AA)

    
    # update the points queue
    pts.appendleft(center)
    
        # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
 
 
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
camera.release()
cv2.destroyAllWindows()