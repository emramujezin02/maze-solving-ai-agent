import threading
import time
from core.runner import TickResult

class BackgroundRunner:
    def __init__(self, runner, interval=0.1, training=True):
        self.runner = runner
        self.interval = interval
        self.training = training
        self.running = False
        self.thread = None

    def _loop(self):
        while self.running:
            result = self.runner.tick(training=self.training)
            if result.tick == TickResult.NO_WORK:
                time.sleep(self.interval)
                continue

            time.sleep(self.interval)

    def start(self):
        if self.running:
            return
        self.running = True
        self.runner.start()
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.runner.stop()
