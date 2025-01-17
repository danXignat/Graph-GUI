import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui

from .BaseGraphView import BaseGraphView

from items.Node.NodeView import NodeView

class BigGraphView(BaseGraphView):
    def __init__(self):
        super().__init__()
        self.zoom_to_fit()

        self.nodes=[]
        self.arcs=[]
    def zoom_to_fit(self):
        self.current_zoom = self.min_zoom
        self.resetTransform()
        self.scale(self.min_zoom, self.min_zoom)
        self.centerOn(0, 0)
    
    