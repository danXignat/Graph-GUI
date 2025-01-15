from dataclasses import dataclass, field
from typing import Set, Dict, List, TypeVar, Union, Any
from uuid import UUID

@dataclass
class BaseGraph:
    nodes: Set[Any] = field(default_factory = set)
    arcs:   Set[Any] = field(default_factory = set)
    
    adjacency_list: Dict[Any, Set[Any]] = field(default_factory = dict)
    
    def add_node(self, node: Any):
        self.nodes.add(node)
        self.adjacency_list[node] = set()
        
    def add_arc(self, arc: Any):
        begin_exist: bool = arc.begin in self.nodes
        end_exists: bool = arc.end in self.nodes
        
        if arc in self.arcs:
            return False
        
        if not(begin_exist and end_exists):
            return False
        
        self.arcs.add(arc)
        self.adjacency_list[arc.begin].add(arc.end)

        return True
    
    def delete_node(self, node: Any):
        self.nodes.remove(node)
        self.adjacency_list.pop(node)
        for nodes in self.adjacency_list.values():
            nodes.discard(node)
    
    def delete_arc(self):
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
        
        return graph_str.rstrip('\n')


                
    
    
    
    
    
    