from dataclasses import dataclass, field
from typing import Optional

from uuid import UUID, uuid4

@dataclass
class BaseNode:
    label: str

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, label: str):
        self._label = label
    
    def __repr__(self):
        return f"N({self._label})"
    
    def __hash__(self):
        return hash(self._label)

class BaseNodeFactory:
    _instances = {}

    @classmethod
    def get_node(cls, identifier):
        if identifier not in cls._instances:
            cls._instances[identifier] = BaseNode(identifier)
        return cls._instances[identifier]
