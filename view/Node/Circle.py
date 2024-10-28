from PySide6.QtWidgets import (
    QGraphicsEllipseItem, QGraphicsItem
)
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui  import QPainter, QPen, QBrush

class Circle(QGraphicsEllipseItem):
    def __init__(self, radius: float, parent: QGraphicsItem):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.setParentItem(parent)
        self.radius = radius
        
        pen = QPen(Qt.GlobalColor.white)
        pen.setWidth(4)
        self.setPen(pen)

        brush = QBrush(Qt.GlobalColor.blue)
        self.setBrush(brush)

        
    