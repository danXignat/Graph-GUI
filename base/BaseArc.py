from dataclasses import dataclass, field
from typing import Tuple, Optional

from uuid import UUID, uuid4

from .BaseNode import BaseNode

@dataclass
class BaseArc:
    begin: BaseNode
    end: BaseNode
    
    @property
    def pair(self) -> Tuple[BaseNode, BaseNode]:
        return (self.begin, self.end)
    
    def __hash__(self):
        return hash(self.begin) ^ hash(self.end)