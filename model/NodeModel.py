from PySide6.QtCore import QObject, Property, QPointF, Signal

from base import BaseNode

class NodeModel(BaseNode, QObject):
    def __init__(self, label: str, pos: QPointF):
        super().__init__(label=label)
        self._pos: QPointF = pos
    
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos: QPointF):
        self._pos = pos