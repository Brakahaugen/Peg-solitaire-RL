import math
import sys
import numpy as np
from hexgames.hexGrid import HexGrid
from simWorld import SimWorld
from actor_and_critic import Actor, Critic
import random

class SimplePlayer:
    def __init__(self,
    #Hyperparameters for learning:
    gamma = 0.9, lamda = 0.9, alpha_a = 0.1, alpha_c = 0.1, epsilon = 0.5, 
    #Rewards for winning and losing:
    winReward = 100, loseReward = -1,
    #BoardType and size:
    boardSize = 5, boardType = "triangle", visualization = True, initial_position = [0,0]
    ):

        lamda = lamda
        gamma = gamma
        alpha_a = alpha_a
        alpha_c = alpha_c
        self.epsilon = epsilon
        self.simWorld = SimWorld(boardSize, boardType, visualization, winReward, loseReward, initial_position)
        self.critic = Critic(self.simWorld, gamma, lamda, alpha_c)
        self.actor = Actor(self.simWorld, gamma, lamda, alpha_a)

        
    def choose_action(self):
        state = self.simWorld.createSimpleState()
        actions = self.simWorld.getValidActions()
        choice = self.actor.predict(state, actions, self.epsilon)
        return choice

    def doAction(self, action):
        #Gets in a number 
        actions = self.simWorld.getValidActions()
        # print(actions)
        act = actions[action]
        # print([self.simWorld.createSimpleState(), action])
        
        if not (self.simWorld.createSimpleState(), action) in self.actor.policy:
            self.actor.policy[self.simWorld.createSimpleState(), action] = random.random()/10

        self.simWorld.createSimpleState(), action
        reward = self.simWorld.updateGame(act, self.actor.policy[self.simWorld.createSimpleState(), action])
        # print(reward)
        return reward



