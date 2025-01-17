import PySide6.QtCore as core
import PySide6.QtGui as gui
import PySide6.QtWidgets as widg

from config import NODE_RADIUS
# from viewmodel import GraphViewModel
# from viewmodel import NodeViewModel
from .Circle import Circle
from .Text import Text

class NodeView(core.QObject, widg.QGraphicsItem):
    node_moving = core.Signal()
    node_deleted = core.Signal(str)
    
    def __init__(self, label: str):
        core.QObject.__init__(self)
        widg.QGraphicsItem.__init__(self)
        
        self.label = label
        self.radius = NODE_RADIUS
        self.circle = Circle(NODE_RADIUS, parent=self)
        self.text = Text(label, parent=self)
        self.text.center(self.circle)
        
        self.is_moving = False
        self.setPos(core.QPointF(0, 0))
        
        self.setAcceptHoverEvents(True)
        self.setFlag(widg.QGraphicsItem.ItemIsMovable)
        self.setFlag(widg.QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(widg.QGraphicsItem.ItemIsSelectable)
        
    #---------------------------------OBJECT-------------------------------------   
    
    def paint(self, painter: gui.QPainter, option, widget=None):
        pass
    
    def boundingRect(self) -> core.QRectF:
        return self.circle.boundingRect()
    
    def shape(self):
        path = gui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path
    
    #-----------------------------------INPUT-------------------------------------
    
    def mousePressEvent(self, event):
        leftClickPressed: bool = event.button() == core.Qt.MouseButton.LeftButton
        rightClickPressed: bool = event.button() == core.Qt.MouseButton.RightButton
        
        match event.button():
            case core.Qt.MouseButton.LeftButton:
                self.is_moving = True
                self.setCursor(core.Qt.ClosedHandCursor)
                
            case core.Qt.MouseButton.MiddleButton:
                self.node_deleted.emit(self.label)
        
        self.setScale(1.25)
        self.setZValue(10)
        
        return super().mousePressEvent(event)   

    def mouseMoveEvent(self, event):
        if self.is_moving:
            self.node_moving.emit()            

        return super().mouseMoveEvent(event)

            
    def mouseReleaseEvent(self, event: widg.QGraphicsSceneMouseEvent) -> None:
        if self.is_moving:
            self.is_moving = False
            self.unsetCursor()
        self.setScale(1)
        self.setZValue(1)
        print(self.pos())
        return super().mouseReleaseEvent(event)
    
    #-------------------------------Hover------------------------------------

    def hoverEnterEvent(self, event: widg.QGraphicsSceneHoverEvent) -> None:
        """Handle mouse hover enter events."""
        if not self.is_moving:
            self.setCursor(core.Qt.OpenHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: widg.QGraphicsSceneHoverEvent) -> None:
        """Handle mouse hover leave events."""
        if not self.is_moving:
            self.unsetCursor()
        super().hoverLeaveEvent(event)
    
    #----------------------------------Methods-----------------------------------

    def _collisionEvent(self, event):
        displacement = event.scenePos() - event.lastScenePos()
        new_pos = self.pos() + displacement
        
        temp_circle = widg.QGraphicsEllipseItem(self.boundingRect())
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
            
    def set_color(self, color):
        brush = gui.QBrush(color)
        
        self.circle.setBrush(brush)
        self.circle.update()