import numpy as np
import imutils
import cv2

colorLower = (3, 100, 100)
colorUpper = (17, 255, 255)


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
    frame = imutils.resize(img, width=100)
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

    return pointArr

def afterDart(arr):
    img = cv2.imread('assets/screenshot.png')
    frame = imutils.resize(img, width=100)
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

    clusterRange = 40
    numClusterPts = 2
    clusterPointArr = []


    for x in range(numClusterPts):
        clusterArr = []
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
        highestScores = []
        
        highestScores.append(newClusterArr[-1])
        clusterPos = clusterArr.index(highestScores[0])
        print('clusterPos:' + str(clusterPos))
        print('coordARR:' + str(len(coordArr)))
        print('Iteration:' + str(x))

        clusterPoint = coordArr[clusterPos]
        clusterPointArr.append(clusterPoint)
        removeArr = []
        for j in range(len(coordArr)):
            if (coordArr[clusterPos][0] - coordArr[j][0])^2 + (coordArr[clusterPos][1] - coordArr[j][1])^2 < clusterRange^2:
                removeArr.append(coordArr[j])

        for i in range(len(removeArr)):
            coordArr.remove(removeArr[i])            

    #if coordArr and len(coordArr) > 0:
    #    for i in range(len(coordArr)):
    #        cv2.circle(img, (coordArr[i][0], coordArr[i][1]), 2, (0, 255, 255), -1)
    #        xArr.append(coordArr[i][0])
    #        yArr.append(coordArr[i][1])

    #    a, b = bestFit(xArr, yArr)
    #    height, width, channels = img.shape
    #    startPoint = (0, int(a))
    #    endPoint = (width, int(a+b*width))
    #img = cv2.line(img,clusterPointArr[0],clusterPointArr[1],(255,0,0),5)
    #else: 
    #    print('No color recognized')
    print('Arr:'+ str(len(clusterPointArr)))
    img = cv2.line(img,clusterPointArr[0],clusterPointArr[1],(255,0,0),5)
    for i in range(len(clusterPointArr)):
        cv2.circle(img, clusterPointArr[i], 2, (0, 0, 255), 5)
    
    cv2.imwrite('assets/test.png', img)
    