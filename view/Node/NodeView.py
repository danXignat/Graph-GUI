from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPainterPath
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneMouseEvent

from config import NODE_RADIUS
from viewmodel import GraphViewModel
from .Circle import Circle
from .Text import Text

class NodeView(QGraphicsItem):
    def __init__(self, viewmodel: GraphViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.circle = Circle(NODE_RADIUS, parent=self)
        self.text = Text(self.viewmodel.label, parent=self)
        self.text.center(self.circle)
        self.is_moving = False
        
        self.setPos(self.viewmodel.model.pos)
        
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        
    #--------------------OBJECT--------------------------------   
    
    def paint(self, painter: QPainter, option, widget=None):
        pass
    
    def boundingRect(self) -> QRectF:
        return self.circle.boundingRect()
    
    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path
    
    #--------------------INPUT------------------------  
    
    def mousePressEvent(self, event):
        leftClickPressed: bool = event.button() == Qt.MouseButton.LeftButton
        rightClickPressed: bool = event.button() == Qt.MouseButton.RightButton
        
        if leftClickPressed:
            self.is_moving = True
            
        elif rightClickPressed: 
            self.viewmodel.handle_add_arc(self.viewmodel.model)
        
        return super().mousePressEvent(event)   
    
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
            if isinstance(item, NodeView) and item != self
        ]

        self.scene().removeItem(temp_circle)
        del temp_circle

        if not colliding_items:
            self.setPos(new_pos)
            self.is_moving = True
            
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.is_moving:
            self.is_moving = False
        
        return super().mouseReleaseEvent(event)