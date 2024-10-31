from PySide6.QtCore import QObject, QPointF, Signal, Slot

from model import ArcModel

class ArcViewModel(QObject):
    def __init__(self, model: ArcModel):
        super().__init__()
        self.model = model
        self.setting: bool = True
    
        