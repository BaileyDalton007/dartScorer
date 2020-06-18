import numpy as np
import imutils
import cv2

colorLower = (7, 100, 100)
colorUpper = (15, 255, 255)


def bestFit(X, Y):
    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar
    return a, b

def beforeDart():
    img = cv2.imread('assets/screenshot.png')
    frame = imutils.resize(img, width=600)
    frame = imutils.rotate(img, angle=180)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    maskBi = mask.astype(np.uint8)

    #get all non zero values
    coordArr = cv2.findNonZero(maskBi)
    if coordArr == None:
        coordArr = []
    else:
        coordArr = coordArr.tolist()
    pointArr = []
    for i in range(len(coordArr)):
        pointArr.append((coordArr[i][0][0], coordArr[i][0][1]))

    return pointArr

def afterDart(arr):
    img = cv2.imread('assets/screenshot.png')
    frame = imutils.resize(img, width=600)
    frame = imutils.rotate(img, angle=180)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    maskBi = mask.astype(np.uint8)

    #get all non zero values
    coordArr = cv2.findNonZero(maskBi)
    if coordArr is None:
        coordArr = []
    else:
        coordArr = coordArr.tolist()


    pointArr = []
    for i in range(len(coordArr)):
        pointArr.append((coordArr[i][0][0], coordArr[i][0][1]))

    diffArr = list(set(pointArr) - set(arr))
    return diffArr
    


def showResult(coordArr):
    xArr = []
    yArr = []
    img = cv2.imread('assets/screenshot.png')

    clusterArr = []
    clusterRange = 1
    for i in range(len(coordArr)):
        score = 0
        for j in range(len(coordArr)):
            if i == j:
                pass
            else:
                if (coordArr[i][0] - coordArr[j][0])^2 + (coordArr[i][1] - coordArr[j][1])^2 < clusterRange^2:
                    score = score + 1
        clusterArr.append(score)

    newClusterArr = clusterArr
    newClusterArr.sort()
    highestScore = newClusterArr[-1]
    clusterPos = clusterArr.index(highestScore)
    clusterPoint = coordArr[clusterPos]


    if coordArr and len(coordArr) > 0:
        for i in range(len(coordArr)):
            cv2.circle(img, (coordArr[i][0], coordArr[i][1]), 2, (0, 255, 255), -1)
            xArr.append(coordArr[i][0])
            yArr.append(coordArr[i][1])

        a, b = bestFit(xArr, yArr)
        height, width, channels = img.shape
        startPoint = (0, int(a))
        endPoint = (width, int(a+b*width))
        img = cv2.line(img,startPoint,endPoint,(255,0,0),5)
    else: 
        print('No color recognized')
    cv2.circle(img, clusterPoint, 2, (0, 0, 255), 5)
    
    cv2.imwrite('assets/test.png', img)
    