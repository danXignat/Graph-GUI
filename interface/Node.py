from PySide6.QtWidgets import (
    QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent,
    QGraphicsEllipseItem, QGraphicsItem, QApplication
)
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui  import QPainter, QPainterPath, QColor

from typing import Any, Callable, List

from interface.Arc import QBrush, QPen
from interface.Circle import Circle
from interface.Text import Text

class Node(QGraphicsItem):
    def __init__(self, radius: float, pos: QPointF, number: int, app: QApplication):
        super().__init__()
        self.setPos(pos)
        self.setZValue(1)
        self.is_moving = False
        self.app = app
        self.radius = radius
        self.number = number
        
        self.circle = Circle(radius, self)
        self.text   = Text(number, self)
        self.text.center(self.circle)
        self.arcs: List[Any] = []
        
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        
    def paint(self, painter: QPainter, option, widget=None):
        pass
    
    def boundingRect(self) -> QRectF:
        return self.circle.boundingRect()
    
    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path
    #Hover
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.app.setOverrideCursor(Qt.OpenHandCursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.app.restoreOverrideCursor()
        return super().hoverEnterEvent(event)
    
    # #Press
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_moving = True
            
        return super().mousePressEvent(event)   

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            for arc in self.arcs:
                self.scene().removeItem(arc)
                del arc
            
            self.app.restoreOverrideCursor()
            print(f"[DELETED] {self}")
            self.scene().removeItem(self)
            del self
        else:
            return super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        if not self.is_moving:
            return super().mouseMoveEvent(event)
        
        displacement = event.scenePos() - event.lastScenePos()
        new_pos = self.pos() + displacement
        
        temp_circle = QGraphicsEllipseItem(self.boundingRect())
        temp_circle.setPos(new_pos)
        temp_circle.setVisible(False)

        self.scene().addItem(temp_circle)
        colliding_items = [
            item for item in temp_circle.collidingItems()
            if isinstance(item, Node) and item != self
        ]

        self.scene().removeItem(temp_circle)
        del temp_circle

        if not colliding_items:
            self.setPos(new_pos)
            self.is_moving = True
            
            self._updateArcs(new_pos)
    
    def _updateArcs(self, new_pos):
        for arc in self.arcs:
            if arc.edge.end_node != self:
                arc.setStartPoint(new_pos)
            arc.fixArc()
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.is_moving:
            print(f"[MOVED] {self}")
            self.is_moving = False
        
        return super().mouseReleaseEvent(event)

    def addArc(self, arc):
        self.arcs.append(arc)

    def __repr__(self) -> str:
        return f"Node({self.text.toPlainText()}) x: {int(self.pos().x())} y: {int(self.pos().y())}"

    def radius(self):
        return self.radius
    
    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.number == other.number            
        return False
    
    def changeColor(self, color):
        brush = QBrush(QColor(color))
        self.circle.setBrush(brush)
        self.circle.update()