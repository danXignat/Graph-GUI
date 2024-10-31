import math

from PySide6.QtCore import QPointF

def getAngle(p1: QPointF, p2: QPointF):
    dy = p1.y() - p2.y()
    dx = p1.x() - p2.x()

    return math.degrees(math.atan2(dy, dx)) - 90

def intersectionPoint(center1: QPointF, center2:QPointF, radius: float, offset: float):
    """Calculates coordinates of intersection between line determined by two circle centers
    and the circumference of the second one with the offset that is the distance between dragging
    point of arrow and the arrow peak"""
    distance = radius + offset                                              #distance from second center to the end of line
                
    director = center2 - center1                                            #director vector
    norm = math.hypot(director.x(), director.y())                           #distance between 2 centers
    unit = director/norm                                                    #cos

    fixed_point = center2 - unit * distance                                 #correct point of the end of line
    
    return fixed_point