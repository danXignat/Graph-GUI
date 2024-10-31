from PySide6.QtCore import QObject, QPointF, Signal, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QMouseEvent
from typing import List

from model import GraphModel, NodeModel, ArcModel
from viewmodel import NodeViewModel, ArcViewModel
from view import NodeView, ArcView

class GraphViewModel(QObject):
    added_node = Signal(NodeView)
    added_arc = Signal(ArcView)
    counter: int = 0
    
    def __init__(self, model: GraphModel, app: QApplication):
        super().__init__()
        self.model = model
        self.app = app
        self.setting_arc: bool = False
        # self.model.added_node.connect(self.added_node)
        # self.model.added_arc.connect(self.added_arc)
        
    @Slot(NodeModel)
    def handle_delete_node(self, node: NodeModel):
        self.model.delete_node_db(node)
        
    def handle_add_node(self, pos: QPointF):
        self.counter += 1
        
        node_model     = NodeModel(label=str(self.counter), pos=pos)
        node_viewmodel = NodeViewModel(node_model, self.app)
        node_view      = NodeView(node_viewmodel)

        node_viewmodel.node_deleted.connect(self.handle_delete_node)
        
        self.model.add_node_db(node_model)
        self.added_node.emit(node_view)

    def handle_creating_arc(self, position: QPointF, start_node: NodeView):
        arc_model     = ArcModel(start_node.viewmodel.model, None)
        arc_viewmodel = ArcViewModel(arc_model)
        arc_view      = ArcView(position, arc_viewmodel)
        start_node.connected_arcs.add(arc_view)
        self.added_arc.emit(arc_view)
    
    def handle_add_arc(self, arc: ArcView, end_node: NodeView):
        arc_model =  arc.viewmodel.model 
        arc_model.end = end_node.viewmodel.model

        if self.model.add_arc_db(arc):
            end_node.connected_arcs.add(arc)
        else:
            end_node.connected_arcs.remove(arc)
    
    def handle_print_graph(self):
        print(self.model.__repr__())