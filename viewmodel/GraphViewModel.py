from PySide6.QtCore import QObject, QPointF, Signal, Slot
from PySide6.QtWidgets import QApplication
from typing import List

from model import GraphModel, NodeModel, ArcModel
from viewmodel import NodeViewModel
from view import NodeView, ArcView

class GraphViewModel(QObject):
    added_node = Signal(NodeView)
    added_arc = Signal(ArcView)
    counter: int = 0
    
    def __init__(self, model: GraphModel, app: QApplication):
        super().__init__()
        self.model = model
        self.app = app
        # self.model.added_node.connect(self.added_node)
        # self.model.added_arc.connect(self.added_arc)
        
    def handle_add_node(self, pos: QPointF):
        self.counter += 1
        node_model = NodeModel(label=str(self.counter), pos=pos)
        node_viewmodel = NodeViewModel(node_model, self.app)
        node_view = NodeView(node_viewmodel)

        self.model.add_node_db(node_model)
        self.added_node.emit(node_view)

    def handle_add_arc(self, node: NodeModel):
       pass
    
    def handle_print_graph(self):
        print(self.model.__repr__())