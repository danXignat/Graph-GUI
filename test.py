from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPen, QBrush, QColor, QFont
import sys

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, number):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.setPos(x, y)
        self.radius = radius
        self.number = number
        self.adjacent_edges = []
        
        # Make node movable
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        # Set visual properties
        self.setBrush(QBrush(QColor(100, 149, 237)))  # Cornflower blue
        self.setPen(QPen(Qt.black))
        
        # Add number label
        self.label = QGraphicsTextItem(str(number), self)
        # Center the text
        text_width = self.label.boundingRect().width()
        text_height = self.label.boundingRect().height()
        self.label.setPos(-text_width/2, -text_height/2)
        self.label.setDefaultTextColor(Qt.white)
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Update connected edges when node moves
            for edge in self.adjacent_edges:
                edge.update_position()
        return super().itemChange(change, value)

    def center(self):
        return self.pos()

class EdgeItem(QGraphicsItem):
    def __init__(self, start_node, end_node=None):
        super().__init__()
        self.start_node = start_node
        self.end_node = end_node
        self.temp_end = None
        self.line_color = QColor(105, 105, 105)  # Dim gray
        
    def set_temp_end(self, point):
        self.temp_end = point
        self.update()

    def set_end_node(self, node):
        self.end_node = node
        self.temp_end = None
        self.update()

    def update_position(self):
        self.prepareGeometryChange()
        self.update()

    def boundingRect(self):
        if self.end_node:
            p1 = self.start_node.center()
            p2 = self.end_node.center()
        elif self.temp_end:
            p1 = self.start_node.center()
            p2 = self.temp_end
        else:
            return QRectF()
        
        # Create a rectangle that encompasses both points
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()
        return QRectF(min(x1, x2), min(y1, y2),
                     abs(x2 - x1), abs(y2 - y1))

    def paint(self, painter, option, widget):
        if self.end_node:
            start = self.start_node.center()
            end = self.end_node.center()
        elif self.temp_end:
            start = self.start_node.center()
            end = self.temp_end
        else:
            return

        pen = QPen(self.line_color, 2)
        painter.setPen(pen)
        painter.drawLine(start, end)

class GraphScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.temp_edge = None
        self.node_radius = 20
        self.node_counter = 1
        
        # Set scene size
        self.setSceneRect(0, 0, 800, 600)

    def mousePressEvent(self, event):
        pos = event.scenePos()
        
        # Left click: Add node
        if event.button() == Qt.LeftButton and not self.itemAt(pos, self.views()[0].transform()):
            self.add_node(pos.x(), pos.y())
            
        # Right click: Start/end edge drawing
        elif event.button() == Qt.RightButton:
            clicked_item = self.itemAt(pos, self.views()[0].transform())
            
            if isinstance(clicked_item, NodeItem) or isinstance(clicked_item, QGraphicsTextItem):
                if isinstance(clicked_item, QGraphicsTextItem):
                    clicked_item = clicked_item.parentItem()
                
                if not self.temp_edge:
                    # Start drawing edge
                    self.temp_edge = EdgeItem(clicked_item)
                    self.addItem(self.temp_edge)
                    self.temp_edge.set_temp_end(pos)
                else:
                    # Complete edge
                    if clicked_item != self.temp_edge.start_node:
                        edge = EdgeItem(self.temp_edge.start_node, clicked_item)
                        self.edges.append(edge)
                        self.addItem(edge)
                        edge.start_node.adjacent_edges.append(edge)
                        edge.end_node.adjacent_edges.append(edge)
                    
                    # Clean up temp edge
                    self.removeItem(self.temp_edge)
                    self.temp_edge = None
            else:
                # Cancel edge creation if clicking empty space
                if self.temp_edge:
                    self.removeItem(self.temp_edge)
                    self.temp_edge = None

        # Middle button: Delete node and connected edges
        elif event.button() == Qt.MiddleButton:
            clicked_item = self.itemAt(pos, self.views()[0].transform())
            if isinstance(clicked_item, NodeItem) or isinstance(clicked_item, QGraphicsTextItem):
                if isinstance(clicked_item, QGraphicsTextItem):
                    clicked_item = clicked_item.parentItem()
                self.delete_node(clicked_item)

    def mouseMoveEvent(self, event):
        if self.temp_edge:
            pos = event.scenePos()
            # Check if mouse is over a node for snapping
            item = self.itemAt(pos, self.views()[0].transform())
            if isinstance(item, NodeItem) or isinstance(item, QGraphicsTextItem):
                if isinstance(item, QGraphicsTextItem):
                    item = item.parentItem()
                if item != self.temp_edge.start_node:
                    self.temp_edge.set_temp_end(item.center())
                else:
                    self.temp_edge.set_temp_end(pos)
            else:
                self.temp_edge.set_temp_end(pos)

    def add_node(self, x, y):
        node = NodeItem(x, y, self.node_radius, self.node_counter)
        self.nodes.append(node)
        self.addItem(node)
        self.node_counter += 1

    def delete_node(self, node):
        # Remove all edges connected to this node
        edges_to_remove = node.adjacent_edges.copy()
        for edge in edges_to_remove:
            self.edges.remove(edge)
            self.removeItem(edge)
            if edge in edge.start_node.adjacent_edges:
                edge.start_node.adjacent_edges.remove(edge)
            if edge in edge.end_node.adjacent_edges:
                edge.end_node.adjacent_edges.remove(edge)
        
        # Remove the node
        self.nodes.remove(node)
        self.removeItem(node)

class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Editor")
        
        # Create and set up the graphics view
        self.view = QGraphicsView()
        self.scene = GraphScene()
        self.view.setScene(self.scene)
        
        # Set the view as the central widget
        self.setCentralWidget(self.view)
        self.resize(800, 600)

def main():
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()