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
        D_in = self.simWorld.num_cells
        D0_out = math.floor(self.simWorld.num_cells/2)
        D1_out = math.floor(D0_out/2)
        
        model = torch.nn.Sequential(
            torch.nn.Linear(D_in, D0_out),
            torch.nn.ReLU(),
            torch.nn.Linear(D0_out, D1_out),
        )
        return model

    def predict(self, x):

        # y = r +γV(s')

        
        y_pred = self.model(x)
        print("y_pred: " + str(y_pred))
        loss = self.loss_fn(y_pred, y)
        print("loss: " + str(loss))
        return y_pred


# class Net(nn.Module):



#     def forward(self, x):
#         # Max pooling over a (2, 2) window
#         x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
#         # If the size is a square you can only specify a single number
#         x = F.max_pool2d(F.relu(self.conv2(x)), 2)
#         x = x.view(-1, self.num_flat_features(x))
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x

#     def num_flat_features(self, x):
#         size = x.size()[1:]  # all dimensions except the batch dimension
#         num_features = 1
#         for s in size:
#             num_features *= s
#         return num_features



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
