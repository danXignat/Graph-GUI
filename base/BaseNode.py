from dataclasses import dataclass, field
from typing import Optional

from uuid import UUID, uuid4

class BaseNode:
    def __init__(self, label: str):
        self._label = label

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