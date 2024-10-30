from PySide6.QtCore import QObject
from typing import Optional

from base import BaseArc
from .NodeModel import NodeModel

class ArcModel(BaseArc, QObject):
    def __init__(self, begin: NodeModel, end: NodeModel):
        super().__init__(begin=begin, end=end)
        