from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox
)


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Dialog")

        # Layouts
        layout = QVBoxLayout(self)

        # Input for first value
        self.label1 = QLabel("Enter first value:")
        self.input1 = QLineEdit(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.input1)

        # Input for second value
        self.label2 = QLabel("Enter second value:")
        self.input2 = QLineEdit(self)
        layout.addWidget(self.label2)
        layout.addWidget(self.input2)

        # OK and Cancel buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def get_inputs(self):
        return self.input1.text(), self.input2.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        # Button to open dialog
        self.button = QPushButton("Open Input Dialog")
        self.button.clicked.connect(self.open_dialog)

        self.setCentralWidget(self.button)

    def open_dialog(self):
        dialog = InputDialog(self)
        if dialog.exec():  # If the dialog is accepted
            value1, value2 = dialog.get_inputs()
            print(f"Value 1: {value1}, Value 2: {value2}")
        else:
            print("Dialog canceled.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
