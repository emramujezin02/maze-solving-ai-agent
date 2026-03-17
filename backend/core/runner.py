from enum import Enum
from collections import namedtuple

class TickResult(Enum):
    WORK_DONE="work_done"
    EPISODE_DONE="episode_done"
    NO_WORK="no_work"

MazeTickResult = namedtuple("MazeTickResult", ["state", "tick"])

class MazeAgentRunner:
    def __init__(self, agent, env, max_steps=300):
        self.agent = agent
        self.env = env
        self.max_steps = max_steps
        self.steps = 0
        self.active=False

    def start(self):
        self.active=True

    def stop(self):
        self.active=False

    def tick(self, training=True):
        if not self.active:
            return MazeTickResult(self.env.state, TickResult.NO_WORK)
        
        done=self.agent.learn_step(training=training)
        self.steps+=1

        if done or self.steps >= self.max_steps:
            self.steps=0
            if training:
                self.env.reset()
            return MazeTickResult(self.env.state,TickResult.EPISODE_DONE)

        return MazeTickResult(self.env.state,TickResult.WORK_DONE)

    def reset_episode(self):
        self.agent.total_reward = 0   
        self.steps = 0                





