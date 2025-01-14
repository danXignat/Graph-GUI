import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui
import config as conf

from .BaseGraphView import BaseGraphView
from items.Node import NodeView

class GraphView(BaseGraphView):
    def __init__(self, is_directed: bool):
        super().__init__()
    
        self.is_directed = is_directed
        self.nodes = []
        self.arcs = []

    def mousePressEvent(self, event):
        leftClickPressed: bool = event.button() == core.Qt.MouseButton.LeftButton
        rightClickPressed: bool = event.button() == core.Qt.MouseButton.RightButton
        
        if leftClickPressed:
            node = NodeView("1")
            node.setPos(self.mapToScene(event.pos()))
            self.scene().addItem(node)

    



