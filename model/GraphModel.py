from PySide6.QtCore import QObject, Signal, QPointF

from base import BaseGraph, BaseArc, BaseNode

from .NodeModel import NodeModel
from .ArcModel import ArcModel

class GraphModel(QObject):
    added_node = Signal(NodeModel)    
    added_arc = Signal(ArcModel)
    
    def __init__(self):
        super().__init__()
        self.graph_data = BaseGraph()
        
    def add_node(self, label: str, pos: QPointF):
        node_data = BaseNode(label)
        print(node_data)
        self.graph_data.add_node(node_data)
        self.added_node.emit(NodeModel(node_data, pos))
    
    def add_arc(self, begin_node: NodeModel, end_node: NodeModel):
        arc_data = BaseArc(begin_node._node_data, end_node._node_data)
        self.graph_data.add_arc(arc_data)
        self.added_arc.emit(ArcModel(arc_data))