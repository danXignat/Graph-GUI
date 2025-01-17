from collections import deque
import heapq

from typing import Generator
from graph.helpers import is_tree
from .flux_algs import ford_fulkerson, cycle_canceling

def dfs(adjacency_list: dict[str, set[str]], start_node: str, *args) -> Generator[str, None, None]:
        visited = set()
        stack = [start_node]
        
        while stack:
            node = stack.pop()
            
            if node not in visited:
                visited.add(node)
                yield node

                stack.extend(reversed([n for n in adjacency_list[node] if n not in visited]))

def bfs(adjacency_list: dict[str, set[str]], start_node: str, *args) -> Generator[str, None, None]:
    visited = set()
    queue = deque([start_node])

    while queue:
        node = queue.popleft()
        
        if node not in visited:
            visited.add(node)
            yield node

            queue.extend([n for n in adjacency_list[node] if n not in visited])

def connected_components(adjacency_list: dict[str, set[str]], start_node: str, *args) -> Generator[tuple[bool, str], None, None]:
    start_node = list(adjacency_list)[0] if start_node == '' else start_node
    
    unvisited = set(adjacency_list.keys())
    
    yield (True, start_node)
    first_node = True
    for node in bfs(adjacency_list, start_node):
        if not first_node:
            yield (False, node)
        first_node = False
        unvisited.discard(node)
    
    while unvisited:
        start = next(iter(unvisited))
        yield (True, start)
        
        first_node = True
        for node in bfs(adjacency_list, start):
            if not first_node:
                yield (False, node)
            first_node = False
            unvisited.discard(node)

def strongly_connected_components(
    adjacency_list: dict[str, set[str]], 
    start_node: str = ''
) -> Generator[tuple[bool, str], None, None]:
    start_node = list(adjacency_list)[0] if start_node == '' else start_node
    
    reversed_graph = {node: set() for node in adjacency_list}
    for node in adjacency_list:
        for neighbor in adjacency_list[node]:
            reversed_graph[neighbor].add(node)
    
    visited = set()
    finish_order = []
    
    def dfs_first(node: str):
        if node in visited:
            return
        visited.add(node)
        for neighbor in adjacency_list[node]:
            dfs_first(neighbor)
        finish_order.append(node)
    
    for node in adjacency_list:
        if node not in visited:
            dfs_first(node)
    
    visited.clear()
    
    def dfs_second(node: str, first_in_component: bool):
        if node in visited:
            return
        visited.add(node)
        yield (first_in_component, node)
        for neighbor in reversed_graph[node]:
            yield from dfs_second(neighbor, False)
    
    while finish_order:
        node = finish_order.pop()
        if node not in visited:
            yield from dfs_second(node, True)

def topological_sort(adjacency_list: dict[str, set[str]], start_node: str, *args) -> Generator[str, None, None]:
    in_degree: dict[str, int] = {node: 0 for node in adjacency_list}
    
    for node in adjacency_list:
        for neighbor in adjacency_list[node]:
            in_degree[neighbor] += 1
    
    queue = deque([node for node, degree in in_degree.items() if degree == 0])
    
    while queue:
        node = queue.popleft()
        yield node
        
        for neighbor in adjacency_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

def deforest(adjacency_list: dict[str, set[str]], *args) -> Generator[list[str], None, None]:
    current_graph = {node: neighbors.copy() 
                    for node, neighbors in adjacency_list.items()}
    
    while current_graph:
        
        leaves = [node for node, neighbors in current_graph.items() 
                 if len(neighbors) == 1]
        
        if not leaves and current_graph:
            
            yield list(current_graph.keys())
            break
            
        if leaves:
            yield leaves
            
            for leaf in leaves:
                if leaf in current_graph:
                    
                    neighbor = next(iter(current_graph[leaf]))
                    
                    if neighbor in current_graph:
                        current_graph[neighbor].discard(leaf)
                    
                    del current_graph[leaf]
                    
def rooting_tree(adjacency_list: dict[str, set[str]], root: str, *args) -> Generator[list[str], None, None]:
    if not adjacency_list:
        return
        
    if root == '':
        root = max(adjacency_list.items(), key=lambda x: len(x[1]))[0]
        
    elif root not in adjacency_list:
        return
        
    visited = set()
    current_level = [root]
    
    while current_level:
        yield current_level
        
        visited.update(current_level)
        next_level = []
        
        for parent in current_level:
            for neighbor in sorted(adjacency_list[parent]):
                if neighbor not in visited and neighbor not in next_level:
                    next_level.append(neighbor)
        
        current_level = next_level


