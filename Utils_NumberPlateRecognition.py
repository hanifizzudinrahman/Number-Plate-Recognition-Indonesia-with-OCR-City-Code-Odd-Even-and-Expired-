import cv2
from cityCode import cityCode_dict
from datetime import datetime
import numpy as np

def check1Line(img, detail):
    date = False
    tolerance = int (img.shape[0] / 7)
    yline1 = 0
    numberPlate = ""

    datePlate = ""

    for i in range (len(detail)):        
        # Check Line
        if i == 0:
            yline1 = detail[i][0][0][1]
            numberPlate = detail[i][1]
            
        else:
            if date == False:
                yMin = yline1 - tolerance
                yMax = yline1 + tolerance
                if yMin < detail[i][0][0][1] < yMax:
                    numberPlate = numberPlate + " " + detail[i][1]
                else:
                    date = True

        if date ==  True:
            datePlate = datePlate + detail[i][1]

        img = createRectangle(img, detail[i][0])

    return numberPlate, datePlate

def createRectangle(img, points):
    color = (0,255,255)
    thickness = 1
    cv2.line(img, points[0], points[1], color, thickness)
    cv2.line(img, points[1], points[2], color, thickness)
    cv2.line(img, points[2], points[3], color, thickness)
    cv2.line(img, points[3], points[0], color, thickness)
    
    return img

def corrrectCity(numberPlatePoints):

    numberPlatePoints = list(numberPlatePoints)
    for i in range (2): # 2 First Digit

        if numberPlatePoints[i] == "0":
            numberPlatePoints[i] = "D"
        elif numberPlatePoints[i] == "5":
            numberPlatePoints[i] = "S"
        elif numberPlatePoints[i] == "6":
            numberPlatePoints[i] = "G" 
        elif numberPlatePoints[i] == "8":
            numberPlatePoints[i] = "B" 

    numberPlatePoints = "".join(numberPlatePoints)
    return numberPlatePoints

def correctCapital(numberPlate):
    numberPlate = list(numberPlate)
    numberPlate = [x.upper() for x in numberPlate]
    numberPlate = "".join(numberPlate)

    return numberPlate

def checkCity(numberPlate):
    cityCode = numberPlate.split()[0]

    if cityCode in cityCode_dict:
        city = cityCode_dict[cityCode]
    else:
        city = "Error City"

    return cityCode, city

def checkOddEven(numberPlate):
    status = "None"
    for x in numberPlate:
        try:
            x = int(x)
            if x%2 == 0:
                status = "Even"
            else:
                status = "Odd"
        except ValueError:
            pass

    return status

def correctNumber(datePlate):
    datePlate = list(datePlate)
    for i in range (len(datePlate)):

        if datePlate[i] == "D" or datePlate[i] == "O" or datePlate[i] == "o":
            datePlate[i] = "0"
        elif datePlate[i] == "S" or datePlate[i] == "s":
            datePlate[i] = "5"
        elif datePlate[i] == "G":
            datePlate[i] = "6" 
        elif datePlate[i] == "B":
            datePlate[i] = "8" 

    datePlate = "".join(datePlate)
    datePlate = datePlate.replace(" ", "")

    #for r in ((".", " "), ("*", " "), (",", " "), ("'", " ")):
        #datePlate = datePlate.replace(*r)

    return datePlate    

def showText(img, numberPlate,datePlate,code,city,oddEven,month,year):
    color = (255,255,0)
    colorG = (0,255,0)
    colorR = (0,0,255)
    thickness = 2
    scale = 2
    distance = int(img.shape[0] / 7)

    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    timeNow = str(currentDay) + "/" + str(currentMonth) + "/" + str(currentYear)

    status = ""
    if currentDay%2 == 0:
        status = "Even"
    else:
        status = "Odd"
    statusText = "Status: " + status
    #Black
    img[0:int(1 * distance)+5 , img.shape[1] - 170:img.shape[1]] = np.zeros(((1*distance)+5 , 170, 3), np.uint8)
    
    cautionStatus = ""
    if status != oddEven:
        cautionStatus = " (VIOLATION!)"    

    cautionExpired = ""
    if year < currentYear:
        cautionExpired = " (VIOLATION!)"
    elif year == currentYear:
        if month <= currentMonth:
            cautionExpired = " (VIOLATION!)"
    textExpired = "Expired: " + str(month) + "/" + str(year)

    cv2.putText(img, timeNow, (img.shape[1] - 170, int(0.5 * distance)), cv2.FONT_HERSHEY_PLAIN, 1.5, color, thickness)
    cv2.putText(img, statusText, (img.shape[1] - 170, int(1 * distance)), cv2.FONT_HERSHEY_PLAIN, 1.5, color, thickness)

    cv2.putText(img, numberPlate, (20, img.shape[0] - int(2.1 * distance)), cv2.FONT_HERSHEY_PLAIN, scale, color, thickness)
    cv2.putText(img, "City: " + str(city), (20, img.shape[0] - int(1.5 * distance)), cv2.FONT_HERSHEY_PLAIN, 1.5, colorG, thickness)
    cv2.putText(img, "Type: " + oddEven, (20, img.shape[0] - 1 * distance), cv2.FONT_HERSHEY_PLAIN, 1.5, colorG, thickness)
    cv2.putText(img, textExpired, (20, img.shape[0] - int(0.5 * distance)), cv2.FONT_HERSHEY_PLAIN, 1.5, colorG, thickness)
    cv2.putText(img, cautionStatus, (20+135, img.shape[0] - int(1 * distance)), cv2.FONT_HERSHEY_PLAIN, 1, colorR, thickness)
    cv2.putText(img, cautionExpired, (20+225, img.shape[0] - int(0.5 * distance)), cv2.FONT_HERSHEY_PLAIN, 1, colorR, 2)

    return img    