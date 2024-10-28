from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import QMainWindow, QApplication

from model import GraphModel
from viewmodel import GraphViewModel
from view import GraphView

from config import (
    WINDOW_ICON_PATH, WINDOW_TITLE,
    WINDOW_WEIGHT, WINDOW_HEIGHT
)

import sys

class MainWindow(QMainWindow):
    def __init__(self, witdh: float, height: float):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(WINDOW_ICON_PATH))      
        self.resize(WINDOW_HEIGHT, WINDOW_WEIGHT)
        
        #MVVM arhitecture
        graph_model = GraphModel()
        graph_viewmodel = GraphViewModel(graph_model)
        graph_view = GraphView(graph_viewmodel, parent=self)
        graph_view.show()
        

if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow(1200, 800)
    window.show()
    
    sys.exit(app.exec())
    
