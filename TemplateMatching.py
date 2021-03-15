import numpy as np 
import cv2 

class Point:
    def __init__(self, x , y):
        self.x = x
        self.y = y
    def __str__(self):
        return "x:  {0}\ty: {1} ".format(self.x, self.y)

class Line: 
    def __init__(self, point1, point2):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        assert not (x1 == x2 and y1 == y2)
        if y1 == y2:
            self.a = 0
            self.b = 1
            self.c = -y1
        else:
            self.a = 1
            self.b = (x2-x1)/(y1-y2)
            self.c = (x1*y2 - x2*y1)/(y1-y2)
class Region: 
    def __init__(self, top, left, right, bottom):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
    def edges(self):
        top_left = Line(self.top, self.left)
        top_right = Line(self.top, self.right)
        bottom_left = Line(self.bottom, self.left)
        bottom_right = Line(self.bottom, self.right)
        return (top_left, top_right, bottom_left, bottom_right)
    def range(self):
        x_min = self.left.x
        x_max = self.right.x
        y_min = self.top.y
        y_max = self.bottom.y
        return (x_min, x_max, y_min, y_max)
    def points(self):
        return (self.top, self.left, self.right, self.bottom)
    def heightwidth(self):
        return (self.bottom.y - self.top.y, self.right.x - self.left.x)

class Template:
    def __init__(self, image, templateRegion):
        top, left, right, bottom = templateRegion.points()
        h,w = templateRegion.heightwidth()
        oriTemplate = image.copy()[top.y: bottom.y, left.x:right.x]
        self.top = Point(top.x - left.x, 0)
        self.left = Point(0, left.y - top.y)
        self.right = Point(right.x - left.x, right.y - top.y)
        self.bottom = Point(bottom.x - left.x, bottom.y - top.y)
        self.templateRegion = Region(self.top, self.left, self.right, self.bottom)
        self.matrix = np.zeros((h, w))

        for i in range(h):
            for j in range(w):
                if isInRegion(Point(j,i), self.templateRegion):
                    if oriTemplate[i,j] == 255:
                        self.matrix[i,j] = 255
                    else:
                        self.matrix[i,j] = oriTemplate[i,j] + 1
    def corners(self):
        return (self.top, self.left, self.right, self.bottom)
                        
class FlexTM:
    def __init__(self):
        pass
    def findTemplateMax(self, template, image, searchRegion):
        x_min, x_max, y_min, y_max = searchRegion.range()
        sh, sw = searchRegion.heightwidth()
        roi = image.copy()[y_min:y_max, x_min:x_max]
        th, tw = template.matrix.shape
        sample_a = template.matrix.reshape(-1)
        #print(sample_a.shape)
        restrict_a = np.array([e for e in sample_a if not e == 0])
        #print(restrict_a.shape)
        nor_a = (restrict_a - np.mean(restrict_a))/(np.std(restrict_a)*len(restrict_a))
        max_score = 0
        loc_x = 0
        loc_y = 0
        for i in range(sh-th):
            for j in range (sw - tw):
                sample_b = roi[i:i+th, j:j+tw].reshape(-1)
                restrict_b = np.array([sample_b[i] for i, e in enumerate(sample_a) if not e == 0])
                nor_b = (restrict_b - np.mean(restrict_b))/(np.std(restrict_b))
                score = np.correlate(nor_a, nor_b)[0]
                if score > max_score:
                    loc_x = j
                    loc_y = i
                    max_score = score
        corners = template.corners()
        top = Point(loc_x + x_min + corners[0].x, loc_y + y_min + corners[0].y)
        left = Point(loc_x + x_min + corners[1].x, loc_y + y_min + corners[1].y)
        right = Point(loc_x + x_min + corners[2].x, loc_y + y_min + corners[2].y)
        bottom = Point(loc_x + x_min + corners[3].x, loc_y + y_min + corners[3].y)
        return top, left, right, bottom, max_score

def relativePosition(point, line):
    x = point.x
    y = point.y
    a = line.a
    b = line.b
    c = line.c
    return a*x +b*y + c >= 0

def isInRegion(point, region):    
    top_left, top_right, bottom_left, bottom_right = region.edges()
    r_top_left = relativePosition(point, top_left)
    r_bottom_left = relativePosition(point, bottom_left)
    r_top_right = not relativePosition(point, top_right)
    r_bottom_right = not relativePosition(point, bottom_right)
    return (r_top_left and r_bottom_left and r_top_right and r_bottom_right)

