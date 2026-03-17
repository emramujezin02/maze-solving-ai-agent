import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "../maze.db")

def init_db():
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS training_run(
        id INTEGER PRIMARY KEY,
        episodes INT,
        avg_reward REAL,
        success_rate REAL,
        time DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    c.commit()
    c.close()

def log_training(episodes, avg_reward, success_rate):
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute(
        "INSERT INTO training_run VALUES(NULL,?,?,?,CURRENT_TIMESTAMP)",
        (episodes, avg_reward, success_rate)
    )
    c.commit()
    c.close()
