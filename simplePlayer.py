import math
import sys
import numpy as np
from hexgames.hexGrid import HexGrid
from simWorld import SimWorld
from actor_and_critic import *
import random

import time
import matplotlib.pyplot as plt



class SimplePlayer:
    def __init__(self,
    #Hyperparameters for learning:
    gamma = 0.9, lamda = 0.9, alpha_a = 0.1, alpha_c = 0.1, epsilon = 0.5, 
    #Rewards for winning and losing:
    winReward = 100, loseReward = -1,
    #Environment:
    env = "peg-solitaire",
    #BoardType and size:
    boardSize = 5, boardType = "triangle", visualization = True, initial_position = [0,0]
    ):

        lamda = lamda
        gamma = gamma
        alpha_a = alpha_a
        alpha_c = alpha_c
        self.epsilon = epsilon
        if env == "peg-solitaire":
            self.simWorld = SimWorld(boardSize, boardType, visualization, winReward, loseReward, initial_position)
        else: 
            self.simWorld = env
        self.critic = NeuralCritic(self.simWorld, gamma, lamda, alpha_c)
        self.actor = Actor(self.simWorld, gamma, lamda, alpha_a)

        
    def choose_action(self):
        state = self.simWorld.createSimpleState()
        actions = self.simWorld.getValidActions()
        choice = self.actor.predict(state, actions, self.epsilon)
        return choice

    def doAction(self, action):
        #Gets in a number action which maps to the action we wanna take
        actions = self.simWorld.getValidActions()
        act = actions[action]
        
        if not (self.simWorld.createSimpleState(), action) in self.actor.policy:
            self.actor.policy[self.simWorld.createSimpleState(), action] = random.random()/10

        # try:
        #     fail
        #     observation, reward, done, info = self.simWorld.step(act)
        # except:
        reward = self.simWorld.step(act, self.actor.policy[self.simWorld.createSimpleState(), action])
        start = time.time()
        self.simWorld.render()
        end = time.time()
        # if end-start > 0.001:
        #     print(end-start)
        return reward
    




def generic_actor_critic(SimplePlayer):
    #Init s and a
    prevS = player.simWorld.createSimpleState()
    #If there is no valid moves from the start
    if player.simWorld.checkGameFinished():
        return

    prevA = player.choose_action()        
    s_a_list.append([prevS, prevA])

    while not player.simWorld.isFinished:
        #Do action a from prevS, mote to s and receive reward r
        reward = player.doAction(prevA)
        s_ = player.simWorld.createSimpleState()

        #find the action based on the current state:
        a_ = player.choose_action()
        
        #Update the actors eligibility trace
        player.actor.e[s_,a_] = 1

        #Update the delta for the critic
        player.critic.updateDelta(reward, prevS, s_)
        
        #Update the eligibility traces for the critic:
        player.critic.e[prevS] = 1

        for s_a in s_a_list:
            s = s_a[0]
            a = s_a[1]

            #change value of s
            delta_value = player.critic.updateValue(s)

            #change eligibility of s
            player.critic.updateEligibility(s)
            
            #update policy of s_a
            delta_update = player.actor.updatePolicy(s, a, player.critic.getDelta())

            #update eligibility of actor
            player.actor.updateEligibility(s,a)

        prevS = s_
        prevA = a_
        s_a_list.append([prevS, prevA])

def run_policy_test(SimplePlayer):
    numEpisodes = 20
    episode = 0
    s_a_list =[]
    wins = 0
    
    player.epsilon = 0

    while episode < numEpisodes:
        player.simWorld.reset() 
        episode += 1

        while not player.simWorld.isFinished and len(player.simWorld.getValidActions()) != 0:
            prevA = player.choose_action()        
            reward = player.doAction(prevA)

        if player.simWorld.pegCount == 1:
            wins += 1

    return wins/numEpisodes

        

if __name__ == "__main__":
    player = SimplePlayer(
    #Hyperparameters for learning:
    gamma = 0.9, lamda = 0.9, alpha_a = 0.1, alpha_c = 0.1, epsilon = 0.5, 
    #Rewards for winning and losing:
    winReward = 100, loseReward = -10,
    #BoardType and size:
    boardSize = 5, boardType = "triangle", visualization = False, initial_position = [2,1]
    )

    epsilon_0 = player.epsilon

    numEpisodes = 5000
    test_every_x_episode = 5
    plot_and_save_every_x_episode = 200

    episode = 0
    peg_sum = 0
    episode_results = []
    i = 0
    policy_wins = 0
    policy_games = 0
    policy_tests = {}

    while episode < numEpisodes:
        
        player.simWorld.reset() 

        episode += 1
        s_a_list =[]
        player.epsilon = epsilon_0 - ((epsilon_0*episode) / numEpisodes)
        generic_actor_critic(player)

        peg_sum += (player.simWorld.pegCount)
        episode_results.append(player.simWorld.pegCount)
        
        if episode % test_every_x_episode == 0:

            policy_test = run_policy_test(player)
            policy_tests[episode] = policy_test
            
            print("we are now at episode: " + str(episode))
            print("Our current policy has a winrate of: " + str(policy_test))

            # episode_results.append(peg_sum/test_every_x_episode)
            peg_sum = 0

        if episode % plot_and_save_every_x_episode == 0:
            i += 1

            x = []
            y = []
            for key, value in policy_tests.items():
                x.append(key)
                y.append(value)

            fig = plt.figure()
            plt.title('On policy learning rate')
            plt.xlabel('Episode')
            plt.ylabel('On policy winrate')
            plt.plot(x,y)
            name = "plots/learning_rate" + str(i) + ".png"
            plt.savefig(name)
            plt.close(fig)

            fig = plt.figure()
            plt.title('Win plot')
            plt.xlabel('Episode')
            plt.ylabel('Remaining pegs at finish')
            plt.plot(episode_results)
            name = "plots/final_learnPlot" + str(i) + ".png"
            plt.savefig(name)
            plt.close(fig)