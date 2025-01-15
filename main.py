# from PySide6.QtGui import QIcon, QPainter
# from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QWidget, QLabel, QVBoxLayout, QComboBox, QGraphicsView, QGraphicsScene, QMainWindow, QGraphicsProxyWidget
# from PySide6.QtCore import Qt, QPointF

# from model import GraphModel
# from viewmodel import GraphViewModel
# from view import GraphView
# from UI.graph import GraphInfoWidget

# from config import (
#     WINDOW_ICON_PATH, WINDOW_TITLE,
#     WINDOW_WIDTH, WINDOW_HEIGHT
# )

# import sys

# class MainWindow(QMainWindow):
#     def __init__(self, witdh: float, height: float, app: QApplication):
#         super().__init__()
#         self.setWindowTitle(WINDOW_TITLE)
#         self.setWindowIcon(QIcon(WINDOW_ICON_PATH))      
#         self.resize(witdh, height)
        
        
#         main_widget = QWidget()
#         main_layout = QHBoxLayout(main_widget)
#         self.setCentralWidget(main_widget)

#         main_layout = QHBoxLayout()
#         main_widget.setLayout(main_layout)

#         graph_model = GraphModel()
#         graph_viewmodel = GraphViewModel(graph_model, app)
#         self.graph_view = GraphView(graph_viewmodel, parent=self)
#         main_layout.addWidget(self.graph_view)
        
#         self.graph_info_widget = GraphInfoWidget("Graph", WINDOW_WIDTH / 4, WINDOW_HEIGHT * 0.5)
#         self.graph_info_widget.setParent(self) 
#         self.graph_info_widget.move(WINDOW_WIDTH * 0.9, 10)
#         self.graph_info_widget.show()


import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui
import config as conf
import sys

from UI.ConsoleMenu import *
from graph import *

class MainWindow(widg.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(conf.WINDOW_TITLE)
        self.setWindowIcon(gui.QIcon(conf.WINDOW_ICON_PATH))
        self.resize(conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT)
        
        self.setStyleSheet("QMainWindow {background-color: #1e1e1e;}")
        
        main_widget = widg.QWidget()
        self.setCentralWidget(main_widget)
        layout = widg.QHBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.stack = widg.QStackedWidget()
        self.__init_controllers()
        
        for view in self.views:
            self.stack.addWidget(view)

        layout.addWidget(self.stack)
        
        self.console = ConsoleMenu()
        self.console.setFixedWidth(conf.MENU_WIDTH)
        self.console.page_combo.currentIndexChanged.connect(self.change_page)
        self.console.page_combo.currentIndexChanged.connect(self.console.update_visible_fields)
        layout.addWidget(self.console)
        

    def change_page(self, index):
        self.stack.setCurrentIndex(index)

    def keyPressEvent(self, event: gui.QKeyEvent):
        if event.key() == core.Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)
        
    def __init_controllers(self):
        self.models = [
            GraphModel(),
            GraphModel()
        ]
        
        self.views = [
            GraphView(is_directed=False),
            GraphView(is_directed=True),
        ]
        
        self.controllers = [GraphController(model, view) for model, view in zip(self.models, self.views)]
        

if __name__ == '__main__':
    app = widg.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())