
import numpy as np
import random
import itertools

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

# Memory machine to optimize strategy lookups
# every time an agent with memory m is introduced to
# the population, the set of all possible histories
# for that m value is added to this data structure.

def generateSequences(n):
        lst = list(itertools.product([0, 1], repeat=n))
        sequences = [s for s in lst]
        return sequences

M = {
    "1": generateSequences(1)
}

# Mechanism functions
# Calculate payoff

# Calculate fitness

# 
# Mutations of strategy
def duplicate(sequence):
    def flatten(t):
        return [item for sublist in t for item in sublist]

    sequence = flatten([sequence, sequence])
    return sequence # duplication occured

def mutate(sequence, p):
    def flip(bit):
        if random.uniform(0,1) <= p:
            print("flipperoo")
            return (bit + 1) % 2
        else:
            return bit

    sequence = tuple(flip(b) for b in sequence)
    return sequence


def split(sequence):
    if len(sequence) == 2:
        return sequence
    else:
        if random.uniform(0,1) <= 0.5:
            return sequence[:int(len(sequence) / 2)]
        else:
            return sequence[int(len(sequence) / 2):]       

# Simulation
def initialize():
    global population
    population = []

    for i in range(N):
        agent = {
            "id": i,
            "memory_length": 1,
            "genome": random.choice([(0,0), (0,1), (1,0), (1,1)]),
            "fitness": 0,
            "memory_history": {}
        }

        # initialize blank memory history against every other agent
        for j in range(N):
            agent["memory_history"][j] = None
        
        # add agent to the population
        population.append(agent)

def compete(a, b):
    payoff = np.array(
        # classic prisoner's dilemma payoff
        [
            [(3, 3), (0, 5)], 
            [(5, 0), (1, 1)]
        ]    
    )

    result = tuple(payoff[a][b])
    return result

def action(history, strategy):
    global M
    if history == None: # initial move
        return strategy[0]
    else:
        try:
            memory = len(history)
            policy = M[str(memory)]
            action = strategy[policy.index(tuple(history))]
            return action
        except Exception as ex:
            print(ex)
            print("weird thing happening in action function")

def step():
    # each agent competes against each other agent
    for i in population:
        for j in population[i["id"] + 1:]:
            # look up history against that agent before selecting response.
            try:
                i_history_j = i["memory_history"][j["id"]]
            except:
                # if there's no history between these players intialize as None
                i["memory_history"][j["id"]] = None
                i_history_j = None
            try:
                j_history_i = j["memory_history"][i["id"]]
            except:
                j["memory_history"][i["id"]] = None
                j_history_i = None

            # take action
            i_action = action(i_history_j, i["genome"])
            j_action = action(j_history_i, j["genome"])

            if i_action is None:
                print("weird i_action is none problem")
                print("player i: ", i)
                print("player j: ", j)
            # record opponent history
            ## check for initial round against this opponent
            
            ## player i
            # first, if there's no history, initialize a blank history
            if i["memory_history"][j["id"]] == None:
                i["memory_history"][j["id"]] = []
            
            # then record histories and manage memory
            i["memory_history"][j["id"]].append(i_action) # first the player's own action
            i["memory_history"][j["id"]].append(j_action) # then the opponent's action
            
            # delete old memories
            while len(i["memory_history"][j["id"]]) > i["memory_length"]:
                del i["memory_history"][j["id"]][0]

           ## player j
            # first, if there's no history, initialize a blank history
            if j["memory_history"][i["id"]] == None:
                j["memory_history"][i["id"]] = []
            
            # then record histories and manage memory
            j["memory_history"][i["id"]].append(j_action) # first the player's own action
            j["memory_history"][i["id"]].append(i_action) # then the opponent's action
            
            # delete old memories
            while len(j["memory_history"][i["id"]]) > j["memory_length"]:
                del j["memory_history"][i["id"]][0]

            # calculate payout
            payout = compete(i_action, j_action) # returns tuple (5, 0), etc
            if not isinstance(payout, tuple):
                print("something weird.")

            # adjust individual fitness for agent i and j
            i["fitness"] += int(payout[0])
            if not isinstance(i["fitness"], int):
                print("something weird.")
            j["fitness"] += int(payout[1])

            # clear payout
            del payout, i_action, j_action, i_history_j, j_history_i
    # calculate average fitness across all agents
    fitness_avg = sum([agent["fitness"] for agent in population]) / len(population)

    # identify probability of each agent to reproduce or die (based on growth rate d and fitness).
    d = 0.1

    for agent in population:
        fitness = agent["fitness"] - fitness_avg
        
        if fitness >= 0:
            # for example s = 50. agent 0 si=55. d=0.1. wi = 55 - 50 = 5. d * wi = 0.5 (agent will reproduce with 50% chance).
            # calculate probability this agent reproduces
            reproduce = random.uniform(0, 1) <= (1 - d * fitness)
            
            if (reproduce):
                # make a copy of the agent
                new_agent = {
                    "id": max([a["id"] for a in population]) + 1,
                    "memory_length": agent["memory_length"], # make a copy
                    "genome": agent["genome"],               # make a copy
                    "fitness": 0,
                    "memory_history": {}
                }
                # apply mutations randomly
                p_duplicate = pow(10, -5)
                # p_duplicate = 1
                p_mutate = 2 * pow(10, -5)
                # p_mutate = 1
                p_split = pow(10, -5)

                # p_split = 1
                
                # duplicate
                if random.uniform(0, 1) <= p_duplicate:
                    new_agent["genome"] = duplicate(new_agent["genome"])
                    new_agent["memory_length"] += 1
                
                # mutate
                new_agent["genome"] = mutate(new_agent["genome"], p_mutate)
                
                # split
                if random.uniform(0, 1) <= p_split:
                    new_agent["genome"] = split([1,0,0,1])
                    new_agent["memory_length"] -= 1    

                # add to population
                population.append(new_agent)                
            
        else: # fitness is less than 0
            # for example s = 50. agent 0 si=45. d=0.1. wi = 45 - 50 = -5. d * wi = -0.5 (agent will die with 50% chance).
            die = random.uniform(0, 1) <= d * abs(fitness)
            
            if (die):
                # remove from the population
                population[:] = [a for a in population if a.get('id') != agent["id"]]

    # Case: agent dies
    # erase this agent from the list of agents (population).

    # Case: agent reproduces
    # assign new id to new agent, add that agent to the population. create empty memory list for the new agent in every other agent's memory.
    # when new agent is reproduced, apply genome mutations with defined probability parameters.


def run():
    for i in range(6000):
        print("iteration: ", i)
        # count unique genomes
        # genomes = [list(genome) for genome in set([tuple(agent["genome"]) for agent in population])]
        genomes = [agent["genome"] for agent in population]
        genome_counts = dict((g, genomes.count(g)) for g in genomes)
        print(genome_counts)
        step()

# Note for El Farol.
# Payoff could be the average performance of 7 (or some other amount) steps. Then simulate many rounds of 7 step iterations. (this makes the performance gradual instead of binary "happy" or "sad" for each round).

if __name__ == "__main__":
    
    N = 1000

    initialize()
    run()

    # print(population)
