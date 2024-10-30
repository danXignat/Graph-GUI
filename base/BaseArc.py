from dataclasses import dataclass, field
from typing import Tuple, Optional, Any

from uuid import UUID, uuid4

@dataclass
class BaseArc:
    begin: Any
    end: Any
    
    @property
    def pair(self) -> Tuple[Any, Any]:
        return (self.begin, self.end)
    
    def __repr__(self):
        return f"A({self.begin}, {self.end})"

    def __hash__(self):
        return hash(self.begin) ^ hash(self.end)