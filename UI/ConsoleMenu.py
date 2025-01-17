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

class InputDialog(widg.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add weight on arc")

        layout = widg.QVBoxLayout(self)

        self.label1 = widg.QLabel("Start node:")
        self.input1 = widg.QLineEdit(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.input1)

        self.label2 = widg.QLabel("End node:")
        self.input2 = widg.QLineEdit(self)
        layout.addWidget(self.label2)
        layout.addWidget(self.input2)

        self.label3 = widg.QLabel("Weight:")
        self.input3 = widg.QLineEdit(self)
        layout.addWidget(self.label3)
        layout.addWidget(self.input3)
        
        self.buttonBox = widg.QDialogButtonBox(widg.QDialogButtonBox.Ok | widg.QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def get_inputs(self):
        return self.input1.text(), self.input2.text(), self.input3.text()

class ConsoleMenu(widg.QFrame):
    weight_added = core.Signal(str, str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setObjectName("consoleMenu")
        
        self.main_layout = widg.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 15, 10, 15)
        self.main_layout.setSpacing(15)
        
        self.create_page_selection()
        
        self.page_groups = [{}, {}, {}]
        
        self.create_algo_selection(0, ["DFS", "BFS", "Connected components", "Deforestation", "Rooting tree"])
        self.create_algo_selection(1, ["DFS", "BFS", "Connected components","Strongly components", "Topological sort", "Kruskal", "Boruvka"])
        self.create_algo_selection(2, ["Dijkstra", "Bellman Ford"])
        
        self.create_add_weight(0)
        self.create_add_weight(1)
        
        self.main_layout.addStretch()

        self.update_visible_fields(0)
        
        self.load_style()

    def create_page_selection(self):
        page_group = FieldGroup("View Selection")
        self.page_combo = widg.QComboBox()
        self.page_combo.addItems(["Undirected graph", "Directed graph", "Big graph"])
        page_group.add_field("Current view:", self.page_combo)
        self.main_layout.addWidget(page_group)
        
        self.page_combo.currentIndexChanged.connect(self.update_visible_fields)
        
    def create_algo_selection(self, page_index: int, algorithms: list):
        group = FieldGroup("Algorithm Selection")
        combo = widg.QComboBox()
        combo.setPlaceholderText("None")
        button = widg.QPushButton("START")
        button_reset_colors = widg.QPushButton("RESET COLORS")
        start = widg.QLineEdit()
        start.setPlaceholderText("Start node")
        combo.addItems(algorithms)
        group.add_field("Type:", combo)
        group.add_field("", start)
        group.add_field("", button)
        group.add_field("", button_reset_colors)
        
        self.main_layout.addWidget(group)
        
        group_widgets = {
            "field_group"  : group,
            "selected_algo": combo,
            "start_node"   : start,
            "start_button" : button,
            "reset_colors" : button_reset_colors,
        }
        
        self.page_groups[page_index]["algorithm"] = group_widgets
        
    def create_add_weight(self, page_index: int):
        group = FieldGroup("Add weights")
        button = widg.QPushButton("ADD")
        button.clicked.connect(self.open_dialog)   
        group.add_field("", button)
        
        self.main_layout.addWidget(group)         
        
        group_widgets = {
            "field_group"  : group,
            "add_weights_button" : button,
        }
        
        self.page_groups[page_index]["weights"] = group_widgets
        
    def load_style(self):
        with open("CSS/menu_style.css", 'r') as file:
            content = file.read()

        self.setStyleSheet(content)
    
    def update_visible_fields(self, index):
        for page_group in self.page_groups:
            for group in page_group.values():
                group["field_group"].hide()
                
        for group in self.page_groups[index].values():
            group["field_group"].show()
            
    def open_dialog(self):
        dialog = InputDialog(self)
        if dialog.exec(): 
            value1, value2, value3 = dialog.get_inputs()
            self.weight_added.emit(value1, value2, value3)
        else:
            print("Dialog canceled.")
        
        
