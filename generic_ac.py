from simplePlayer import SimplePlayer
import time
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import collections
import gc
import gym


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


    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
    dqn_solver = DQNSolver(observation_space, action_space)
    while True:
        state = env.reset()
        state = np.reshape(state, [1, observation_space])
        while True:
            env.render()
            action = dqn_solver.act(state)
            state_next, reward, terminal, info = env.step(action)
            reward = reward if not terminal else -reward
            state_next = np.reshape(state_next, [1, observation_space])
            dqn_solver.remember(state, action, reward, state_next, terminal)
            dqn_solver.experience_replay()
            state = state_next
            if terminal:
                break
        

if __name__ == "__main__":

    env = "peg-solitaire"
    player = SimplePlayer(
    #Hyperparameters for learning:
    gamma = 0.9, lamda = 0.9, alpha_a = 0.1, alpha_c = 0.1, epsilon = 0.5, 
    #Rewards for winning and losing:
    winReward = 100, loseReward = -10,
    env = env,
    #BoardType and size:
    boardSize = 5, boardType = "triangle", visualization = True, initial_position = [0,0]
    )


    epsilon_0 = player.epsilon

    numEpisodes = 20000
    test_every_x_episode = 50
    plot_and_save_every_x_episode = test_every_x_episode*10

    episode = 0
    peg_sum = 0
    episode_results = []
    i = 0
    policy_wins = 0
    policy_games = 0
    policy_tests = {}
    this_time = timer()
    last_time = time.time()


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

            this_time = time.time()
            print("Time since last step: " + str(this_time - last_time))
            last_time = this_time

            gc.collect()


            # episode_results.append(peg_sum/test_every_x_episode)
            peg_sum = 0

        if episode % plot_and_save_every_x_episode == 0:
            i += 1

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