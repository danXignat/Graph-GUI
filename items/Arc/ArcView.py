from PySide6.QtCore import QPointF, QRectF, Qt, QRect, QLineF, QLine
from PySide6.QtGui import QPainterPath, QPainter, QPen, QFont
from PySide6.QtWidgets import QGraphicsItem

import math

from config import ARROW_SIZE, NODE_RADIUS
from utils import geometry
from .Arrow import Arrow
from .Line import Line
import math
class ArcView(QGraphicsItem):
    def __init__(self, start_point: QPointF):
        super().__init__()
        
        self.size = ARROW_SIZE
        self.line = Line(start_point, start_point, parent=self)
        self.line.hide()
        self.arrow = Arrow(self.size, parent=self)
        self.nodes = {"start": None, "end": None}
        self.midpoint = None
        self.setup_mid_point()
        self.updateArrowPos()
        self.setZValue(0)
        self.setFlag(QGraphicsItem.ItemClipsToShape, False)
        self.setFlag(QGraphicsItem.ItemClipsChildrenToShape, False)
        self.weight = None
        self.color = "blue"
        
    def setup_mid_point(self):
        start = self.line.line().p1()
        end = self.line.line().p2()
        
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        distance = math.sqrt(dx * dx + dy * dy)
        angle = math.atan2(dy, dx)
        
        curve_height = min(distance * 0.5, 100)
        
        perpendicular_x = -math.sin(angle) * curve_height
        perpendicular_y = math.cos(angle) * curve_height
        
        self.midpoint = self.mapToScene(QPointF(
            (start.x() + end.x()) / 2 + perpendicular_x,
            (start.y() + end.y()) / 2 + perpendicular_y
        ))
    
    def boundingRect(self) -> QRectF:
        start = self.line.line().p1()
        end = self.line.line().p2()
        
        if self.midpoint is None:
            self.setup_mid_point()
        
        left = min(start.x(), end.x(), self.midpoint.x())
        right = max(start.x(), end.x(), self.midpoint.x())
        top = min(start.y(), end.y(), self.midpoint.y())
        bottom = max(start.y(), end.y(), self.midpoint.y())
        
        padding = 100
        return QRect(
            left - padding,
            top - padding,
            (right - left) + 2 * padding,
            (bottom - top) + 2 * padding
        )
    
    def paint(self, painter: QPainter, option, widget=None):
        start = self.line.line().p1()
        end = self.line.line().p2()
        self.setup_mid_point()
        
        path = QPainterPath()
        path.moveTo(start)
        path.quadTo(self.midpoint, end)
        
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color)
        pen.setWidth(7)
        painter.setPen(pen)
        painter.drawPath(path)
        
        if self.weight:
            painter.setFont(QFont("Verdana", 12))
            painter.drawText(self.midpoint, self.weight)
        
        self.update()

    #------------------------------Methods-------------------------------------

    def updateArrowPos(self):
        self.arrow.setPos(self.line.line().p2())
        
        tangent = QLineF(self.midpoint, self.line.line().p2())
        angle = math.degrees(90+math.atan2(tangent.dy(), tangent.dx()))
        
        # angle = geometry.getAngle(
        #         self.line.line().p1(),
        #         self.line.line().p2()
        #     )
                
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
        
    def fixArc(self, end_pos: QPointF):
        """algad to win"""
        center1 = self.line.line().p1()                                     #first node center
        center2 = end_pos
        
        fixed_point = geometry.intersectionPoint(center1, center2, NODE_RADIUS, ARROW_SIZE)

        self.setEndPoint(fixed_point)
    
    def getArrowPoint(self):
        return self.arrow.getArrowPoint()
    
    def update_pos(self):
        self.setStartPoint(self.nodes["start"].scenePos())
        self.fixArc(self.nodes["end"].pos())