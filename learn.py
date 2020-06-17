import cv2 as cv2

cap = cv2.VideoCapture(0)

#different kinds of trackers (look at docs or smth)
#tracker = cv2.TrackerMOSSE_create()
tracker = cv2.TrackerCSRT_create()

success, img = cap.read()
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img, bbox)

def drawBox(img, bbox):
    # bbox is a tuple, needs to be converted into integers
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 255), 3, 1)
    cv2.putText(img, str("Tracking"), (75,50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,225,0), 2)

while True:
    #timer = cv2.getTickCount()
    
    success, img = cap.read()

    success, bbox = tracker.update(img) 

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, str("Lost"), (75,50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

    #fps counter that doesnt work
    #fps = cv2.getTickFrequency()/(cv2.getTickCount() - timer)
    #cv2.putText(img, str(fps), (75,50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
