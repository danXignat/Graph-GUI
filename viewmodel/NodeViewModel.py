from PySide6.QtCore import Property

from model import NodeModel

class NodeViewModel:
    def __init__(self, model = NodeModel):
        self.model = model
        
    @property
    def label(self):
        return self.model.label