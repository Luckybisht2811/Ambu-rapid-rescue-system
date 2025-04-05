import heapq

def dijkstra(grid, start, goals):
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    queue = [(0, start, [])]  # (distance, current_node, path)

    while queue:
        dist, node, path = heapq.heappop(queue)

        if node in visited:
            continue
        visited.add(node)

        path = path + [node]

        if node in goals:
            return dist, path, node  # distance, path list, goal reached

        x, y = node
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != '#':
                heapq.heappush(queue, (dist + 1, (nx, ny), path))

    return float('inf'), [], None
