from collections import deque, defaultdict
from typing import List, Dict, Tuple, Any
import heapq

def residual_bfs(graph, s, t, parent):
    visited = set()
    que = deque()
    que.append(s)
    visited.add(s)
    parent[s] = -1

    while que:
        u = que.popleft()
        for node_id in graph.get(u, {}):
            flow = graph[u][node_id]
            if node_id not in visited and flow > 0:
                que.append(node_id)
                visited.add(node_id)
                parent[node_id] = u
                if node_id == t:
                    return  True

    return False

def ford_fulkerson(
    adjacency_list: dict[str, set[str]], 
    arcs: dict[tuple[str, str], Any],
    source: str,
    sink: str
):
    r_g = {}
    for node in adjacency_list:
        r_g[node] = {}
        for neighbor in adjacency_list[node]:
            r_g[node][neighbor] = arcs[(node, neighbor)].capacity
            if neighbor not in r_g:
                r_g[neighbor] = {}
            r_g[neighbor][node] = 0
    
    parent = {node: None for node in adjacency_list}
    max_flow = 0
    
    while residual_bfs(r_g, source, sink, parent):
        current = sink
        path_flow = float('inf')
        path_edges = []
        
        while current != source:
            prev = parent[current]
            path_flow = min(path_flow, r_g[prev][current])
            path_edges.append((prev, current))
            current = prev
            
        for edge in path_edges:
            yield (edge, False)
        
        max_flow += path_flow
        current = sink
        
        while current != source:
            prev = parent[current]
            r_g[prev][current] -= path_flow
            r_g[current][prev] += path_flow
            yield ((prev, current), True)
            current = prev
    
    flows = {(u, v): r_g[v][u] for u in r_g for v in r_g[u] if r_g[v][u] > 0}
    yield (max_flow, flows)


def bellman_ford(graph: Dict[int, List[Tuple]], source: int, n: int, residual_graph: Dict[int, List[Tuple]]) -> Tuple[
    bool, Dict[int, float]]:

    distances = {i: float('inf') for i in range(n)}
    distances[source] = 0
    predecessor = {i: None for i in range(n)}

    for _ in range(n - 1):
        for u in residual_graph:
            for v, flux, capacity, weight in residual_graph[u]:
                if distances[u] + weight < distances[v] and flux < capacity:
                    distances[v] = distances[u] + weight
                    predecessor[v] = u

    for u in residual_graph:
        for v, flux, capacity, weight in residual_graph[u]:
            if distances[u] + weight < distances[v] and flux < capacity:
                return True, predecessor

    return False, predecessor


def find_negative_cycle(graph: Dict[int, List[Tuple]], n: int, residual_graph: Dict[int, List[Tuple]]) -> List[int]:
    has_negative_cycle, predecessor = bellman_ford(graph, 0, n, residual_graph)

    if not has_negative_cycle:
        return []

    visited = set()
    curr = 0
    while curr not in visited:
        visited.add(curr)
        curr = predecessor[curr]

    cycle = []
    start = curr
    cycle.append(start)
    curr = predecessor[start]
    while curr != start:
        cycle.append(curr)
        curr = predecessor[curr]
    cycle.append(start)

    return cycle[::-1]


def find_residual_capacity(cycle: List[int], residual_graph: Dict[int, List[Tuple]]) -> float:
    min_capacity = float('inf')

    for i in range(len(cycle) - 1):
        u = cycle[i]
        v = cycle[i + 1]

        for to_node, flux, capacity, weight in residual_graph[u]:
            if to_node == v:
                residual_cap = capacity - flux
                min_capacity = min(min_capacity, residual_cap)
                break

    return min_capacity


def create_residual_graph(graph: Dict[int, List[Tuple]]) -> Dict[int, List[Tuple]]:
    residual_graph = defaultdict(list)

    for u in graph:
        for v, weight, capacity in graph[u]:
            residual_graph[u].append((v, 0, capacity, weight))
            residual_graph[v].append((u, 0, 0, -weight))

    return residual_graph


def cycle_canceling(
    adjacency_list: dict[str, set[str]],
    arcs: dict[tuple[str, str], Any], 
    source: str,
    sink: str
):
    
    ff_gen = ford_fulkerson(adjacency_list, arcs, source, sink)
    max_flow = None
    flows = None
    
    for result in ff_gen:
        if isinstance(result, tuple) and not isinstance(result[0], str):
            max_flow, flows = result
        else:
            yield result 
            
    r_g = defaultdict(list)
    for (u, v), arc in arcs.items():
        flow = flows.get((u, v), 0)
        r_g[u].append((v, flow, arc.capacity, arc.cost))
        r_g[v].append((u, 0, 0, -arc.cost))
    
    while True:
        cycle = find_negative_cycle(r_g, len(adjacency_list), dict(r_g))
        if not cycle:
            break
            
        
        for i in range(len(cycle)-1):
            yield ((cycle[i], cycle[i+1]), False)
            
        min_capacity = find_residual_capacity(cycle, dict(r_g))
        
        for i in range(len(cycle)-1):
            u, v = cycle[i], cycle[i+1]
            for j, (to_node, flux, capacity, weight) in enumerate(r_g[u]):
                if to_node == v:
                    r_g[u][j] = (to_node, flux + min_capacity, capacity, weight)
                    yield ((u, v), True)
                    break
                    
            for j, (to_node, flux, capacity, weight) in enumerate(r_g[v]):
                if to_node == u:
                    r_g[v][j] = (to_node, flux + min_capacity, capacity, weight)
                    break
    
    final_flows = {}
    for u in r_g:
        for v, flow, cap, cost in r_g[u]:
            if cap > 0:
                final_flows[(u, v)] = flow
                
    yield final_flows