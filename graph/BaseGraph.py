from typing import List, Set, Dict, Any, Optional

class BaseGraph:
    def __init__(self, nodes: Optional[List] = [], edges: Optional[List] = []):
        self.nodes: List = []
        self.edges: List = []
        self.adjacency_list: Dict[Any, Set] = {}
        
        for node in nodes:
            self.addNode(node)
        
        for edge in edges:
            self.addEdge(edge)
            
    def addNode(self, node):
        self.nodes.append(node)
        
        self.adjacency_list[node] = set()
        
    def addEdge(self, edge):
        start, end = edge
        if start not in self.nodes:
            self.add_node(start)
        if end not in self.nodes:
            self.add_node(end)
            
        self.edges.append(edge)
        self.adjacency_list[edge[0]].add(edge[1])
        
    def getAdjacencyList(self):
        return self.adjacency_list
    
    def __repr__(self):
        result = ""
        for node, connections in self.adjacency_list.items():
            result += f"{node}: -> "
            if connections:
                result += f"{', '.join(map(str, (connections)))}\n"
            else:
                result += 'None\n'
            
        return result
    
    def dfs(self, start_node):
        visited = set()
        traversed = []
        stack = [start_node]
        
        while stack:
            node = stack.pop()
            
            if node not in visited:
                visited.add(node)
                traversed.append(node)
            
            stack.extend(
                filter(lambda x: x not in visited, self.adjacency_list[node])
            )
        
        return traversed
    
    def bfs(self, start_node):
        visited = set()
        traversed = []
        queue = [start_node]

        while queue:
            node = queue.pop(0)

            if node not in visited:
                yield node
                visited.add(node)
                traversed.append(node)
            
            queue.extend(
                filter(lambda x: x not in visited, self.adjacency_list[node])
            )
        



nodes = [1, 2, 3, 4, 5]
edges = [(1, 2), (2, 3), (1, 3), (3, 4), (2, 1)]

graph = BaseGraph(nodes, edges)

gen = graph.bfs(1)

print(next(gen))


    