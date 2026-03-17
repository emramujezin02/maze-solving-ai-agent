def episodes_for_maze(env):
    d = env.difficulty_score()
    if d < 50: return 500
    if d < 150: return 2000
    return 5000
