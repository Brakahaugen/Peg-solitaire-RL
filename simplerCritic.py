import math
import sys
import numpy as np
from hexgames.hexGrid import HexGrid
from simWorld import SimWorld
import random
import time
import matplotlib.pyplot as plt



class Critic:
    def __init__(self, simWorld, gamma, lamda, alpha):
        self.V = {} #V(s)
        self.e = {} #e(s)
        self.gamma = gamma
        self.lamda = lamda
        self.alpha = alpha
        self.delta = 0
        self.simWorld = simWorld
        self.initDic()

    def initDic(self):
        #Maxlength 31, which is a size of max 7 given triangle, and max 5 given diamond.
        for i in range(2**self.simWorld.length):
            self.V[i] = random.random()/10
            self.e[i] = 0

    def updateDelta(self, r, prevS, s):
        self.delta = r + self.gamma*self.V[prevS] - self.V[s]
    
    def updateEligibility(self, s):
        self.e[s] = self.gamma*self.lamda*self.e[s]
    
    def updateValue(self, s):
        self.V[s] += self.alpha*self.delta*self.e[s]
    
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
        self.initDic()

    def initDic(self):
        #Maxlength 31, which is a size of max 7 given triangle, and max 5 given diamond.
        for s in range(2**self.simWorld.length):
            # maxnumber of actions is probably
            actions = int(3*self.simWorld.length/4)
            for a in range(actions):
                self.policy[s, a] = random.random()/10
                self.e[s, a] = 0


    def updateEligibility(self, s, a):
        self.e[s,a] = self.gamma * self.lamda * self.e[s,a]

    def updatePolicy(self, s, a, delta):
        self.policy[s,a] += self.alpha * delta * self.e[s,a]
        

    def predict(self, s, actions, epsilon):
        if len(actions) == 0:
            return 0
        if len(actions) == 1:
            return 0
        if random.random() > epsilon:
            choiceValue = -999
            choice = 0
            for a in range(len(actions)):
                if self.policy[s,a] > choiceValue:
                    choiceValue = self.policy[s,a]
                    return a
        else: 
            return random.randrange(0, len(actions)-1)

class SimplePlayer:
    def __init__(self):
        lamda = 0.9
        gamma = 0.9
        alpha_a = 0.00001
        alpha_c = 0.00001
        self.epsilon = 0.5
        self.simWorld = SimWorld(5, "triangle")
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
        action = actions[action]
        reward = self.simWorld.updateGame(action)
        return reward


    

if __name__ == "__main__":

    player = SimplePlayer()
    numEpisodes = 100000
    episode = 0
    episode_results = []
    lastWin = 0 
    i = 0
    prevValues = None   


    while episode < numEpisodes:
        episode += 1
        s_a_list =[]
        if player.epsilon > 0:
            player.epsilon = 0.5 - ((0.5*episode + 100) / numEpisodes)



        prevS = player.simWorld.createSimpleState()
        prevA = player.choose_action()
        # print(player.simWorld.getValidActions())
        reward = player.doAction(prevA)

        while not player.simWorld.isFinished:

            s = player.simWorld.createSimpleState()

            #find the action based on the current state:
            a = player.choose_action()

            
            #Update the actors eligibility trace
            player.actor.e[s,a] = 1

            #Update the delta for the critic
            player.critic.updateDelta(reward, prevS, s)
            
            #Update the eligibility traces for the critic:
            player.critic.e[s] = 1

            prevS = s
            prevA = a
            #for each state action pair in this episode:

            #TODO CREATE A HASHING FOR THE STATE ACTION PAIRS
            for s_a in s_a_list:
                s = s_a[0]
                a = s_a[1]
                
                #change value of s
                player.critic.updateValue(s)

                #change eligibility of s
                player.critic.updateEligibility(s)
                
                #update policy of s_a
                player.actor.updatePolicy(s, a, player.critic.getDelta())

                #update eligibility of actor
                player.actor.updateEligibility(s,a)
            reward = player.doAction(prevA)
            s_a_list.append([prevS, prevA])



        episode_results.append(player.simWorld.pegCount)

        if player.simWorld.pegCount == 1:
            print("!!!VICTORY!!!!")
            print("it took: " + str(episode - lastWin) + " episodes to find the solution")
            lastWin = episode

        # print(player.actor.policy[3263,8])

        if episode % 1000 == 0:
            
            fig = plt.figure()
            plt.plot(episode_results)
            name = "plots/learnPlot" + str(i) + ".png"
            plt.savefig(name)
            plt.close(fig)

            res = 0
            for v in episode_results:
                res += v
            episode_results = [res/len(episode_results)]

            i +=1


        player.simWorld.resetGame() 