import PySide6.QtWidgets as widg
import PySide6.QtCore as core
import PySide6.QtGui as gui

from .GraphModel import GraphModel
from .GraphView import GraphView
from items.Node import NodeView
from items.Arc import ArcView

class GraphController(core.QObject):
    def __init__(self, model: GraphModel, view: GraphView):
        super().__init__()
        self.view = view
        self.model = model
        
        self.node_counter = 0
        
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
        
        self.view.nodes.append(node)        
        self.view.scene.addItem(node)
        print(f"Node {label} created successfully")
    
    @core.Slot(NodeView)
    def onArcCreationStart(self, node):
        if node is None:
            return
            
        # Clean up any existing arc buffer first
        if self.view.arc_buffer is not None:
            self.cleanupArcBuffer()
        
        self.view.arc_buffer = ArcView(node.pos())
        self.view.arc_buffer.nodes["start"] = node
        self.view.scene.addItem(self.view.arc_buffer)
    
    @core.Slot(NodeView)
    def onArcCreationEnd(self, node):
        if self.view.arc_buffer is None:
            return
            
        # If canceling or invalid end node, cleanup properly
        if node is None:
            self.cleanupArcBuffer()
            print("canceled")
            return
            
        try:
            self.view.arc_buffer.fixArc(node)
            self.view.arc_buffer.nodes["end"] = node
            self.view.arcs.append(self.view.arc_buffer)
            self.view.arc_buffer = None
        except Exception as e:
            print(f"Error completing arc: {e}")
            self.cleanupArcBuffer()
    
    @core.Slot()
    def on_node_moving(self):
        try:
            for arc in self.view.arcs:
                arc.update()
        except Exception as e:
            print(f"Error during node movement: {e}")
            
    @core.Slot(str)            
    def on_node_deleted(self, node_label):
        try:
            # First clean up any in-progress arc creation
            if self.view.arc_buffer is not None:
                self.cleanupArcBuffer()
            
            # Find and remove the node
            deleted_node = next((node for node in self.view.nodes if node.label == node_label), None)
            if deleted_node is None:
                return
                
            # Remove connected arcs first
            arcs_to_remove = [
                arc for arc in self.view.arcs 
                if (arc.nodes["start"].label == node_label or 
                    arc.nodes["end"].label == node_label)
            ]
            
            # Clean up arcs
            for arc in arcs_to_remove:
                if arc in self.view.scene.items():
                    self.view.scene.removeItem(arc)
                    # Clear node references to prevent circular references
                    arc.nodes["start"] = None
                    arc.nodes["end"] = None
            
            # Update arc list
            self.view.arcs = [arc for arc in self.view.arcs if arc not in arcs_to_remove]
            
            # Finally remove the node
            if deleted_node in self.view.scene.items():
                self.view.scene.removeItem(deleted_node)
            self.view.nodes.remove(deleted_node)
            
        except Exception as e:
            print(f"Error during node deletion: {e}")

    
    def cleanupArcBuffer(self):
        """Safely cleanup the arc buffer"""
        if self.view.arc_buffer:
            if self.view.arc_buffer in self.view.scene.items():
                self.view.scene.removeItem(self.view.arc_buffer)
            self.view.arc_buffer = None