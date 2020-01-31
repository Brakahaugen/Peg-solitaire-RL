import math
import sys
import numpy as np
from hexgames.hexGrid import HexGrid
from simWorld import SimWorld
import random
import time


class Critic:
    def __init__(self, grid):
        self.V = {} #V(s)
        self.e = {} #e(s)

class Actor:
    def __init__(self, grid):
        self.policy = {} #Policy(s,a)
        self.e = {} #e(s,a)

    def predict(self, s, actions):
        probs = []
        for a in actions:
            print((s, a))
            if (s, a) in self.policy:
                probs.append(self.policy[s,a])
            else: 
                self.policy[(state,a)] = 0
                probs.append(0)
        return probs





class SimplePlayer:
    def __init__(self):
        self.simWorld = SimWorld(5, "triangle")
        self.critic = Critic(self.simWorld.hexGrid)
        self.actor = Actor(self.simWorld.hexGrid)
        self.numEpisodes = 100



    def choose_action(self):
        state = self.simWorld.createSimpleState()
        actions = self.simWorld.getValidActions()
        print(state)

        # probabilities = self.actor.predict(state, actions)
        action = random.choice(self.simWorld.getValidActions())
        return action
    
    def doAction(self, action):
        self.simWorld.updateGame(action)



class Player:
    def __init__(self, simWorld, alpha, beta, gamma=0.99, n_actions=4, layer1_size=1024, layer2_size=512, input_dims=8):
        self.gamma = gamma
        self.alpha = alpha
        self.beta = beta
        self.input_dims = input_dims
        self.fc1_dims = layer1_size
        self.fc2_dims = layer2_size
        self.n_actions = n_actions

        self.actor, self.critic, self.policy = self.build_actor_critic_network()
        self.action_space = [i for i in range(self.n_actions)]
        self.simWorld = simWorld

        self.actor, self.critic = build_actor_critic_network()

    def build_actor_critic_network(self):
        # input = Input(shape=(self.input_dims,))
        # delta = Input(shape=[1])
        # dense1 = Dense(self.fc1_dims, activation='relu')(input)
        # dense2 = Dense(self.fc2_dims, activation='relu')(dense1)
        # probs = Dense(self.n_actions, activation='softmax')(dense2)
        # values = Dense(1, activation='linear')(dense2)

        # def custom_loss(y_true, y_pred):
        #     out = K.clip(y_pred, 1e-8, 1-1e-8)
        #     log_lik = y_true*K.log(out)

        #     return K.sum(-log_lik*delta)

        actor = Actor()

        critic = Critic(self.simWorld.hexGrid)
        
        return actor, critic

    def choose_action(self):
        state = self.simWorld
        # probabilities = self.policy.predict(state)[0]
        action = np.random.choice()
        return action
    
    def learn(self, state, action, reward, state_, done):
        state = state[np.newaxis, :]
        state_ = state_[np.newaxis, :]

        critic_value_ = self.critic.predict(state_)
        critic_value = self.critic.predict(state)

        target = reward + self.gamma*critic_value_*(1-int(done))
        delta = target - critic_value

        actions = np.zeros([1, self.n_actions])
        actions[np.arrange(1), action] = 1.0

        self.actor.fit([state, delta], actions, verbose=0)
        self.critic.fit(state, target, verbose=0)



if __name__ == "__main__":


    player = SimplePlayer()
    numEpisodes = 1000
    episode = 0

    while episode < numEpisodes:
        episode += 1

        while not player.simWorld.isFinished:
            action = player.choose_action()
            player.doAction(action)
            