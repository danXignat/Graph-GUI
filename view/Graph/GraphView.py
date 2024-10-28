from PySide6.QtCore import QPointF, QTimer, Qt, Slot
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene, QGraphicsView
from shiboken6 import isValid


from config import WINDOW_HEIGHT, WINDOW_WEIGHT
from model import NodeModel
from viewmodel import GraphViewModel, NodeViewModel, ArcViewModel
from view import NodeView

class GraphView(QGraphicsView):
    def __init__(self, viewmodel: GraphViewModel, parent):
        super().__init__(parent=parent)
        
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        
        self.resize(WINDOW_HEIGHT, WINDOW_WEIGHT)
        self.setScene(QGraphicsScene(self))
        self.scene().setSceneRect(0, 0, self.width(), self.height())
            
        self.viewmodel = viewmodel
        self.viewmodel.added_node.connect(self.on_node_added)
        self.viewmodel.added_arc.connect(self.on_arc_added)
        
    @Slot(NodeModel)
    def on_node_added(self, model: NodeModel):
        model     = model
        viewmodel = GraphViewModel(model)
        node_view = NodeView(viewmodel)
        
        self.scene().addItem(node_view)
    
    @Slot(str)
    def on_arc_added(self):
        pass
    
    def mousePressEvent(self, event):
        leftClickPressed: bool = event.button() == Qt.MouseButton.LeftButton
        validPos: bool = self._isValidNodePos(event.position())
        node = self.getNode(event.pos())
        
        if leftClickPressed and node == None and validPos:
            self.viewmodel.handle_add_node(event.position())
            
        super().mousePressEvent(event)
    
    def getNode(self, pos: QPointF):
        item = self.itemAt(pos)

        while item is not None and not isinstance(item, NodeView):
            item = item.parentItem()

        return item if isinstance(item, NodeView) and item != self else None
    
    def _isValidNodePos(self, pos: QPointF) -> bool: 
        radius = self.node_radius
        temp_circle = QGraphicsEllipseItem(-radius, -radius, 2 * radius, 2 * radius)
        temp_circle.setPos(pos)
        temp_circle.setVisible(False)

        self.scene.addItem(temp_circle)
        colliding_items = [
            item for item in temp_circle.collidingItems()
            if isinstance(item, NodeView) and item != self
        ]
        
        self.scene.removeItem(temp_circle)
        del temp_circle
        
        return len(colliding_items) == 0