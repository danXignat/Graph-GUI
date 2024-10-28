from pydantic import BaseModel
from typing import Any, Callable, Optional


from interface.Node import Node
class Edge(BaseModel, arbitrary_types_allowed=True):
    
    start_node: Optional[Node] = None
    end_node:   Optional[Node] = None
    
    def as_tuple(self):
        return (self.start_node, self.end_node)
    