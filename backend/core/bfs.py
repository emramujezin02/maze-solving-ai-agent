from collections import deque

def bfs(maze, start, goal):
    h, w = maze.shape
    q = deque()
    q.append((start, [start]))
    visited = set([start])

    while q:
        (r, c), path = q.popleft()
        if (r, c) == goal:
            return path

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w:
                if maze[nr, nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append(((nr, nc), path + [(nr, nc)]))
    return None
