import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui

from test import QPointF

from .BigGraphView import BigGraphView
from .GraphModel import GraphModel

from utils.big_map import get_arc_data, get_node_data

class SimpleNode(core.QObject, widg.QGraphicsItem):
    node_selected = core.Signal(str)
    
    def __init__(self, pos, radius, label, color = "blue", parent=None):
        core.QObject.__init__(self)
        widg.QGraphicsItem.__init__(self)
        
        self.radius = radius
        self.label = label
        self.setPos(pos)
                
        self.color = color
        self.update()
        self.setFlag(widg.QGraphicsItem.ItemIsSelectable)
    
    def mousePressEvent(self, event):
        if event.button() == event.button() == core.Qt.MouseButton.LeftButton:
            self.node_selected.emit(self.label)
        
        return super().mousePressEvent(event)
        
    def boundingRect(self):
        return core.QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter, option, widget):
        painter.setBrush(gui.QBrush(self.color))
        painter.setPen(gui.QPen(self.color))
        painter.drawEllipse(core.QPointF(0, 0), self.radius, self.radius)

class SimpleEdge(widg.QGraphicsItem):
    def __init__(self, p1: QPointF, p2: QPointF, length: float, color: gui.QColor = gui.QColor("#90EE90"), parent=None):
        super().__init__(parent)
        self.p1 = p1
        self.p2 = p2
        self.length = length
        
        self.color = color        
        self.update()
        
    def boundingRect(self):
        p1 = self.p1
        p2 = self.p2

        rect = core.QRectF(min(p1.x(), p2.x()), min(p1.y(), p2.y()), 
                    abs(p2.x() - p1.x()), abs(p2.y() - p1.y()))
        
        return rect
    
    def paint(self, painter, option, widget):
        painter.setPen(gui.QPen(self.color))
        painter.drawLine(self.p1, self.p2)
    
    
class BigGraphController(core.QObject):
    def __init__(self, model: GraphModel, view: BigGraphView):
        super().__init__()
        
        self.model = model
        self.view = view
        
        self.draw_nodes()
        self.draw_arcs()
        
        self.nodes_buffer = []
        self.algo_generator = None
        self.color_timer = core.QTimer()
        self.color_timer.timeout.connect(lambda : None)
        
        self.start_node=None
        self.end_node =None
        
    def draw_nodes(self):
        for node_id, pos in get_node_data():
            node = SimpleNode(pos, 5, node_id)
            node.setZValue(10)
            node.node_selected.connect(self.on_node_selected)
            self.model.add_node(node_id, QPointF(0, 0))
            self.view.nodes.append(node)
            self.view.scene.addItem(node)
            
    def draw_arcs(self):
        for (arc_from, arc_to), length in get_arc_data():
            edge = SimpleEdge(
                self.view.nodes[int(arc_from)].pos(),
                self.view.nodes[int(arc_to)].pos(),
                int(length)
            )
            
            self.model.add_arc(arc_from, arc_to, int(length))
            self.view.arcs.append(edge)
            self.view.scene.addItem(edge)
    
    @core.Slot(str)
    def on_node_selected(self, node_label):
        if self.start_node == None:
            self.start_node = node_label
            self.view.nodes[int(node_label)].radius = 20
            self.view.nodes[int(node_label)].color = "green"
            self.view.nodes[int(node_label)].setZValue(11)
            self.view.nodes[int(node_label)].update()
            print("Selected first", node_label)
            
        elif self.end_node == None:
            self.end_node = node_label
            self.view.nodes[int(node_label)].radius = 20
            self.view.nodes[int(node_label)].color = "green"
            self.view.nodes[int(node_label)].setZValue(11)
            self.view.nodes[int(node_label)].update()
            print("Selected second", node_label)
            
        else:
            pass
    
    def color_next_node(self):
        try:
            step = next(self.algo_generator)
            
            if isinstance(step, set):
                print(step)
                
                for node_label in self.nodes_buffer:
                    node = self.view.nodes[int(node_label)]
                    
                    if node.label not in step:
                        node.color = "blue"   
                        node.update()
            else:
                next_node, _ = step
                
                if next_node != self.start_node and next_node != self.end_node:
                    self.nodes_buffer.append(next_node)
                    self.view.nodes[int(next_node)].color = "red"
                
                self.view.nodes[int(next_node)].update()
            
        except StopIteration:
            self.color_timer.stop()
            self.algo_generator = None
    
    @core.Slot(str, str)        
    def start_algorithm(self, algo_name, start_label):
        if self.start_node == None or self.end_node == None:
            return
        
        print(algo_name if algo_name is not None else "None", start_label)
        self.color_timer.timeout.disconnect()

        match algo_name:
            case "Dijkstra" |  "Bellman Ford":             
                self.color_timer.timeout.connect(self.color_next_node)
            
            case _:
                pass

        self.algo_generator = self.model.generate_from_algorithm(algo_name, self.start_node, self.end_node)        
        self.color_timer.start(0.01)
            
            
    def reset(self):
        for node_label in self.nodes_buffer:
            node = self.view.nodes[int(node_label)]
            
            node.color = "blue"
            node.update()
            
        start_node = self.view.nodes[int(self.start_node)]
        start_node.radius = 5
        start_node.color = "blue"
        start_node.update()
        self.start_node = None
        
        end_node = self.view.nodes[int(self.end_node)]
        end_node.radius = 5
        end_node.color = "blue"
        end_node.update()
        self.end_node = None