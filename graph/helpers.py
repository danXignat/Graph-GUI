def has_no_cycles(adjacency_list: dict[str, set[str]]) -> bool:
    visited = set()
    parent = {}
    
    def dfs_cycle_check(node: str, parent_node: str | None = None) -> bool:
        visited.add(node)
        
        for neighbor in adjacency_list[node]:
            if neighbor not in visited:
                parent[neighbor] = node
                if not dfs_cycle_check(neighbor, node):
                    return False
            
            elif neighbor != parent_node:
                return False
        return True
    
    for node in adjacency_list:
        if node not in visited:
            if not dfs_cycle_check(node):
                return False
    
    return True

def has_correct_edges(adjacency_list: dict[str, set[str]]) -> bool:
    n = len(adjacency_list)
    edge_count = sum(len(neighbors) for neighbors in adjacency_list.values()) // 2
    return edge_count == n - 1

def is_connected(adjacency_list: dict[str, set[str]]) -> bool:
    from graph.algorithms import bfs    
    
    if not adjacency_list:
        return True
        
    start_node = next(iter(adjacency_list))
    visited = set()
    
    for node in bfs(adjacency_list, start_node):
        visited.add(node)
    
    return len(visited) == len(adjacency_list)

def is_tree(adjacency_list: dict[str, set[str]]) -> bool:
    return (has_no_cycles(adjacency_list) and 
            has_correct_edges(adjacency_list) and 
            is_connected(adjacency_list))
    
def organize_tree_levels(adjacency_list: dict[str, set[str]]) -> list[list[str]]:
    if not adjacency_list:
        return []
        
    root = max(adjacency_list.items(), key=lambda x: len(x[1]))[0]
    
    levels: list[list[str]] = []
    visited = set()
    current_level = [root]
    
    while current_level:
        levels.append(current_level.copy())
        visited.update(current_level)
        
        next_level = []
        for node in current_level:
            for neighbor in adjacency_list[node]:
                if neighbor not in visited and neighbor not in next_level:
                    next_level.append(neighbor)
        
        next_level.sort()
        current_level = next_level
    
    return levels