from dataclasses import dataclass, field
from typing import Set, Dict, List, TypeVar, Union, Any
from uuid import UUID

from interface import GraphInterface


@dataclass
class BaseGraph(GraphInterface):
    nodes: Set[Any] = field(default_factory = set)
    arc:   Set[Any] = field(default_factory = set)
    
    adjacency_list: Dict[Any, List[Any]] = field(default_factory = dict)
    
    def add_node(self, node: Any):
        self.nodes.add(node)
        self.adjacency_list[node] = list()
        
    def add_arc(self, arc: Any):
        self.arc.add(arc)

        begin_exist: bool = arc.begin in self.nodes
        end_exists: bool = arc.end in self.nodes
        
        if begin_exist and end_exists:
            self.adjacency_list[arc.begin].append(arc.end)

    def remove_node(self):
        pass
    
    def remove_arc(self):
        pass

    def dfs(self):
        pass

    def bfs(self):
        pass

    def __repr__(self):
        graph_str: str = ""
        for key, ls in self.adjacency_list.items():
            nodes_str = ', '.join(repr(node) for node in ls)
            graph_str += f"{key}: {nodes_str}\n"
            
        return graph_str


                
    
    
    
    
    
    