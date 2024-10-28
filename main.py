from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,QInputDialog,
    QMessageBox
)
from PySide6.QtCore import Qt, QPointF, QTimer
from PySide6.QtGui  import QColor, QPainter, QIcon

import sys
import time

from interface.Node import Node
from interface.Arc import Arc, QBrush
from graph.BaseGraph import BaseGraph

class GraphView(QGraphicsView, BaseGraph):
    def __init__(self):
        super().__init__()
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        
        self.node_counter = 0
        self.node_radius = 20.0
        
        self.current_arc = None
        
    def getNode(self, pos: QPointF):
        item = self.itemAt(pos.toPoint())

        while item is not None and not isinstance(item, Node):
            item = item.parentItem()

        return item if isinstance(item, Node) and item != self else None

    def _isValidNodePos(self, pos: QPointF) -> bool: 
        radius = self.node_radius
        temp_circle = QGraphicsEllipseItem(-radius, -radius, 2 * radius, 2 * radius)
        temp_circle.setPos(pos)
        temp_circle.setVisible(False)

        self.scene.addItem(temp_circle)
        colliding_items = [
            item for item in temp_circle.collidingItems()
            if isinstance(item, Node) and item != self
        ]
        
        self.scene.removeItem(temp_circle)
        del temp_circle
        
        return len(colliding_items) == 0
    
    def mousePressEvent(self, event)-> None: 
        leftClickPressed: bool = event.button() == Qt.MouseButton.LeftButton
        rightClickPressed: bool = event.button() == Qt.MouseButton.RightButton
        nodeExist: bool  = True if self.getNode(event.position()) else False
        validPos: bool = self._isValidNodePos(event.position())
        
        if leftClickPressed and not nodeExist and validPos:
            self.node_counter += 1
            r = self.node_radius
            scene_pos = self.mapToScene(event.position().toPoint())
            
            node = Node(radius=r, pos=scene_pos, number=self.node_counter, app=app)
            print(f"[CREATED] {node}")

            collided_nodes = [
                existing_node for existing_node in self.scene.items()
                if isinstance(existing_node, Node) if node.collidesWithItem(existing_node)
            ]
            
            self.addNode(node)
            self.scene.addItem(node)
            
        elif rightClickPressed:
            node = self.getNode(event.position())
            if node == None:
                return super().mousePressEvent(event)
            
            start_point = node.mapToScene(node.boundingRect().center())
            self.current_arc = Arc(start_point, start_point)
            self.current_arc.setStartNode(node)
            
            self.scene.addItem(self.current_arc)
            
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.current_arc:
            end_point = event.position()
            
            self.current_arc.setEndPoint(end_point)
        
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.current_arc:
            self.current_arc.setVisible(False)
            node = self.getNode(self.current_arc.getArrowPoint())
            
            if node:
                self.current_arc.setEndNode(node)
                self.current_arc.fixArc()
                
                initial_node = self.current_arc.edge.start_node
                initial_node.addArc(self.current_arc)
                node.addArc(self.current_arc)
                self.addEdge(self.current_arc.edge.as_tuple())
                
                self.current_arc.setVisible(True)
            else:
                self.scene.removeItem(self.current_arc)
            
            self.current_arc = None
        
        return super().mouseReleaseEvent(event)
    
    def __repr__(self):
        return BaseGraph.__repr__(self)
    
    def keyPressEvent(self, event):
        key = event.key()
        if key == ord('D'):
            number, ok = QInputDialog.getInt(self, "DFS", "Please enter a valid node index to start:")
            if ok:
                QMessageBox.information(self, "Index you entered", f"You entered: {number}")
            
            start_node = next((node for node in self.nodes if node.number == number), None)   
            if start_node:
                nodes = self.dfs(start_node)
                
                print(nodes)
                
                def change_circle_colors(index=0):
                    if index < len(nodes):
                        nodes[index].changeColor("green")
                        QTimer.singleShot(1000, lambda: change_circle_colors(index + 1))
                        nodes[index].changeColor("red")

                    elif index == len(nodes):
                        for node in nodes:
                            node.changeColor("green")
            
                QTimer.singleShot(1000, lambda: change_circle_colors(0))
            
        elif key == ord('B'):
            number, ok = QInputDialog.getInt(self, "BFS", "Please enter a valid node index to start:")
            if ok:
                QMessageBox.information(self, "Index you entered", f"You entered: {number}")
            
            start_node = next((node for node in self.nodes if node.number == number), None)   
            if start_node:
                nodes = self.bfs(start_node)
                
                print(nodes)
                
                def change_circle_colors(index=0):
                    if index < len(nodes):
                        nodes[index].changeColor("green")
                        QTimer.singleShot(1000, lambda: change_circle_colors(index + 1))
                        nodes[index].changeColor("green")

                    elif index == len(nodes):
                        for node in nodes:
                            node.changeColor("green")
            
                QTimer.singleShot(1000, lambda: change_circle_colors(0))
                
        elif key == ord('R'):
            print(self)
        else:
            return super().keyPressEvent(event)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QIcon("static/graph_icon.png")
    
    view = GraphView()
    view.setWindowTitle("Algoritmica Grafurilor")
    view.setWindowIcon(icon)
    view.resize(1200, 600)
    
    view.show()
    
    sys.exit(app.exec())