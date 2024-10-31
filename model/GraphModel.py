from PySide6.QtCore import QObject, Signal, QPointF

from base import BaseGraph

from .NodeModel import NodeModel
from .ArcModel import ArcModel

class CommonMeta(type(QObject), type(BaseGraph)):
    pass

class GraphModel(BaseGraph, QObject, metaclass = CommonMeta):
    def __init__(self):
        super().__init__()

    def add_node_db(self, node: NodeModel):
        self.add_node(node)
        print(f"[ADDED] {node}")
        
    def delete_node_db(self, node: NodeModel):
        self.delete_node(node)
        print(f"[DELETED] {node}")