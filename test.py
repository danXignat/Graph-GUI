import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PySide6.QtGui import QPainterPath, QPen, QPainter
from PySide6.QtCore import Qt, QPointF

class DraggableCircle(QGraphicsEllipseItem):
    def __init__(self, x, y, radius):
        super().__init__(0, 0, radius * 2, radius * 2)
        self.setPos(x, y)
        self.setBrush(Qt.red)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionChange:
            self.scene().update_arc()  # Notify the scene to update the arc
        return super().itemChange(change, value)

class ArcScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.circle1 = DraggableCircle(100, 100, 20)  # First circle
        self.circle2 = DraggableCircle(300, 100, 20)  # Second circle
        self.addItem(self.circle1)
        self.addItem(self.circle2)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # Get the centers of the two circles
        center1 = self.circle1.sceneBoundingRect().center()
        center2 = self.circle2.sceneBoundingRect().center()

        # Define control points for the Bézier curve
        control_point1 = QPointF((center1.x() + center2.x()) / 2, center1.y())
        control_point2 = QPointF((center1.x() + center2.x()) / 2, center2.y())

        # Create the Bézier curve path
        path = QPainterPath()
        path.moveTo(center1)
        path.cubicTo(control_point1, control_point2, center2)

        # Draw the Bézier curve
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.blue, 3))
        painter.drawPath(path)

    def update_arc(self):
        self.update()  # Redraw the scene

class MyApp(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = ArcScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setFixedSize(500, 300)
        self.setSceneRect(0, 0, 500, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MyApp()
    view.show()
    sys.exit(app.exec())
