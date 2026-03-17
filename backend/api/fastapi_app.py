from fastapi import FastAPI
import sqlite3, os

app = FastAPI()
DB = "backend/maze.db"

@app.get("/stats/training")
def stats():
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute("SELECT avg_reward, success_rate, time FROM training_run")
    rows = cur.fetchall()
    return [{"avg_reward":r[0],"success_rate":r[1],"time":r[2]} for r in rows]