def dijkstra(
    adjacency_list: dict[str, set[str]],
    start: str,
    end: str,
    arcs,
) -> Generator[tuple[int, bool], None, set[str]]:
    pq = [(0, start)]
    distances = {node: float('inf') for node in adjacency_list}
    distances[start] = 0
    visited = set()
    predecessors = {node: None for node in adjacency_list}  # To reconstruct the path

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)
        yield (current_node, True if current_node == end else False)

        if current_node == end:
            path = set()
            while current_node:
                path.add(current_node)
                current_node = predecessors[current_node]
            yield path
            return

        for neighbor in adjacency_list[current_node]:
            weight = arcs[(current_node, neighbor)].weight

            if neighbor not in visited:
                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node  # Track the predecessor
                    heapq.heappush(pq, (new_distance, neighbor))
                    yield (neighbor, False)

def bellman_ford(
    adjacency_list: dict[str, set[str]],
    start: str,
    end: str,
    arcs
) -> Generator[tuple[int, bool], None, list[str]]:
    distances = {node: float('inf') for node in adjacency_list}
    distances[start] = 0
    predecessors = {node: None for node in adjacency_list}

    for _ in range(len(adjacency_list) - 1):
        for (u, v), arc in arcs.items():
            weight = arc.weight
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                yield (v, False)

    for (u, v), arc in arcs.items():
        weight = arc.weight
        if distances[u] + weight < distances[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    if distances[end] < float('inf'):
        path = set()
        current_node = end
        while current_node:
            path.add(current_node)
            current_node = predecessors[current_node]
        yield path
        return

    yield []
    return

def kruskal(
    adjacency_list: dict[str, set[str]],
    arcs, *args
) -> Generator[tuple[tuple[str, str], bool], None, set[tuple[str, str]]]:
    parent = {node: node for node in adjacency_list}
    rank = {node: 0 for node in adjacency_list}
    
    def find(node: str) -> str:
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    
    def union(node1: str, node2: str):
        root1, root2 = find(node1), find(node2)
        if root1 != root2:
            if rank[root1] < rank[root2]:
                root1, root2 = root2, root1
            parent[root2] = root1
            if rank[root1] == rank[root2]:
                rank[root1] += 1
    
    edges = [(arc[0], arc[1], arcs[arc].weight) 
            for arc in arcs]
    edges.sort(key=lambda x: x[2])
    
    mst_edges = set()
    
    for node1, node2, weight in edges:
        yield ((node1, node2), False)
        
        if find(node1) != find(node2):
            union(node1, node2)
            mst_edges.add((node1, node2))
            yield ((node1, node2), True)
    
    yield mst_edges

def boruvka(
    adjacency_list: dict[str, set[str]],
    arcs
) -> Generator[tuple[tuple[str, str], bool], None, set[tuple[str, str]]]:
    parent = {node: node for node in adjacency_list}
    rank = {node: 0 for node in adjacency_list}
    
    def find(node: str) -> str:
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    
    def union(node1: str, node2: str):
        root1, root2 = find(node1), find(node2)
        if root1 != root2:
            if rank[root1] < rank[root2]:
                root1, root2 = root2, root1
            parent[root2] = root1
            if rank[root1] == rank[root2]:
                rank[root1] += 1
    
    mst_edges = set()
    components = {node: {node} for node in adjacency_list}
    
    while len(set(map(find, adjacency_list))) > 1: 
        cheapest_edges = {}
        
        for (node1, node2) in arcs:
            weight = arcs[(node1, node2)].weight
            root1, root2 = find(node1), find(node2)
            
            if root1 != root2:
                yield ((node1, node2), False)
                
                if root1 not in cheapest_edges or weight < arcs[cheapest_edges[root1]].weight:
                    cheapest_edges[root1] = (node1, node2)
                if root2 not in cheapest_edges or weight < arcs[cheapest_edges[root2]].weight:
                    cheapest_edges[root2] = (node1, node2)
        
        if not cheapest_edges:
            break
            
        added_edges = set()
        for edge in cheapest_edges.values():
            node1, node2 = edge
            if find(node1) != find(node2):
                union(node1, node2)
                mst_edges.add(edge)
                added_edges.add(edge)
                yield (edge, True)
        
        if not added_edges:
            break
    
    yield mst_edges

algorithms = {
    "DFS"                 : dfs,
    "BFS"                 : bfs,
    "Connected components": connected_components,
    "Strongly components" : strongly_connected_components,
    "Topological sort"    : topological_sort,
    "Deforestation"       : deforest,
    "Rooting tree"        : rooting_tree,
    "Dijkstra"            : dijkstra,
    "Bellman Ford"        : bellman_ford,
    "Kruskal"             : kruskal,
    "Boruvka"             : boruvka,
    "Ford Fulkerson"      : ford_fulkerson,
    "Cycle Canceling"     : cycle_canceling
}