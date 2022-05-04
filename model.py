
import numpy as np

# agents = [[0, 0], [0, 0], [1, 1], [1, 0], [0, 1]]
# genotypes = [[0, 0], [1, 1], [1, 0], [0, 1]]

# genotype_matrix = [
# 
# 
# ]
# dw (from paper) is probability of agent growing or dying.


# Each agent has three variables:
# 1. the length of its memory
# 2. its current strategy encoded as a genome
# 3. a memory matrix of gameplay against each opponent
# Example agent in a 3 player system:
# agent = {
#   "id": 0 
#   "memory": 1,
#   "genome": [0, 1] # this is tit=for-tat strategy
#   "memory_matrix": {
#       "1": [0],
#       "2": [1],
#   }
# }
#
#
# agent = {
#   "id": 1 
#   "memory": 2,
#   "genome": [0, 1, 0, 0] # this is tit=for-tat strategy
#   "memory_history": {
#       "1": [0, 0],
#       "2": [1, 1],
#   }
# }
#
# list of agents
# 2 agents
# [0, 1] | [1, 0, 1, 0]
# 1 | 2
# 0 | 1 - [1] | [0]
# 
# 
#

# Mechanism functions
def calculatePayoff():
    pass

def calculatePayoff(player_action, opponent_action):
    payoff_matrix = np.array([[(3, 3), (0, 5)], [(5, 0), (1, 1)]]) # classic prisoner's dilemma payoff
    return tuple(payoff_matrix[player_action][opponent_action])

def calculateFitness():
    pass

# Mutations of strategy
def reproduce():
    pass

def mutate():
    pass

def split():
    pass

# Simulation
def initialize():
    global population
    population = []

    for i in range(N):
        agent = {
            "id": i,
            "memory_length": 1,
            "genome": [0,1],
            "memory_history": {}
        }

        # initialize blank memory history against every other agent
        for j in range(N):
            agent["memory_history"][j] = None
        
        # add agent to the population
        population.append(agent)
    
def step():
    # each agent competes against each other agent
    for i in population:
        for j in population[i["id"] + 1:]:
            # look up history against that agent before selecting response.
            i_history_j = i["memory_history"][j]
            j_history_i = j["memory_history"][i]

            # take action
            i_action = None
            j_action = None

            # calculate payout
            payout = compete(i_action, j_action) # returns tuple (5, 0), etc
            
            # adjust individual fitness for agent i and j
            i["fitness"] += payout[0]
            j["fitness"] += payout[1]

    # calculate average fitness across all agents
    fitness_avg = sum([agent["genome"] for agent in population]) / len(population)

    # identify probability of each agent to reproduce or die (based on growth rate d and fitness).
    # for example s = 50. agent 0 si=45. d=0.1. wi = 45 - 50 = -5. d * wi = -0.5 (agent will die with 50% chance).
     
    d = 0.1


    # Case: agent dies
    # erase this agent from the list of agents (population).

    # Case: agent reproduces
    # assign new id to new agent, add that agent to the population. create empty memory list for the new agent in every other agent's memory.
    # when new agent is reproduced, apply genome mutations with defined probability parameters.


def run():
    pass


# Note for El Farol.
# Payoff could be the average performance of 7 (or some other amount) steps. Then simulate many rounds of 7 step iterations. (this makes the performance gradual instead of binary "happy" or "sad" for each round).

if __name__ == "__main__":
    
    N = 5

    initialize()

    print(population)
