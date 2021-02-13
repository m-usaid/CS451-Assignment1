

##########################################################
######### PARENT SELECTION SCHEMAS (MINIMIZATION) ########
##########################################################

import random

def select_fps(population, fitnesses):
    s_fit = 0
    cum_fit = []
    for i in range(len(population)):
        cum_fit.append(s_fit + fitnesses[i])
        s_fit += fitnesses[i]
    parents = random.choices(population, cum_weights=cum_fit, k=2)
    return parents


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


