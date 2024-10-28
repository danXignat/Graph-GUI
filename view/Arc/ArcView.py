from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainterPath
from PySide6.QtWidgets import QGraphicsItem

import math

from config import ARROW_SIZE
from .Arrow import Arrow
from .Line import Line

class ArcView(QGraphicsItem):
    def __init__(self, start_point: QPointF, end_point: QPointF, parent):
        super().__init__(parent=parent)
        
        self.setZValue(0)
        self.size = ARROW_SIZE
        self.line  = Line(start_point, end_point, parent = self)
        self.arrow = Arrow(self.size, parent=self)
        self.updateArrowPos()
    
    def boundingRect(self) -> QRectF:
        return self.line.boundingRect()

    def paint(self, painter, option, widget=None):
        pass

    def shape(self) -> QPainterPath:
        return self.line.shape()

    def updateArrowPos(self):
        self.arrow.setPos(self.line.line().p2())
        self.arrow.setRotation(
            self.getAngle()
        )

    def getAngle(self):
        point1 = self.line.line().p1()
        point2 = self.line.line().p2()

        dy = point1.y() - point2.y()
        dx = point1.x() - point2.x()
    
        return math.degrees(math.atan2(dy, dx)) - 90
    
    def setStartPoint(self, start_point: QPointF):
        line = self.line.line()
        line.setP1(start_point)
        self.line.setLine(line)

        self.updateArrowPos()
    
    def setEndPoint(self, end_point: QPointF):
        line = self.line.line()
        line.setP2(end_point)
        self.line.setLine(line)
        
        self.updateArrowPos()
        
    def fixArc(self):
        """algad to win"""
        other_node = self.edge.end_node
        
        center1 = self.line.line().p1()                                         #first node center
        center2 = other_node.mapToScene(other_node.boundingRect().center())     #second node center
        distance = other_node.radius + self.size                                #distance from second center to the end of line
                
        director = center2 - center1                                            #director vector
        norm = math.hypot(director.x(), director.y())                           #distance between 2 centers
        unit = director/norm                                                    #cos

        fixed_point = center2 - unit * distance                                 #correct point of the end of line

        self.setEndPoint(fixed_point)
    
    def getArrowPoint(self):
        return self.arrow.getArrowPoint()
    
    def setStartNode(self, node):
        self.edge.start_node = node
        
    def setEndNode(self, node):
        self.edge.end_node = node