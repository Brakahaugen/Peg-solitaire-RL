import gym
from actor_critic_keras import Agent
import utils
import numpy as np

if __name__ == '__main__':
    agent = Agent(alpha=0.00001, beta=0.00005)

    env = gym.make('LunarLander')
    score_history = []
    num_episodes = 2000

    for i in range(num_episodes):
        done = False
        score = 0
        observation = env.reset()

        while not done:
            action = agent.choose_action(observation)
            observation_,reward, done, info = env.step(action)
            agent.learn(observation, action, reward, observation_, done)
            observation = observation_
            score += reward

        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        print(score)


        filename = 'lunar-lander-actor-critic.png'
        utils.plotLearning(score_history, filename=filename, window=100)