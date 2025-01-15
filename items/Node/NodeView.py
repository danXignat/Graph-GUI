from typing import Optional, Set

import PySide6.QtCore as core
import PySide6.QtGui as gui
import PySide6.QtWidgets as widg

from config import NODE_RADIUS

class NodeView(core.QObject, widg.QGraphicsItem):
    node_moving = core.Signal()
    node_deleted = core.Signal(str)
    
    def __init__(self, label: str):
        """Initialize a new NodeView."""
        core.QObject.__init__(self)
        widg.QGraphicsItem.__init__(self)
        
        self.radius: float = NODE_RADIUS
        self.label: str = label
        self.is_moving: bool = False
        
        self._setup_visuals()
        self._setup_interaction_flags()
    
    def _setup_visuals(self) -> None:
        self.setPos(core.QPointF(0, 0))
        self.setZValue(1)
        self.setCacheMode(widg.QGraphicsItem.DeviceCoordinateCache)
        
    def _setup_interaction_flags(self) -> None:
        """Set up the interaction flags for the node."""
        self.setAcceptHoverEvents(True)
        self.setFlag(widg.QGraphicsItem.ItemIsMovable)
        self.setFlag(widg.QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(widg.QGraphicsItem.ItemIsSelectable)
        
    def paint(self, painter: gui.QPainter, option, widget=None) -> None:
        """Paint the circle and the text with an inward border."""
        # Define pen width
        pen_width = 3

        bounding_rect = self.boundingRect()
        inward_rect = bounding_rect.adjusted(pen_width / 2, pen_width / 2, -pen_width / 2, -pen_width / 2)

        painter.setBrush(gui.QBrush(core.Qt.blue))
        painter.setPen(gui.QPen(core.Qt.white, 3))
        painter.drawEllipse(inward_rect)

        font = painter.font()
        font.setFamily("Times New Roman")  # Set the font family
        font.setPointSize(22)  # Set the font size (adjust as needed)
        font.setBold(True)  # Make the text bold
        painter.setFont(font)  # Apply the font to the painter

        painter.setPen(core.Qt.white)  # Set text color
        painter.drawText(
            bounding_rect,
            core.Qt.AlignCenter,
            str(self.label)
        )
    
    def boundingRect(self) -> core.QRectF:
        """Define the bounding rectangle for the item."""
        diameter = self.radius * 2
        return core.QRectF(
            -self.radius,
            -self.radius,
            diameter,
            diameter,
        )
    
    def shape(self) -> gui.QPainterPath:
        path = gui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def mousePressEvent(self, event: widg.QGraphicsSceneMouseEvent) -> None:
        """Handle mouse press events."""
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.is_moving = True
            self.setCursor(core.Qt.ClosedHandCursor)
        elif event.button() == core.Qt.MouseButton.MiddleButton:
            self._handle_deletion()
        
        self.setScale(1.25)
        self.setZValue(10)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: widg.QGraphicsSceneMouseEvent) -> None:
        """Handle mouse release events."""
        if self.is_moving:
            self.is_moving = False
            self.unsetCursor()
            
        self.setScale(1)
        self.setZValue(1)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: widg.QGraphicsSceneMouseEvent) -> None:
        """Handle mouse move events."""
        self.node_moving.emit()
        
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: widg.QGraphicsSceneMouseEvent) -> None:
        """Handle double-click events."""
        if event.button() == core.Qt.MouseButton.RightButton:
            pass
        else:
            super().mouseDoubleClickEvent(event)

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

    def _handle_deletion(self) -> None:
        """Handle the deletion of this node."""
        self.node_deleted.emit(self.label)
