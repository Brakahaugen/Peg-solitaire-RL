import math
import sys
import numpy as np
from hexgames.hexGrid import HexGrid
from simWorld import SimWorld
from actor_and_critic import *
import random

import time
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, env, actor, critic, epsilon = 0.5):
        self.epsilon = epsilon
        self.simWorld = env
        self.critic = critic
        self.actor = actor

        
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
    