from PySide6.QtCore import QPointF, QTimer, Qt, Signal, Slot
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent

from config import WINDOW_HEIGHT, WINDOW_WIDTH, NODE_RADIUS

from viewmodel import GraphViewModel
from view import NodeView, ArcView
import viewmodel

class GraphView(QGraphicsView):
    def __init__(self, viewmodel: GraphViewModel, parent):
        super().__init__(parent=parent)
        
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        
        self.resize(WINDOW_HEIGHT, WINDOW_WIDTH)
        self.setScene(QGraphicsScene(self))
        self.scene().setSceneRect(0, 0, self.width(), self.height())
            
        self.viewmodel = viewmodel
        self.viewmodel.added_node.connect(self.on_node_added)
        self.viewmodel.added_arc.connect(self.on_arc_added)

        self.arc_dragging_buffer = None

    #------------------------------------SLOTS----------------------------------------

    @Slot(NodeView)
    def on_node_added(self, node_view: NodeView):
        self.scene().addItem(node_view)
    
    @Slot(ArcView)
    def on_arc_added(self, arc_view: ArcView):
        self.arc_dragging_buffer = arc_view
        self.scene().addItem(arc_view)
    
    #----------------------------------MOUSE-EVENTS-----------------------------------

    def mousePressEvent(self, event):
        leftClickPressed: bool = event.button() == Qt.MouseButton.LeftButton
        rightClickPressed: bool = event.button() == Qt.MouseButton.RightButton
        validPos: bool = self._isValidNodePos(event.position())
        node = self.getNode(event.pos())
        
        if leftClickPressed and node == None and validPos:
            self.viewmodel.handle_add_node(event.position())
            
        elif rightClickPressed:
            node = self.getNode(event.position().toPoint())

            if node and self.arc_dragging_buffer == None:
                start_point = node.mapToScene(node.boundingRect().center())
                self.viewmodel.handle_creating_arc(start_point, node)

            elif node and self.arc_dragging_buffer:
                self.viewmodel.handle_add_arc(self.arc_dragging_buffer, node)
                self.arc_dragging_buffer.fixArc(node)
                self.arc_dragging_buffer = None

            elif node == None and self.arc_dragging_buffer:
                self.arc_dragging_buffer = None

        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.arc_dragging_buffer:
            self.arc_dragging_buffer.setEndPoint(event.position())
            
        return super().mouseMoveEvent(event)
    
    #------------------------------KEYBOARD-EVENTS---------------------------------

    def keyPressEvent(self, event):
        key = str.lower(chr(event.key()))

        match key:
            case 'r':
                self.viewmodel.handle_print_graph()

        return super().keyPressEvent(event)

    #----------------------------------METHODS-----------------------------------------

    def getNode(self, pos: QPointF):
        item = self.itemAt(pos)

        while item is not None and not isinstance(item, NodeView):
            item = item.parentItem()

        return item if isinstance(item, NodeView) and item != self else None
    
    def _isValidNodePos(self, pos: QPointF) -> bool: 
        radius = NODE_RADIUS
        temp_circle = QGraphicsEllipseItem(-radius, -radius, 2 * radius, 2 * radius)
        temp_circle.setPos(pos)
        temp_circle.setVisible(False)

        self.scene().addItem(temp_circle)
        colliding_items = [
            item for item in temp_circle.collidingItems()
            if isinstance(item, NodeView) and item != self
        ]
        
        self.scene().removeItem(temp_circle)
        del temp_circle
        
        return len(colliding_items) == 0
    
