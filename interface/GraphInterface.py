from abc import ABC, abstractmethod


class GraphInterface(ABC):
    @abstractmethod
    def add_node(self):
        pass

    @abstractmethod
    def add_arc(self):
        pass

    @abstractmethod
    def delete_node(self):
        pass

    @abstractmethod
    def delete_arc(self):
        pass

    @abstractmethod
    def bfs(self):
        pass

    @abstractmethod
    def dfs(self):
        pass