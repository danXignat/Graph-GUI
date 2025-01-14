import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui
import config as conf

class FieldGroup(widg.QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("fieldGroup")
        
        layout = widg.QVBoxLayout(self)
        layout.setSpacing(10)
        
        title_label = widg.QLabel(title)
        title_label.setObjectName("groupTitle")
        title_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        self.inner_layout = widg.QFormLayout()
        self.inner_layout.setSpacing(8)
        layout.addLayout(self.inner_layout)
        
    def add_field(self, label, widget):
        label_widget = widg.QLabel(label)
        label_widget.setObjectName("fieldLabel")
        widget.setObjectName("fieldInput")

        if hasattr(widget, 'setAlignment'):
            widget.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.inner_layout.addRow(label_widget, widget)
        self.inner_layout.setAlignment(widget, core.Qt.AlignmentFlag.AlignRight)

class ConsoleMenu(widg.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("consoleMenu")
        
        self.main_layout = widg.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 15, 10, 15)
        self.main_layout.setSpacing(15)
        
        # Page selection
        page_group = FieldGroup("View Selection")
        self.page_combo = widg.QComboBox()
        self.page_combo.addItems(["Directed graph", "Undirected graph"])
        page_group.add_field("Current view:", self.page_combo)
        self.main_layout.addWidget(page_group)

        # Shape-specific fields
        self.circle_group = FieldGroup("Circle Properties")
        self.circle_radius = widg.QSpinBox()
        self.circle_radius.setRange(10, 100)
        self.circle_group.add_field("Radius:", self.circle_radius)
        self.main_layout.addWidget(self.circle_group)

        self.rectangle_group = FieldGroup("Rectangle Properties")
        self.rect_width = widg.QSpinBox()
        self.rect_height = widg.QSpinBox()
        self.rect_width.setRange(10, 200)
        self.rect_height.setRange(10, 200)
        self.rectangle_group.add_field("Width:", self.rect_width)
        self.rectangle_group.add_field("Height:", self.rect_height)
        self.main_layout.addWidget(self.rectangle_group)

        self.triangle_group = FieldGroup("Triangle Properties")
        self.triangle_size = widg.QSpinBox()
        self.triangle_rotation = widg.QSpinBox()
        self.triangle_size.setRange(10, 150)
        self.triangle_rotation.setRange(0, 360)
        self.triangle_group.add_field("Size:", self.triangle_size)
        self.triangle_group.add_field("Rotation:", self.triangle_rotation)
        self.main_layout.addWidget(self.triangle_group)

        self.main_layout.addStretch()

        self.update_visible_fields(0)
        
        with open("CSS/menu_style.css", 'r') as file:
            content = file.read()

        self.setStyleSheet(content)

    def update_visible_fields(self, index):
        self.circle_group.hide()
        self.rectangle_group.hide()
        self.triangle_group.hide()
        
        if index == 0:
            self.circle_group.show()
        elif index == 1:
            self.rectangle_group.show()
        
