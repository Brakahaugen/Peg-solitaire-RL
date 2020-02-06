from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F

import math
import sys
import random


class NeuralCritic:
    def __init__(self, simWorld, gamma, lamda, alpha):
        self.V = {} #V(s)
        self.e = {} #e(s)
        self.gamma = gamma
        self.lamda = lamda
        self.alpha = alpha
        self.delta = 0
        self.simWorld = simWorld
        self.model = self.init_nn()
        self.loss_fn = torch.nn.MSELoss(reduction='sum')


    def init_nn(self):
        L_1 = self.simWorld.num_cells
        L_2 = int(L_1 / 2)
        L_3 = int(L_2 / 2)
        L_4 = int(L_3 / 2)
        
        
        model = torch.nn.Sequential(
            torch.nn.Linear(L_1, L_2),
            torch.nn.ReLU(),
            torch.nn.Linear(L_2, L_3),
            torch.nn.ReLU(),
            torch.nn.Linear(L_3, L_4),
            torch.nn.ReLU(),
            torch.nn.Linear(L_4, 1),
        )

        return model

    def loss_function(self, delta):
        loss = torch.mean((delta)**2)
        return loss

    def updateDelta(self, r, prevS, s):   
   
        prevS = self.pre_process_state(prevS)
        s = self.pre_process_state(s)
        
        self.delta = r + self.gamma*self.model(s) - self.model(prevS)

    def updateEligibility(self, s):
        if not s in self.e:
            self.e[s] = 0
        self.e[s] = self.gamma*self.lamda*self.e[s]

    def updateValue(self, s):
        if not s in self.e:
            self.e[s] = 0
        loss = self.loss_function(self.delta)

        loss.backward(retain_graph=True)

        # self.model(s) += self.alpha*self.delta*self.e[s]
        return 0
    
    def getDelta(self):
        return self.delta

    def pre_process_state(self, state):

        tensor_state = torch.zeros([len(state)])
        
        for i in range(len(state)):
            tensor_state[i] = int(state[i])

        return tensor_state

class Critic:
    def __init__(self, simWorld, gamma, lamda, alpha):
        self.V = {} #V(s)
        self.e = {} #e(s)
        self.gamma = gamma
        self.lamda = lamda
        self.alpha = alpha
        self.delta = 0
        self.simWorld = simWorld
        # self.initDic()

    def initDic(self):
        #Maxlength 31, which is a size of max 7 given triangle, and max 5 given diamond.
        for i in range(2**self.simWorld.length):
            self.V[i] = random.random()/10
            self.e[i] = 0
        
    def resetEligibility(self):
        #Maxlength 31, which is a size of max 7 given triangle, and max 5 given diamond.
        for i in range(2**self.simWorld.length):
            self.e[i] = 0
        

    def updateDelta(self, r, prevS, s):
        if not s in self.V:
            self.V[s] = random.random()/10
        if not prevS in self.V:
            self.V[prevS] = random.random()/10
        self.delta = r + self.gamma*self.V[s] - self.V[prevS]
        # print(self.delta)

    def updateEligibility(self, s):
        if not s in self.e:
            self.e[s] = 0
        self.e[s] = self.gamma*self.lamda*self.e[s]
    
    def updateValue(self, s):
        if not s in self.V:
            self.V[s] = 0 #random.random()/10
        if not s in self.e:
            self.e[s] = 0
                
        self.V[s] += self.alpha*self.delta*self.e[s]
        return self.alpha*self.delta*self.e[s]
    
    def getDelta(self):
        return self.delta

class Actor:
    def __init__(self, simWorld, gamma, lamda, alpha):
        self.policy = {} #Policy(s,a)
        self.e = {} #e(s,a)
        self.alpha = alpha
        self.lamda = lamda
        self.gamma = gamma
        self.simWorld = simWorld
        # self.initDic()

    def initDic(self):
        #Maxlength 31, which is a size of max 7 given triangle, and max 5 given diamond.
        for s in range(2**self.simWorld.length):
            # maxnumber of actions is probably
            actions = int(3*self.simWorld.length/4)
            for a in range(actions):
                self.policy[s, a] = random.random()/10
                self.e[s, a] = 0

    def resetEligibility(self):
        #Maxlength 31, which is a size of max 7 given triangle, and max 5 given diamond.
        for s in range(2**self.simWorld.length):
            # maxnumber of actions is probably
            actions = int(3*self.simWorld.length/4)
            for a in range(actions):
                self.e[s, a] = 0

    def updateEligibility(self, s, a):
        if not (s,a) in self.e:
            self.e[s,a] = 0

        self.e[s,a] = self.gamma * self.lamda * self.e[s,a]

    def updatePolicy(self, s, a, delta):
        if not (s,a) in self.policy:
            self.policy[s, a] = random.random()/10
        if not (s,a) in self.e:
            self.e[s,a] = 0

        added_policy = self.alpha * delta * self.e[s,a]
        self.policy[s,a] += added_policy

        return added_policy


    def predict(self, s, actions, epsilon):
        choice = 0
        if len(actions) == 0 or len(actions) == 1:
            return choice
        if  random.random() > epsilon:
            choiceValue = -999
            choice = 0
            for a in range(len(actions)):
                if not (s,a) in self.policy:
                    self.policy[s, a] = random.random()/10
                if self.policy[s,a] > choiceValue:
                    choiceValue = self.policy[s,a]
                    choice = a
        else: 
            choice = random.randrange(0, len(actions))
        return choice
