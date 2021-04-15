import gym


def main():
    env = gym.make("CartPole-v1")
    observation = env.reset()
    for _ in range(1000):
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)

        if done:
            observation = env.reset()
    env.close()


if __name__ == "__main__":
    main()
