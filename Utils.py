import cv2
import numpy as np

move = False
xMouse, yMouse = 0,0

## TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def initializeTrackbars(intialTracbarVals=0):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", 200,255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 200, 255, nothing)
 
 
def valTrackbars():
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    src = Threshold1,Threshold2
    return src
     
def findPositionCorner(myPoints):
 
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
 
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
 
    return myPointsNew
  
def nothing(x):
    pass

def resize(img, scale):
    widthNew = int(img.shape[1] * scale)
    heightNew = int(img.shape[0] * scale)
    dim = (widthNew, heightNew)
    img = cv2.resize(img, dim)
    return img

def findRectangle(contours):
    rectCor = []
    for i in contours:
        area = cv2.contourArea(i)   
        if area > 500:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            if len(approx) == 4:
                rectCor.append(i)
    rectCor = sorted(rectCor, key=cv2.contourArea, reverse=True) 
    return rectCor     

def FixCornerPositions(imgReal, points):
    img = imgReal.copy()
    points = points.reshape((4, 2))
    space = 10

    while True:
        img = imgReal.copy()
        img = makeCircle(img, points, (0,0,255), 4)
        img = drawRectangle(img,points,2)
        cv2.imshow('img', img)
        
        cv2.setMouseCallback("img", mousePoints)
        
        if int(points[0][0] + space) > xMouse > int(points[0][0] - space) and int(points[0][1] + space) > yMouse > int(points[0][1] - space):
            points[0] = xMouse, yMouse
        elif int(points[1][0] + space) > xMouse > int(points[1][0] - space) and int(points[1][1] + space) > yMouse > int(points[1][1] - space):
            points[1] = xMouse, yMouse
        elif int(points[2][0] + space) > xMouse > int(points[2][0] - space) and int(points[2][1] + space) > yMouse > int(points[2][1] - space):
            points[2] = xMouse, yMouse
        elif int(points[3][0] + space) > xMouse > int(points[3][0] - space) and int(points[3][1] + space) > yMouse > int(points[3][1] - space):
            points[3] = xMouse, yMouse

        if cv2.waitKey(1) == ord("s"):
            break
    return img, points

def makeCircle(img, points, color, radius):
    imgC = cv2.circle(img, points[0], radius, color, -1)
    imgC = cv2.circle(img, points[1], radius, color, -1)
    imgC = cv2.circle(img, points[2], radius, color, -1)
    imgC = cv2.circle(img, points[3], radius, color, -1)
    return imgC

def mousePoints (event, x, y, flags, params):
    global move,xMouse,yMouse
    if event == cv2.EVENT_LBUTTONDOWN:
        move = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if move == True:
            xMouse, yMouse = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        move = False
    
def drawRectangle(img,points,thickness):
    cv2.line(img, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0, 255, 0), thickness)
    cv2.line(img, (points[1][0], points[1][1]), (points[2][0], points[2][1]), (0, 255, 0), thickness)
    cv2.line(img, (points[2][0], points[2][1]), (points[3][0], points[3][1]), (0, 255, 0), thickness)
    cv2.line(img, (points[3][0], points[3][1]), (points[0][0], points[0][1]), (0, 255, 0), thickness)
    return img

def cropRectangle(img, position):
    img = img[position[0][1]:position[1][1], position[0][0]:position[1][0]]
    return img
