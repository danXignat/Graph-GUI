from uuid import uuid4, UUID

class NodeModel:
    def __init__(self, data: str) -> None:
        self._data: str = data
        self._id: UUID = uuid4()

    @property
    def data(self) -> str:
        return self._data
    
    @property
    def id(self) -> str:
        return str(self._id)
    
    def __hash__(self):
        return hash(self._id)
    
    def __repr__(self):
        return f"Node({self._data})"
    
# node = {NodeModel("1"): "miau", NodeModel("2"): "bau"}

# print(node)