import sqlite3, matplotlib.pyplot as plt

c = sqlite3.connect("backend/maze.db")
cur = c.cursor()
cur.execute("SELECT avg_reward FROM training_run")
r = [x[0] for x in cur.fetchall()]
plt.plot(r)
plt.title("Learning Curve")
plt.show()
