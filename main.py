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
        
        self._setup_ui()
        self._setup_controllers()
    
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
        self.models = [GraphModel(), GraphModel()]
        self.views = [ GraphView(is_directed=False), GraphView(is_directed=True)]
        
        for view in self.views:
            self.stack.addWidget(view)
        
        self.controllers = [
            GraphController(model, view) 
            for model, view in zip(self.models, self.views)
        ]
        
        self.console.page_combo.currentIndexChanged.connect(self.change_page)
        self.console.page_combo.currentIndexChanged.connect(
            self.console.update_visible_fields
        )

    def change_page(self, index):
        self.stack.setCurrentIndex(index)

    def keyPressEvent(self, event: gui.QKeyEvent):
        if event.key() == core.Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

if __name__ == '__main__':
    import traceback
    import logging
    import faulthandler
    
    faulthandler.enable()

    logging.basicConfig(
        filename="app_crash.log", 
        level=logging.DEBUG, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    def message_handler(mode, context, message):
        log_message = f"{mode}: {message}"
        print(log_message)
        logging.debug(log_message)

    core.qInstallMessageHandler(message_handler)

    if not widg.QApplication.instance():
        app = widg.QApplication(sys.argv)
    else:
        app = widg.QApplication.instance()

    try:
        window = MainWindow()
        window.show()
        exit_code = app.exec()
        
        del window  # Cleanup before exit
        sys.exit(exit_code)

    except Exception as e:
        logging.error("Unhandled Exception", exc_info=True)
        print("An error occurred:", e)
        traceback.print_exc()
        sys.exit(1)
