from collections import deque

def bfs(graph, start_node):
  # Keep track of visited nodes to avoid cycles
  visited = set()
  queue = deque([start_node])

  while queue:
    # Dequeue the first node
    current_node = queue.popleft()

    # Process the current node (print node name and its connected nodes)
    print(f"Node: {current_node}")
    print(f"Connected Nodes: {graph[current_node]}")

    # Mark the current node as visited
    visited.add(current_node)

    # Enqueue unvisited neighbors
    for neighbor in graph[current_node]:
      if neighbor not in visited:
        queue.append(neighbor)

# Example usage
graph = {
  "A": ["B", "C"],
  "B": ["D", "E"],
  "C": ["F"],
  "D": [],
  "E": ["F"],
  "F": [],
}

start_node = "A"
bfs(graph, start_node)
