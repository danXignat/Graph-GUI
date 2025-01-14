from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainterPath
from PySide6.QtWidgets import QGraphicsItem

import math

from config import ARROW_SIZE, NODE_RADIUS
from utils import geometry
from viewmodel import ArcViewModel
from .Arrow import Arrow
from .Line import Line

class ArcView(QGraphicsItem):
    def __init__(self, start_point: QPointF, viewmodel: ArcViewModel):
        super().__init__()
        
        self.size = ARROW_SIZE
        
        self.viewmodel = viewmodel
        self.line  = Line(start_point, start_point, parent = self)
        self.arrow = Arrow(self.size, parent=self)
        self.nodes = {"start" : None, "end" : None}

        self.updateArrowPos()
        self.setZValue(0)
    
    #--------------------------------Draw------------------------------------
    
    def boundingRect(self) -> QRectF:
        return self.line.boundingRect().united(self.arrow.boundingRect())

    def paint(self, painter, option, widget=None):
        pass

    def shape(self) -> QPainterPath:
        return self.line.shape().united(self.arrow.shape())

    #--------------------------------Input-------------------------------------
    
 
    
    #------------------------------Methods-------------------------------------

    def updateArrowPos(self):
        self.arrow.setPos(self.line.line().p2())
        
        angle = geometry.getAngle(
                self.line.line().p1(),
                self.line.line().p2()
            )
                
        self.arrow.setRotation(angle)
    
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
        
    def fixArc(self, end_node):
        """algad to win"""
        center1 = self.line.line().p1()                                         #first node center
        center2 = end_node.mapToScene(end_node.boundingRect().center())     #second node center
        
        fixed_point = geometry.intersectionPoint(center1, center2, NODE_RADIUS, ARROW_SIZE)

        self.setEndPoint(fixed_point)
    
    def getArrowPoint(self):
        return self.arrow.getArrowPoint()
    
    def update(self):
        self.setStartPoint(self.nodes["start"].scenePos())
        self.fixArc(self.nodes["end"])