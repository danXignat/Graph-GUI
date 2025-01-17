import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui
import config as conf
import sys

from icecream import ic
from functools import partial

from UI.ConsoleMenu import *
from graph import *

class MainWindow(widg.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(conf.WINDOW_TITLE)
        self.setWindowIcon(gui.QIcon(conf.WINDOW_ICON_PATH))
        self.resize(1920, 1080)
        
        self._setup_ui()
        self._setup_controllers()
        self._setup_connections()
    
    def _setup_ui(self):
        self.setStyleSheet("QMainWindow {background-color: #1e1e1e;}")
        
        main_widget = widg.QWidget()
        self.setCentralWidget(main_widget)
        layout = widg.QHBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.stack = widg.QStackedWidget()
        layout.addWidget(self.stack)
        
        self.console = ConsoleMenu()
        self.console.setFixedWidth(conf.MENU_WIDTH)
        layout.addWidget(self.console)
        
    def _setup_controllers(self):
        self.models = [GraphModel(is_directed=False), GraphModel(is_directed=True), GraphModel(is_directed=False)]
        self.views =  [GraphView(is_directed=False), GraphView(is_directed=True), BigGraphView()]
        
        for view in self.views:
            self.stack.addWidget(view)
        
        self.controllers = []
        for index, (model, view) in enumerate(zip(self.models, self.views)):
            if index == 2:
                self.controllers.append(BigGraphController(model, view))
            else:
                self.controllers.append(GraphController(model, view))
                
    def _setup_connections(self):
        self.console.page_combo.currentIndexChanged.connect(lambda index: self.stack.setCurrentIndex(index))
        self.console.weight_added.connect(self.add_weights_handler)
        
        
        for controller, page_group in zip(self.controllers, self.console.page_groups):
            if "algorithm" in page_group:            
                algo_group = page_group["algorithm"]
                
                algo_group["start_button"].clicked.connect(
                    lambda _, c=controller, g=algo_group: 
                        c.start_algorithm(g["selected_algo"].currentText(), g["start_node"].text())
                )
                if isinstance(controller, BigGraphController):
                    algo_group["reset_colors"].clicked.connect(
                        lambda _, c=controller, g=algo_group:
                            c.reset()
                    )
                else:               
                    algo_group["reset_colors"].clicked.connect(
                        lambda _, c=controller, g=algo_group:
                            c.view.set_node_colors()
                    )
    
    def change_algo(self, name):
        index = self.stack.currentIndex()
        self.controllers[index].current_algo = name
        
    def keyPressEvent(self, event: gui.QKeyEvent):
        match event.key() :
            case core.Qt.Key_Escape:
                self.close()
                
            case core.Qt.Key_R:
                index = self.stack.currentIndex()
                print(self.models[index])
                
            case core.Qt.Key_M:
                print(self.stack.currentIndex())

        super().keyPressEvent(event)

    def add_weights_handler(self, start_node, end_node, weight):
        index = self.stack.currentIndex()
        
        self.controllers[index].add_weight(start_node, end_node, weight)
    
if __name__ == '__main__':
    app = widg.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
