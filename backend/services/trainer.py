from analytics.database import log_training

def train(agent, env, episodes):
    success = 0
    for _ in range(episodes):
        agent.learn_episode()
        if env.state == env.goal_pos:
            success += 1

    log_training(
        episodes=episodes,
        avg_reward=agent.total_reward / max(1, episodes),
        success_rate=success / episodes
    )
