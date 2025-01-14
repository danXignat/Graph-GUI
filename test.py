# model.py
class Person:
    def __init__(self, name=""):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


# viewmodel.py
from PySide6.QtCore import QObject, Signal

class PersonViewModel(QObject):
    nameChanged = Signal(str)

    def __init__(self, person):
        super().__init__()
        self._person = person

    @property
    def name(self):
        return self._person.name

    @name.setter
    def name(self, value):
        if value != self._person.name:
            self._person.name = value
            self.nameChanged.emit(value)

# class MovableItem(widg.QGraphicsItem):
#     def __init__(self, shape_type):
#         super().__init__()
#         self.shape_type = shape_type
#         self.setFlag(widg.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setAcceptHoverEvents(True)

#     def boundingRect(self):
#         return core.QRectF(-50, -50, 100, 100)

#     def paint(self, painter, option, widget):
#         if self.shape_type == "circle":
#             painter.setBrush(gui.QBrush(gui.QColor("red")))
#             painter.drawEllipse(-40, -40, 80, 80)
#         elif self.shape_type == "rectangle":
#             painter.setBrush(gui.QBrush(gui.QColor("blue")))
#             painter.drawRect(-40, -40, 80, 80)
#         elif self.shape_type == "triangle":
#             painter.setBrush(gui.QBrush(gui.QColor("green")))
#             points = [
#                 core.QPointF(-40, 40),
#                 core.QPointF(40, 40),
#                 core.QPointF(0, -40)
#             ]
#             painter.drawPolygon(points)

# view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

class PersonView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.init_ui()

    def init_ui(self):
        # UI Components
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        self.setLayout(layout)

        # Set initial name in the input
        self.name_input.setText(self.view_model.name)

        # Connect ViewModel to View
        self.view_model.nameChanged.connect(self.on_name_changed)

        # Connect View to ViewModel
        self.name_input.textChanged.connect(self.view_model.name_changed)

    def on_name_changed(self, value):
        # Update the input if the name changes in the ViewModel
        self.name_input.setText(value)


# main.py
import sys
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)

    # Create Model, ViewModel, and View
    person = Person("John Doe")
    view_model = PersonViewModel(person)
    view = PersonView(view_model)

    # Show the main window
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
