from PySide6.QtCore import QObject, Property, QPointF, Signal

from base import BaseNode

class NodeModel(QObject):
    def __init__(self, node_data: BaseNode, pos: QPointF):
        super().__init__()
        self._node_data = node_data
        self._pos: QPointF = pos

    @property
    def label(self):
        return self._node_data.label
    
    @label.setter
    def label(self, label: str):
        self._node_data.label = label
    
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos: QPointF):
        self._pos = pos