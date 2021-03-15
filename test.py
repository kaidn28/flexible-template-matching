import numpy as np
import cv2
from TemplateMatching import *

         
image = cv2.imread('./chessboard.jpg')
image = cv2.resize(image,(int(image.shape[1]/2), int(image.shape[0]/2)))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#template region
ttop = Point(225, 200)
tleft = Point(215, 225)
tright = Point(250, 210)
tbottom = Point(245, 230)

#search region
stop = Point(225, 190)
sleft = Point(200, 225)
sright = Point(260, 210)
sbottom = Point(250, 240)


gray_cp = gray.copy()

ppoints = [(ttop, tright), (ttop, tleft), (tright, tbottom),(tleft, tbottom)]
pp2 = [(stop, sright), (stop, sleft), (sright, sbottom), (sleft, sbottom)]
for p in ppoints:
    cv2.line(gray_cp, (p[0].x, p[0].y),(p[1].x, p[1].y), 255, 1)
for p in pp2:
    cv2.line(gray_cp, (p[0].x, p[0].y),(p[1].x, p[1].y), 255, 1)

cv2.imshow('wtf', gray_cp)
cv2.waitKey()
cv2.destroyAllWindows()


templateRegion = Region(ttop, tleft, tright, tbottom)
searchRegion = Region(stop, sleft, sright, sbottom)

template = Template(gray, templateRegion)

cv2.imshow('template getters result', template.matrix)
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imwrite('./template.jpg',template.matrix)

flextm = FlexTM()

top, left, right, bottom , score = flextm.findTemplateMax(template, gray, searchRegion)

print(top)
print(left)
print(right)
print(bottom)
print(score)