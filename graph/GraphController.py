import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui
import random

from .GraphModel import *
from .GraphView import GraphView
from items.Node import NodeView
from items.Arc import ArcView, EdgeView
import graph.helpers as helper
import utils
from config import ROOT_POS, WIDTH_TREE_OFFSEET, HEIGHT_TREE_OFFSET

class GraphController(core.QObject):
    def __init__(self, model: GraphModel, view: GraphView):
        super().__init__()
        self.view = view
        self.model = model
        self.node_counter = 0
        self.current_algo = None
        
        self.algo_generator = None
        self.color_timer = core.QTimer()
        self.color_timer.timeout.connect(lambda : None)
        self.rooting = False
        self.current_tree_index = 0
        self.new_node_color = utils.get_random_color()
        
        self.view.node_added.connect(self.on_create_node)
        self.view.arc_creation_start.connect(self.onArcCreationStart)
        self.view.arc_creation_end.connect(self.onArcCreationEnd)
    
    @core.Slot(core.QPointF)
    def on_create_node(self, scene_pos: core.QPointF):
        label = str(self.node_counter + 1)
        self.node_counter += 1
        
        node = NodeView(label)
        node.setPos(scene_pos)
        node.node_moving.connect(self.on_node_moving)
        node.node_deleted.connect(self.on_node_deleted)
            
        self.view.nodes[label] = node
        self.view.scene.addItem(node)
        
        self.model.add_node(label, scene_pos)
        print(f"Node {label} created successfully")
        
    @core.Slot(str)            
    def on_node_deleted(self, node_label):
        deleted_node = self.view.nodes[node_label]
        
        arcs_to_remove = {
            labels: arc for labels, arc in self.view.arcs.items()
            if ( (arc.nodes["start"].label == node_label or 
                    arc.nodes["end"].label == node_label))
        }
        
        for arc in arcs_to_remove.values():
            start, end = arc.nodes.values()
            self.model.delete_arc(start.label, end.label)
            
            arc.hide()
            
            arc.nodes["start"] = None
            arc.nodes["end"] = None
                
        self.view.arcs = {
            labels: arc for labels, arc in self.view.arcs.items()
            if labels not in arcs_to_remove
        }
        
        self.view.nodes.pop(node_label)
        self.model.delete_node(node_label)
        deleted_node.hide()
    
    @core.Slot(NodeView)
    def onArcCreationStart(self, node):
        if node is None:
            return
        
        if self.view.is__directed:
            self.view.arc_buffer = ArcView(node.pos())
        else:
            self.view.arc_buffer = EdgeView(node.pos())
            
        self.view.arc_buffer.nodes["start"] = node
        self.view.scene.addItem(self.view.arc_buffer)
    
    @core.Slot(NodeView)
    def onArcCreationEnd(self, node: NodeView):
        if node is None or node is self.view.arc_buffer.nodes["start"]:
            self.view.arc_buffer.hide()
            self.view.arc_buffer = None
            print("Canceled arc creation")
            
        else:
            if self.view.is__directed:
                self.view.arc_buffer.fixArc(node.pos())
            else:
                self.view.arc_buffer.setEndPoint(node.pos())
            
            self.view.arc_buffer.nodes["end"] = node
            start, end = self.view.arc_buffer.nodes.values()
            
            self.view.arcs[(start.label, end.label)] = self.view.arc_buffer
            self.model.add_arc(start.label, end.label)
            
            self.view.arc_buffer = None
            
    
    @core.Slot()
    def on_node_moving(self):
        for arc in self.view.arcs.values():
            arc.update_pos()                
    
    def color_next_node(self):
        try:
            next_node = next(self.algo_generator)
            if next_node is not None:
                self.view.set_node_color(next_node, self.new_node_color)
            
        except StopIteration:
            self.color_timer.stop()
            self.algo_generator = None
            self.view.set_node_colors()
            
    def color_next_node_in_components(self):
        try:
            next_node = next(self.algo_generator)
            
            if next_node[0] == True:
                self.new_node_color = utils.get_random_color()
            
            self.view.set_node_color(next_node[1], self.new_node_color)
            
        except StopIteration:
            self.color_timer.stop()
            self.algo_generator = None
    
    def color_list_nodes(self):
        try:
            next_nodes = next(self.algo_generator)
            self.new_node_color = utils.get_random_color()
            
            for node in next_nodes:
                self.view.set_node_color(node, self.new_node_color)
                
        except:
            self.color_timer.stop()
            self.algo_generator = None
            
            if self.rooting:
                self.algo_generator = self.model.generate_from_algorithm("Rooting tree", '')
                self.color_timer.timeout.disconnect()
                self.color_timer.timeout.connect(self.rooting_graph)
                self.color_timer.start(1000)
    
    def rooting_graph(self):
        try:
            level_nodes = next(self.algo_generator)
            level_width = (len(level_nodes) - 1) * WIDTH_TREE_OFFSEET
            curr_x = -level_width / 2
            
            for node_label in level_nodes:
                root_x, root_y = ROOT_POS
                
                self.view.nodes[node_label].setPos(
                    root_x + curr_x,
                    root_y + self.current_tree_index * HEIGHT_TREE_OFFSET
                )
                self.on_node_moving()
                
                curr_x += WIDTH_TREE_OFFSEET
            
            self.current_tree_index += 1
            
        except:
            self.color_timer.stop()
            self.algo_generator = None
            self.current_tree_index = 0
            self.rooting = False
            
    def color_next_arc(self):
        try:
            step = next(self.algo_generator)
            
            if isinstance(step, tuple):
                self.view.arcs[step[0]].color = self.new_node_color
                self.view.arcs[step[0]].update()
                
        except StopIteration:
            self.color_timer.stop()
            self.algo_generator = None
            self.view.set_node_colors()
            
    @core.Slot(str, str)        
    def start_algorithm(self, algo_name, start_label):
        print(algo_name if algo_name is not None else "None", start_label)
        self.color_timer.timeout.disconnect()

        match algo_name:
            case "Connected components" | "Strongly components":
                self.color_timer.timeout.connect(self.color_next_node_in_components)
                
            case "Deforestation":
                self.color_timer.timeout.connect(self.color_list_nodes)
                
            case "Rooting tree":
                self.color_timer.timeout.connect(self.color_list_nodes)
                self.rooting = True
            
            case "Kruskal" | "Boruvka":
                self.color_timer.timeout.connect(self.color_next_arc)
                
            case _:
                self.color_timer.timeout.connect(self.color_next_node)

        self.algo_generator = self.model.generate_from_algorithm(algo_name, start_label)        
        self.color_timer.start(2000)
        
        
    def add_weight(self, start_node, end_node, weight):
        arc = self.view.arcs[(start_node, end_node)]
        
        arc.weight = weight
        arc.update()
        
        