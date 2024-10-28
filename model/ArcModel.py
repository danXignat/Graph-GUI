from PySide6.QtCore import QObject
from base import BaseArc

from base import BaseArc

class ArcModel(QObject):
    def __init__(self, arc_data: BaseArc):
        super().__init__()
        
        self.arc_data = arc_data