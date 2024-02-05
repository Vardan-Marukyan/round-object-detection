import cv2
import imutils
import numpy as np
import requests
from PIL import Image
import io
import sys


url = sys.argv[1]

response = requests.get(url)
exit() if response.status_code != 200 else None
image = Image.open(io.BytesIO(response.content))
img_np = np.array(image)


def circlePercentage (array):
    plus = len(array)
    plus -= sum(1 for el in array if el >= 0)
    percent = round(plus / len(array) * 100)
    return percent > 65

def calculateAangle(xy1, xy2):
    [x1, y1], [x2, y2] = xy1, xy2
    angle_degrees = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    return angle_degrees

def picturesFigure(image):
    if(len(image.shape) != 3):
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaus = cv2.GaussianBlur(gray, (5,5), 2)
    canny = cv2.Canny(gaus, 10, 90)

    ker = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closed = cv2.morphologyEx(canny,cv2.MORPH_CLOSE, ker)

    conturs = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conturs = imutils.grab_contours(conturs)
    if len(conturs) > 1:
        return False
    for contur in conturs:
        approx = cv2.approxPolyDP(contur, 0.01* cv2.arcLength(contur, True), True)
        figureAngle = []

        if 8 <  len(approx):
            arr = []
            for index in range(len(approx)-1):
                figureAngle.append(round(calculateAangle( approx[index][0], approx[index+1][0])))
            for index in range(len(figureAngle)-1):
                arr.append(figureAngle[index+1] - figureAngle[index])
            return circlePercentage(arr)
                
    return False

print(picturesFigure(img_np))