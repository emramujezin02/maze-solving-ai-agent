import numpy as np
from core.env import MazeEnvironment
from core.strategies import EpsilonGreedy, Greedy

class QLearningAgent:
    def __init__(self):
        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995

        self.Q = None
        self.env = None
        self.strategy = "epsilon"

        self.total_reward = 0  
        self.episodes = 0       
        self.success = 0        


    def set_env(self, env):
        self.env = env
        n_states = env.height * env.width
        self.Q = np.zeros((n_states, 4), dtype=np.float32)

    def state_index(self, s=None):
        r, c = s if s else self.env.state
        return r * self.env.width + c

    def _walls(self, r, c):
        g = self.env.maze_grid
        h, w = self.env.height, self.env.width
        m = 0
        if r - 1 < 0 or g[r - 1, c] == 1: m |= 1
        if r + 1 >= h or g[r + 1, c] == 1: m |= 2
        if c - 1 < 0 or g[r, c - 1] == 1: m |= 4
        if c + 1 >= w or g[r, c + 1] == 1: m |= 8
        return m

    def choose_action(self):
        state = self.state_index()
        q_vals = self.Q[state]

        if self.strategy == "greedy":
            return int(np.argmax(q_vals))

        if np.random.rand() < self.epsilon:
            return np.random.randint(4)

        return int(np.argmax(q_vals))

    def learn_step(self, training=True):
        s_idx = self.state_index()
        action = self.choose_action()

        next_state, reward, done = self.env.step(action)
        ns_idx = self.state_index(next_state)

        if training:
            best_next = np.max(self.Q[ns_idx])
            self.Q[s_idx, action] += self.alpha * (
                reward + self.gamma * best_next - self.Q[s_idx, action]
            )

        self.total_reward += reward

        if done:
            self.episodes += 1
            self.success += 1

            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

        return done

    def save(self, path):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.save(path, self.Q)

