from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui  import QPen, QPolygonF, QBrush

class Arrow(QGraphicsPolygonItem):
    def __init__(self, size: int, parent):
        super().__init__(parent = parent)
        
        self.size = size
        self.setPolygon(QPolygonF([
            QPointF(0, 0),
            QPointF(-size/2, size/2),          
            QPointF(0, -size),             
            QPointF(size/2, size/2)   
        ]))
        
        brush = QBrush(Qt.GlobalColor.blue)
        self.setBrush(brush)

        pen = QPen(Qt.GlobalColor.blue)
        self.setPen(pen)
        
    def getArrowPoint(self):
        return self.mapToScene(self.boundingRect().center() - QPointF(0, self.size))