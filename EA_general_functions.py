

##########################################################
######### PARENT SELECTION SCHEMAS (MINIMIZATION) ########
##########################################################

import random
from copy import deepcopy

def cum_fitness(population,fitnesses):
    s_fit = 0
    cum_fit = []
    for i in range(len(population)):
        cum_fit.append(s_fit + fitnesses[i])
        s_fit += fitnesses[i]
    return cum_fit

def select_fps(population, fitnesses, num=2, cum_fit = None):
    if cum_fit == None:
        cum_fit = cum_fitness(population,fitnesses)

    parents = random.choices(population, cum_weights=cum_fit, k=num)
    return parents

def select_random(population, num=2):
    return random.choices(population, k=num)

def select_truncation(pop,num):
    truncPop = deepcopy(pop)
    truncPop.sort(key=lambda x: x[0],reverse=True)
    truncPop = pop[:num+1]

    return truncPop

def select_rbs(pop,num):
    returnPop = deepcopy(pop)
    returnPop.sort(key=lambda x: x[0])
    cum_fit = [x for x in range(1,len(pop)+1)]
    returnPop = random.choices(returnPop, cum_weights=cum_fit, k=num)

    return returnPop

def crossover(parent: list):
    ### GENERAL METHOD 
    """Crossover method to create child chromosome.

    Args:
        parent (list): A list of size 2 containing the parent chromosomes.

    Returns:
        [list]: A new child chromosome.
    """
    child1 = []
    child2 = []
    child = []
    geneA = int(random.random() * len(parent[0]))
    geneB = int(random.random() * len(parent[0]))
    startgene = min(geneA, geneB)
    endgene = max(geneA, geneB)
    for i in range(startgene, endgene):
        child1.append(parent[0][i])
    child2 = [item for item in parent[1] if item not in child1]
    child = child2[:startgene] + child1 + child2[startgene:]
    return child 


