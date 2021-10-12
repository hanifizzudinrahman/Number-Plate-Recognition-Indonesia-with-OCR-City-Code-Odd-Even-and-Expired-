import os
import glob
import cv2
import easyocr
from Utils_NumberPlateRecognition import check1Line, corrrectCity, correctCapital, checkCity, checkOddEven, correctNumber, showText
import Utils

imagesPath = "Images\\"
reader = easyocr.Reader(['en'])
numberPlatePoints = []

heightNumberPlate = 250

def main():
    for filename in glob.glob(imagesPath+"*.jpg"):
        img = cv2.imread(filename)
        scale = round(heightNumberPlate / img.shape[0], 1)
        img = Utils.resize(img, scale)

        detail = reader.readtext(img)

        numberPlate, datePlate = check1Line(img, detail)
        # print("numberPlate:", numberPlate)
        # print("datePlate:", datePlate)

        numberPlate, code, city, oddEven = detailNumberPlate(numberPlate)
        datePlate, month, year = detailDatePlate(datePlate)

        #printDetail(numberPlate, datePlate, code, city, oddEven, month, year)
        
        img = showText(img, numberPlate,datePlate,code,city,oddEven,month,year)

        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def detailNumberPlate(numberPlate):

    numberPlate = corrrectCity(numberPlate)
    numberPlate = correctCapital(numberPlate)

    code, city = checkCity(numberPlate)
    oddEven = checkOddEven(numberPlate)

    return numberPlate, code, city, oddEven

def detailDatePlate(datePlate):
    datePlate = correctNumber(datePlate)

    month = int(datePlate[:2])
    year = int("20" + datePlate[-2:])
    return datePlate, month, year

def printDetail(numberPlate, datePlate, code, city, oddEven, month, year):
    print("---"*20)
    print("numberPlateFix:", numberPlate)
    print("datePlateFix:", datePlate)
    print("- city code:", code)
    print("- city:", city)
    print("- type:", oddEven)
    print("- month:", month)
    print("- year:", year)
    print("---"*20)

if __name__ == '__main__':       
    # Calling main() function 
    main()