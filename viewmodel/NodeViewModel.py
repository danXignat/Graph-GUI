from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from model import NodeModel

class NodeViewModel:
    def __init__(self, model: NodeModel, app: QApplication):
        self.model = model
        self.app = app

    def handle_deletion(self):
        del self.model
        del self

    #---------------------------Cursor--------------------------------

    def handle_open_hand_cursor(self):
        self.app.setOverrideCursor(Qt.OpenHandCursor)

    def handle_closed_hand_cursor(self):
        self.app.setOverrideCursor(Qt.ClosedHandCursor)

    def handle_restore_cursor(self):
        self.app.restoreOverrideCursor()