from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QPainter, QPainterPath, QCursor
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent

from config import NODE_RADIUS
# from viewmodel import GraphViewModel
# from viewmodel import NodeViewModel
from .Circle import Circle
from .Text import Text

class NodeView(QGraphicsItem):
    def __init__(self, label: str):
        super().__init__()
        self.radius = NODE_RADIUS
        circle = Circle(NODE_RADIUS, parent=self)
        text = Text(label, parent=self)
        text.center(circle)
        
        self.is_moving = False
        self.setPos(QPointF(0, 0))
        
        self.setZValue(1)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.connected_arcs = set()
        
    #---------------------------------OBJECT-------------------------------------   
    
    def paint(self, painter: QPainter, option, widget=None):
        pass
    
    def boundingRect(self) -> QRectF:
        return self.circle.boundingRect()
    
    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path
    
    #-----------------------------------INPUT-------------------------------------
    
    def mousePressEvent(self, event):
        leftClickPressed: bool = event.button() == Qt.MouseButton.LeftButton
        rightClickPressed: bool = event.button() == Qt.MouseButton.RightButton
        
        if leftClickPressed:
            self.is_moving = True
        
        return super().mousePressEvent(event)   

    def mouseDoubleClickEvent(self, event):
        rightClickPressed : bool = event.button() == Qt.MouseButton.RightButton

        if rightClickPressed:
            self.scene().removeItem(self)
            self.viewmodel.handle_deletion()
            self.viewmodel.handle_restore_cursor()
            del self
        else:
            return super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_moving:
            self._collisionEvent(event)

            self._updateArc()

        return super().mouseMoveEvent(event)

        
            
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.is_moving:
            self.is_moving = False
            self.viewmodel.handle_restore_cursor()
        
        return super().mouseReleaseEvent(event)
    
    #-------------------------------Hover------------------------------------

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.viewmodel.handle_open_hand_cursor()
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.viewmodel.handle_restore_cursor()
        return super().hoverEnterEvent(event)
    
    #----------------------------------Methods-----------------------------------

    def _collisionEvent(self, event):
        displacement = event.scenePos() - event.lastScenePos()
        new_pos = self.pos() + displacement
        
        temp_circle = QGraphicsEllipseItem(self.boundingRect())
        temp_circle.setPos(new_pos)
        temp_circle.setVisible(False)

        self.scene().addItem(temp_circle)
        colliding_items = [
            item for item in temp_circle.collidingItems()
            if isinstance(item, NodeView) and item != self
        ]

        self.scene().removeItem(temp_circle)
        del temp_circle

        if not colliding_items:
            self.setPos(new_pos)
            self.is_moving = True

    def _updateArc(self):
        for arc in self.connected_arcs:
            arc.update()

    