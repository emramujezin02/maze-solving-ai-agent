import numpy as np

class MazeEnvironment:
    def __init__(self, maze_file):
        self.maze_grid, self.start_pos, self.goal_pos = self.load_maze(maze_file)
        self.height, self.width = self.maze_grid.shape
        self.state = self.start_pos
        self.prev_state = None
        self.visited = set()

    def load_maze(self, file):
        grid, free = [], []

        with open(file) as f:
            for r, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue

                row = [int(x) for x in line.split()] if " " in line else [int(x) for x in line]

                for c, v in enumerate(row):
                    if v == 0:
                        free.append((r, c))
                grid.append(row)

        return np.array(grid), free[0], free[-1]

    def reset(self):
        self.state = self.start_pos
        self.prev_state = None
        self.visited = {self.state}
        return self.state



    def step(self, action):
        r, c = self.state
        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        dr, dc = moves[action]
        nr, nc = r + dr, c + dc
        old_r, old_c = self.state
        
        old_dist = abs(old_r - self.goal_pos[0]) + abs(old_c - self.goal_pos[1])
        new_dist = abs(nr - self.goal_pos[0]) + abs(nc - self.goal_pos[1])


        if not (0 <= nr < self.height and 0 <= nc < self.width):
            return self.state, -10, False

        if self.maze_grid[nr, nc] == 1:
            return self.state, -10, False

        new_state = (nr, nc)

        reward = -1

        if new_dist < old_dist:
            reward += 2      
        elif new_dist > old_dist:
            reward -= 2      


        if new_state == self.prev_state:
            reward -= 8

        if new_state in self.visited:
            reward -= 15

        self.visited.add(new_state)

        self.prev_state = self.state
        self.state = new_state

        if self.state == self.goal_pos:
            return self.state, 100, True

        return self.state, reward, False
