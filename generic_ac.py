from agent import Agent
from actor_and_critic import *
from simWorld import SimWorld
import time
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import collections
import gc
import gym
import numpy as np


def init_training(agent,
    numEpisodes = 200,
    test_every_x_episode = None,
    plot_and_save_every_x_episode = None):

    # Setting up a test periodically if frequency is not specified
    if test_every_x_episode == None:
        test_every_x_episode = numEpisodes / 100
    if plot_and_save_every_x_episode == None:
        plot_and_save_every_x_episode = numEpisodes

    #Initializing variables for tracking training and loss and episodes and peg_sums
    episode = 0
    peg_sum = 0
    episode_results = []
    save_step = 0
    policy_tests = {}
    policy_tests[0] = 0
    this_time = timer()
    last_time = time.time()
    epsilon_0 = agent.epsilon



    while episode < numEpisodes:

        episode += 1

        #Resets the world at every new episode
        agent.simWorld.reset() 

        #Adjusts epsilon dynamically (Falls linearly down to zero.).
        agent.epsilon = epsilon_0 - ((epsilon_0*episode) / numEpisodes)

        #Runs the main algorithm (The "repeat for each step of the episode ")
        generic_actor_critic(agent)

        #Logging the results
        peg_sum += (agent.simWorld.pegCount)
        episode_results.append(agent.simWorld.pegCount)
        
        if episode % test_every_x_episode == 0:

            policy_test = run_policy_test(agent)
            policy_tests[episode] = policy_test
            
            print("we are now at episode: " + str(episode))
            print("Our current policy has a winrate of: " + str(policy_test))

            this_time = time.time()
            print("Time since last step: " + str(this_time - last_time))
            last_time = this_time

            gc.collect()
            peg_sum = 0

        if episode % plot_and_save_every_x_episode == 0:
            save_step += 1
            save_training_plot(policy_tests, episode_results, save_step)

    #At the end we run a loop of tests
    agent.simWorld.visualizationOn = True
    while True:
        run_policy_test(agent)



def generic_actor_critic(agent):

    #Init s and a
    prevS = agent.simWorld.createSimpleState()
    prevA = agent.choose_action()        

    s_a_list =[]
    #If there is no valid moves from the start
    if agent.simWorld.checkGameFinished():
        return

    s_a_list.append([prevS, prevA])

    while not agent.simWorld.isFinished:
        #1. Do action a from prevS, mote to s' and receive reward r
        reward = agent.doAction(prevA)
        s_ = agent.simWorld.createSimpleState()

        #2. find the action based on the current state:
        a_ = agent.choose_action()
        
        #3. Update the actors eligibility trace
        agent.actor.e[s_,a_] = 1

        #4. Update the delta for the critic
        agent.critic.updateDelta(reward, prevS, s_)
        
        #5. Update the eligibility traces for the critic:
        agent.critic.e[prevS] = 1

        #6. For each state action in episode:
        for s_a in s_a_list:
            s = s_a[0]
            a = s_a[1]

            #a) change value of s
            delta_value = agent.critic.updateValue(s)

            #b) change eligibility of s
            agent.critic.updateEligibility(s)
            
            #c) update policy of s_a
            delta_update = agent.actor.updatePolicy(s, a, agent.critic.getDelta())

            #d) update eligibility of actor
            agent.actor.updateEligibility(s,a)

        #7.
        prevS = s_
        prevA = a_
        s_a_list.append([prevS, prevA])

def run_policy_test(Agent):
    numEpisodes = 1
    episode = 0
    s_a_list =[]
    wins = 0
    
    agent.epsilon = 0

    while episode < numEpisodes:
        agent.simWorld.reset() 
        episode += 1
        while not agent.simWorld.isFinished and len(agent.simWorld.getValidActions()) != 0:
            prevA = agent.choose_action()        
            reward = agent.doAction(prevA)

        if agent.simWorld.pegCount == 1:
            wins += 1


    return wins/numEpisodes


def save_training_plot(
    policy_tests: dict, 
    episode_results: dict,
    save_step: int
    ):

    criticor = "NA"
    x = []
    y = []
    od = collections.OrderedDict(sorted(policy_tests.items()))

    for key, value in od.items():
        print(key, value)
        x.append(key)
        y.append(value)
    



    fig = plt.figure()
    plt.title('On policy learning rate')
    plt.xlabel('Episode')
    plt.ylabel('On policy winrate')
    plt.plot(x,y)
    name = "plots/["+ "]learning_rate" + str(save_step) + str(criticor) + ".png"
    plt.savefig(name)
    plt.close(fig)

    fig = plt.figure()
    plt.title('Win plot')
    plt.xlabel('Episode')
    plt.ylabel('Remaining pegs at finish')
    plt.plot(episode_results)
    name = "plots/[" + "]final_learnPlot" + str(save_step) + str(criticor) + ".png"
    plt.savefig(name)
    plt.show(fig)
    plt.close(fig)    


if __name__ == "__main__":

    #Setting up the objects. Specify your hyperparameters here.
    env = SimWorld(size = 4, type = "diamond", visualization = False, winReward = 1, loseReward = -0.1, initialPosition = [2,1])
    
    critic = Critic(simWorld = env, gamma = 0.9, lamda = 0.9, alpha = 0.01)

    neuralCritic = NeuralCritic(simWorld = env, gamma = 0.9, lamda = 0.9, alpha = 0.01, layers = [15, 20, 30, 5, 1])

    actor = Actor(simWorld = env, gamma = 0.9, lamda = 0.9, alpha = 0.01)
    
    agent = Agent(env, actor, neuralCritic, epsilon = 0.5)

    init_training(agent,
    numEpisodes = 50,
    test_every_x_episode = None,
    plot_and_save_every_x_episode = None
    )