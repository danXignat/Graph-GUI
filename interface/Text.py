from PySide6.QtWidgets import (
    QGraphicsTextItem, QGraphicsItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui  import QFont

class Text(QGraphicsTextItem):
    def __init__(self, number: int, parent: QGraphicsItem):
        super().__init__(str(number))
        self.setParentItem(parent)

        self.setDefaultTextColor(Qt.GlobalColor.white)
        self.setFont(QFont("Times New Roman", 20))

    def center(self, object: QGraphicsItem):
        rect = self.boundingRect()
        rect.moveCenter(object.boundingRect().center())
        self.setPos(rect.topLeft())
