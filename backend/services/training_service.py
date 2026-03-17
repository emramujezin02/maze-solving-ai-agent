from services.background_runner import BackgroundRunner 

class TrainingService:
    def __init__(self, runner):
        self.runner = runner
        self.bg_runner = None

    def start_training(self):
        agent=self.runner.agent
        agent.strategy="epsilon"
        self.bg_runner=BackgroundRunner(self.runner,training=True)
        self.bg_runner.start()

    def start_inference(self):
        agent=self.runner.agent
        agent.strategy="greedy"
        agent.epsilon=0.0
        self.bg_runner=BackgroundRunner(self.runner,training=False)
        self.bg_runner.start()

    def stop(self):
        if self.bg_runner:
            self.bg_runner.stop()
            self.bg_runner=None
