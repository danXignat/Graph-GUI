from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem
from PySide6.QtCore import Qt
import sys

class CustomGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.item = None  # Initially, no item

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # Create item on left click
            self.create_item(event.pos())
        elif event.button() == Qt.RightButton:  # Delete item on right click
            self.delete_item(event.pos())

    def create_item(self, pos):
        """Creates a QGraphicsEllipseItem at the clicked position."""
        if self.item is None:
            scene_pos = self.mapToScene(pos)  # Convert view coordinates to scene coordinates
            self.item = QGraphicsEllipseItem(scene_pos.x(), scene_pos.y(), 50, 50)
            self.scene.addItem(self.item)

    def delete_item(self, pos):
        """Deletes the item if the right-click happens inside it."""
        if self.item and self.item.contains(self.mapToScene(pos)):
            self.scene.removeItem(self.item)
            del self.item
            self.item = None

# Main Application
app = QApplication(sys.argv)
view = CustomGraphicsView()
view.show()
sys.exit(app.exec())
