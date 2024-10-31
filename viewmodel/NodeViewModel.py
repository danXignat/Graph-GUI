from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QObject, Signal

from model import NodeModel


class NodeViewModel(QObject):
    node_deleted = Signal(object)
    
    def __init__(self, model: NodeModel, app: QApplication):
        super().__init__()
        self.model = model
        self.app = app

    def handle_deletion(self):
        self.node_deleted.emit(self.model)

    #---------------------------Cursor--------------------------------

    def handle_open_hand_cursor(self):
        self.app.setOverrideCursor(Qt.OpenHandCursor)

    def handle_closed_hand_cursor(self):
        self.app.setOverrideCursor(Qt.ClosedHandCursor)

    def handle_restore_cursor(self):
        self.app.restoreOverrideCursor()