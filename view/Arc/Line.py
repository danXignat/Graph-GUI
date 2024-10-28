from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui  import QPen

class Line(QGraphicsLineItem):
    def __init__(self, start_point: QPointF, end_point: QPointF, parent):
        super().__init__(
            start_point.x(), start_point.y(),
            end_point.x(), end_point.y(),
            parent = parent
        )

        pen = QPen(Qt.GlobalColor.blue)
        pen.setWidth(8)
        self.setPen(pen)