import glob, random, os
import numpy as np
from flask import Flask, jsonify, send_from_directory

from core.env import MazeEnvironment
from core.agent import QLearningAgent
from core.runner import MazeAgentRunner
from services.training_service import TrainingService
from core.bfs import bfs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(BASE_DIR, "..", "..", "frontend")
DATA = os.path.join(BASE_DIR, "..", "data")

QTABLE_DIR = os.path.join(BASE_DIR, "..", "q_tables")
os.makedirs(QTABLE_DIR, exist_ok=True)
QPATH = os.path.join(QTABLE_DIR, "global_q.npy")

app = Flask(__name__, static_folder=FRONTEND, static_url_path="")

agent = QLearningAgent()
env = None
runner = None
training_service = None
mazes = glob.glob(os.path.join(DATA, "*.txt"))

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/reset", methods=["POST"])
def reset():
    global env, runner, training_service, agent

    env = MazeEnvironment(random.choice(mazes))
    agent = QLearningAgent()
    agent.set_env(env)

    runner = MazeAgentRunner(agent, env)
    training_service = TrainingService(runner)

    s = env.reset()
    return jsonify({
        "maze": env.maze_grid.tolist(),
        "state": {"row": s[0], "col": s[1]},
        "goal": {"row": env.goal_pos[0], "col": env.goal_pos[1]}
    })

@app.route("/api/start_training", methods=["POST"])
def start_training():
    if training_service is None:
        return jsonify({"error": "Maze not initialized"}), 400

    training_service.start_training()
    return jsonify({"message": "Training started"})

@app.route("/api/start_inference", methods=["POST"])
def start_inference():
    if training_service is None:
        return jsonify({"error": "Maze not initialized"}), 400

    training_service.start_inference()
    return jsonify({"message": "Inference started"})

@app.route("/api/stop", methods=["POST"])
def stop():
    if training_service:
        training_service.stop()
    return jsonify({"message": "Runner stopped"})

@app.route("/api/step", methods=["POST"])
def step():
    if runner is None:
        return jsonify({"error": "Maze not initialized"}), 400

    state = runner.env.state
    return jsonify({
        "state": {
            "row": state[0],
            "col": state[1]
        }
    })

@app.route("/api/play_best", methods=["POST"])
def play_best():
    path = bfs(
        env.maze_grid,
        tuple(env.start_pos),
        tuple(env.goal_pos)
    )

    if not path:
        return jsonify({"error": "Maze nema rješenje"}), 400

    return jsonify({"path": path})

