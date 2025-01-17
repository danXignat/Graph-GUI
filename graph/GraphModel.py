import PySide6.QtCore as core
from typing import Optional
from dataclasses import dataclass, field

import graph.algorithms as algo

@dataclass
class NodeModel:
    label: str
    pos: core.QPointF = field(default_factory=core.QPointF(0, 0))

@dataclass
class ArcModel:
    begin_node: NodeModel
    end_node: NodeModel    
    weight: int
    capacity: Optional[int] = None
    cost: Optional[int] = None
    flow: int = field(default_factory=int)

class GraphModel(core.QObject):
    def __init__(self, is_directed: bool):
        super().__init__()
        self.is_directed = is_directed
        
        self.nodes:          dict[str, NodeModel] = {}
        self.arcs:           dict[(str, str), ArcModel] = {}
        self.adjacency_list: dict[str, set[str]] = {}
    
    def add_node(self, node_label, pos):
        node_model = NodeModel(node_label, pos)
        self.nodes[node_label] = node_model
        
        self.adjacency_list[node_label] = set()
        
    def delete_node(self, node_label):
        self.nodes.pop(node_label)
        self.adjacency_list.pop(node_label)
        
        for node_labels in self.adjacency_list.values():
            node_labels.discard(node_label)
            
    def add_arc(self, begin_label, end_label, weight = 0):
        arc = ArcModel(self.nodes[begin_label], self.nodes[end_label], weight)
        
        self.arcs[(begin_label, end_label)] = arc
        
        self.adjacency_list[arc.begin_node.label].add(arc.end_node.label)
        
        if self.is_directed == False:
            self.adjacency_list[arc.end_node.label].add(arc.begin_node.label)

    def delete_arc(self, start_label, end_label):
        self.arcs.pop((start_label, end_label))
        
        self.adjacency_list[start_label].discard(end_label)

    def generate_from_algorithm(self, name: str, *args):
        match name:
            case "Dijkstra" | "Bellman Ford":
                yield from algo.algorithms[name](self.adjacency_list, *args, self.arcs)    
            
            case "Kruskal" | "Boruvka":    
                yield from algo.algorithms[name](self.adjacency_list, self.arcs)    
                
            case _:
                yield from algo.algorithms[name](self.adjacency_list, *args)

    def __repr__(self):
        graph_str: str = "\n"
        for key, ls in self.adjacency_list.items():
            nodes_str = ', '.join(repr(node) for node in ls)
            graph_str += f"{key}: {nodes_str}\n"
        
        return graph_str.rstrip('\n')