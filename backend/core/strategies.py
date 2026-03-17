import numpy as np

class Strategy:
    def select_action(self, agent, state_index):
        raise NotImplementedError

class EpsilonGreedy(Strategy):
    def select_action(self, agent, state_index):
        if np.random.rand() < agent.epsilon:
            return np.random.randint(4)
        return int(np.argmax(agent.Q[state_index]))

class Greedy(Strategy):
    def select_action(self, agent, state_index):
        return int(np.argmax(agent.Q[state_index]))

class RandomWalk(Strategy):
    def select_action(self, agent, state_index):
        return np.random.randint(4)

class WallFollower(Strategy):
    def select_action(self, agent, state_index):
        return np.random.choice([0, 1, 2, 3])
