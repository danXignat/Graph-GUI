from PySide6.QtCore import QObject, QPointF, Signal, Slot
from typing import List

from model import GraphModel, NodeModel, ArcModel

class GraphViewModel(QObject):
    added_node = Signal(NodeModel)
    added_arc = Signal(ArcModel)
    counter: int = 0
    nodes_for_arc_buffer: List[NodeModel] = []
    
    def __init__(self, model: GraphModel):
        super().__init__()
        self.model = model
        self.model.added_node.connect(self.added_node)
        self.model.added_arc.connect(self.added_arc)
        
    def handle_add_node(self, pos: QPointF):
        self.counter += 1
        label = str(self.counter)
        self.model.add_node(label, pos)
        
    def handle_add_arc(self, node: NodeModel):
        self.nodes_for_arc_buffer.append(node)
        if len(self.nodes_for_arc_buffer) == 2:
            self.model.add_arc(
                self.nodes_for_arc_buffer[0],
                self.nodes_for_arc_buffer[1]
            )
            self.nodes_for_arc_buffer.clear()
        