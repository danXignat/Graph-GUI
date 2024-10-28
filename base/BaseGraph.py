from dataclasses import dataclass, field
from typing import Set, Dict, List

from .BaseArc import BaseArc
from .BaseNode import BaseNode

from uuid import UUID

@dataclass
class BaseGraph:
    nodes: Set[BaseNode] = field(default_factory = set)
    arc:   Set[BaseArc] = field(default_factory = set)
    
    adjacency_list: Dict[BaseNode, List[BaseNode]] = field(default_factory = dict)
    
    def add_node(self, node: BaseNode):
        self.nodes.add(node)
        self.adjacency_list[node] = list()
        
    def add_arc(self, arc: BaseArc):
        self.arc.add(arc)

        begin_exist: bool = arc.begin in self.nodes
        end_exists: bool = arc.end in self.nodes
        
        if begin_exist and end_exists:
            self.adjacency_list[arc.begin].append(arc.end)
            
    def __repr__(self):
        graph_str: str = ""
        for key, ls in self.adjacency_list.items():
            nodes_str = ', '.join(repr(node) for node in ls)
            graph_str += f"{key}: {nodes_str}\n"
            
        return graph_str

# nodes = [BaseNode("1"), BaseNode("2"), BaseNode("3"), BaseNode("4")]
# arcs = [BaseArc(nodes[0], nodes[1]), BaseArc(nodes[0], nodes[2]),
#         BaseArc(nodes[0], nodes[3]), BaseArc(nodes[2], nodes[3])]

# graph = BaseGraph()

# for node in nodes:
#     graph.add_node(node)
# for arc in arcs:
#     graph.add_arc(arc)

# print(graph)
                
    
    
    
    
    
    