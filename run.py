import itertools
import random
import numpy as np

# 0 = defect
# 1 = cooperate
N = 3 # number of agents playing prisoner's dilemma
iterations = 3 # how many time steps to run the simulation

# initialize blank array to hold histories
histories = np.empty((N))
histories[:] = [np.nan]

# define the agent class
class Agent:
    def __init__(self, id):
        self.id = id
        self.memory = 1
        self.histories = self.initializeHistories()
        self.strategy = random.choice([[0, 0], [0, 1], [1, 0], [1, 1]])
        self.sequences = self.generateGeneticSequences()

    def initializeHistories(self):
        histories = [[np.nan] for h in range(N)]
        return histories

    def generateGeneticSequences(self):
        lst = list(itertools.product([0, 1], repeat=self.memory))
        sequences = [list(s) for s in lst]
        return sequences

    def lookupOpponentHistory(self, id):
        return self.histories[id]

    def recordOpponentHistory(self, opponentId, opponentAction):
        # remove the oldest action (unless the length of history changed)
        if len(self.histories[opponentId]) == self.memory:
            del self.histories[opponentId][0]
        else:
            pass

        # append the latest action
        self.histories[opponentId].append(opponentAction)

    def performAction(self, history):
        if history == None or np.isnan(history): # initial move (no history between these two players exist yet)
            return self.strategy[0] 
        else:
            try:
                policy = self.sequences.index(history)
                action = self.strategy[policy]
                return action
            except Exception as ex:
                print("Exception occured on agent " + str(self.id) + " with history " + str(history) + " and Exception type " + str(type(ex)))
    
# intialize the agents
agents = []
for i in range(N):
    a = Agent(i)
    agents.append(a)

def calculatePayoff(player_action, opponent_action):
    payoff_matrix = np.array([[(3, 3), (0, 5)], [(5, 0), (1, 1)]]) # classic prisoner's dilemma payoff
    return tuple(payoff_matrix[player_action][opponent_action])

# play the game
def step():
    # iterate through so each agent plays every other agent in each round
    for player in agents:
        for opponent in agents[player.id + 1:]:
            # Lookup history against that player
            p_history = player.lookupOpponentHistory(opponent.id)
            o_history = opponent.lookupOpponentHistory(player.id)

            # Perform action given the history
            print("player #" + str(player.id) + " performs action " + str(player.performAction(p_history)) + " against player #" + str(opponent.id) \
            + " | playing strategy: " + str(player.strategy))
            print("player #" + str(opponent.id) + " performs action " + str(opponent.performAction(o_history)) + " against player #" + str(player.id) \
            + " | playing strategy: " + str(opponent.strategy))
            player_action = player.performAction(p_history)
            opponent_action = opponent.performAction(o_history)

            # Record history of this game
            player.recordOpponentHistory(opponent.id, opponent_action)
            opponent.recordOpponentHistory(player.id, player_action)

            calculatePayoff(player_action, opponent_action)
for i in range(iterations):
    print("### Round " + str(i) + " ###")
    step()