def evaluate_agent(agent, env, episodes=50, max_steps=500):
    successes = 0
    total_steps = 0

    old_strategy = agent.strategy
    agent.strategy = "greedy"

    for _ in range(episodes):
        env.reset()
        for step in range(max_steps):
            done = agent.learn_step()
            if done:
                successes += 1
                total_steps += step + 1
                break

    agent.strategy = old_strategy

    return {
        "success_rate": successes / episodes,
        "avg_steps": total_steps / max(1, successes)
    }
