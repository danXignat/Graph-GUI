from PySide6.QtCore import QObject, Signal, QPointF

from base import BaseGraph

class GraphModel(QObject):
    def __init__(self):
        super().__init__()

        self.graph = BaseGraph()

    def add_node():
        pass