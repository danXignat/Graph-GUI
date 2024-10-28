from uuid import uuid4, UUID
from typing import Tuple

class ArcModel:
    def __init__(self, data: Tuple[str, str]) -> None:
        self._data: Tuple[str, str] = data
        self._id: UUID = uuid4()

    @property
    def data(self) -> str:
        return self._data
    
    @property
    def begin(self) -> str:
        return self._data[0]

    @property
    def end(self) -> str:
        return self._data[1]

    @property
    def id(self) -> str:
        return str(self._id)