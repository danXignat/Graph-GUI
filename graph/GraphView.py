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
        
        self.is__directed = is_directed
        self.nodes: dict[NodeView] = {}
        self.arcs: dict[ArcView] = {}
        
        self.arc_buffer = None

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        clicked_item = self.scene.itemAt(scene_pos, self.scene.views()[0].transform())
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
        
        return super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if self.arc_buffer is not None:
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
    
    def set_node_color(self, node_label: str, color):
        self.nodes[node_label].set_color(color)
        
    def set_node_colors(self, color = core.Qt.GlobalColor.blue):
        for node in self.nodes.values():
            node.set_color(color)
            
        for arc in self.arcs.values():
            arc.color = "blue"
            arc.update()

    

    



