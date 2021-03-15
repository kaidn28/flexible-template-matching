import numpy as np 
import cv2 

image = cv2.imread('./chessboard.jpg')
image = cv2.resize(image,(int(image.shape[1]/2), int(image.shape[0]/2)))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('wtf', gray)
cv2.waitKey()
cv2.destroyAllWindows()

top = (225, 200)
right = (250, 210)
left = (215, 225)
bottom = (245, 230)


gray_cp = gray.copy()

ppoints = [(top, right), (top, left), (right, bottom),(left, bottom)]
for p in ppoints:
    cv2.line(gray_cp, p[0], p[1], 255, 1)

cv2.imshow('wtf', gray_cp)
cv2.waitKey()
cv2.destroyAllWindows()

template = gray_cp.copy()[top[1]: bottom[1], left[0]:right[0]]
cv2.imshow('wtf', template)
cv2.waitKey()
cv2.destroyAllWindows()

def line(point1, point2):
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]
    assert not (x1 == x2 and y1 == y2)
    if y1 == y2:
        return (0, 1, -y1)
    else :
        
        return (1,(x2-x1)/(y1 - y2), (x2*y1 - x1*y2)/(y1-y2))

    
def relativePosition(point, line):
    x = point[0]
    y = point[1]
    a = line[0]
    b = line[1]
    c = line[2]
    return a*x + b*y +c >= 0

def isInTemplate(point, top, left, right, bottom):
    topleft = line(top, left)
    topright = line(top, right)
    rightbottom = line(right, bottom)
    leftbottom = line(left, bottom)
