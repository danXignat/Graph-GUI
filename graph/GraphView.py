import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui
import config as conf
from items.Arc import ArcView

from .BaseGraphView import BaseGraphView
from items.Node import NodeView

class GraphView(BaseGraphView):
    node_added         = core.Signal(core.QPointF)
    node_deleted       = core.Signal(str)
    arc_added          = core.Signal((str, str))
    arc_deleted        = core.Signal((str, str))
    arc_creation_start = core.Signal(NodeView)
    arc_creation_end   = core.Signal(NodeView)
    
    def __init__(self, is_directed: bool):
        super().__init__()
        
        self.is_directed = is_directed
        self.nodes: list[NodeView] = []
        self.arcs: list[ArcView] = []
        
        self.arc_buffer = None

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        node = self.get_node(scene_pos)
        
        leftClickPressed: bool = event.button() == core.Qt.MouseButton.LeftButton
        rightClickPressed: bool = event.button() == core.Qt.MouseButton.RightButton
        
        if leftClickPressed and self.is_valid_node_pos(scene_pos):
            self.node_added.emit(scene_pos)
            
        elif rightClickPressed:
            if self.arc_buffer is None:
                self.arc_creation_start.emit(node)
            else:
                self.arc_creation_end.emit(node)
                
        print()
        for item in self.scene.items():
            print(item)
            print("miau" if self.arc_buffer is not None else "NONE")
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.arc_buffer and self.arc_buffer in self.scene.items():
            scene_pos = self.mapToScene(event.pos())
            self.arc_buffer.setEndPoint(scene_pos)
        
        return super().mouseMoveEvent(event)
    
    def get_node(self, pos: core.QPointF):
        items = self.scene.items(pos)
        
        for item in items:
            if isinstance(item, NodeView):
                return item
            
        return None
    
    def is_valid_node_pos(self, pos: core.QPointF) -> bool: 
        radius = conf.NODE_RADIUS
        temp_circle = widg.QGraphicsEllipseItem(-radius, -radius, 2 * radius, 2 * radius)
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
            
                
    

    



