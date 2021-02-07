import tsplib95
import random
import matplotlib.pyplot as plt
import networkx as nx

tsp_instance = tsplib95.load('qa194.tsp')
G = tsp_instance.get_graph()

def init_tsp_pop(tsp, n):
    """ Selects random complete tours from the TSP problem 
    to create the initial population.

    Args:
        tsp:  an instance of the TSP problem
        n: the size of the initial population required

    Returns:
        list: a list of random Hamiltonian tours of the TSP complete graph.
    """    
    pop = []
    nodes = list(tsp.get_nodes())
    random_path = []
    p_len = len(nodes)
    for i in range(n):
        temp_nodes = list(tsp.get_nodes())
        random_path = []
        for j in range(p_len):
            x = random.choice(temp_nodes)
            random_path.append(x)
            temp_nodes.remove(x)
        pop.append(random_path)
    return pop


def fitness(chrom, tsp):
    """ Calculates the fitness of a single chromosome 
    of the TSP problem. 

    Args:
        chrom: a chromosome from the population 
        tsp: an instance of the TSP problem

    Returns:
        int: the cost (fitness) of the path
    """

    fit = 0
    for i in range(len(chrom)-1):
        cost = tsp.get_weight(chrom[i], chrom[i+1])
        fit += cost
    return fit

def fitnesses(population, tsp):
    """Creates a list of fitnesses of the population.

    Args:
        population: the population whose fitnesses need to be calculated.
        tsp: the instance of the TSP problem. 

    Returns:
        list: a list of fitnesses of the population.
    """
    fitnesses = []
    for i in range(len(population)):
        fitnesses.append(fitness(population[i], tsp))
    return fitnesses

def roulette2(population, fitnesses):

    new_pop = []
    divs = []
    s_fit = sum(fitnesses)
    rel_fit = [(1/i)*s_fit for i in fitnesses]
    probs = [rel_fit[i]/sum(rel_fit) for i in range(len(rel_fit))]
    s_probs = 0
    num = len(population)
    for i in range(len(probs)):
        divs.append(s_probs+probs[i])
        s_probs += probs[i]
    while len(new_pop) < 15:
        r = random.uniform(0, 1)
        for i in range(len(population)):
            if r > divs[i] and r < divs[i+1]:
                new_pop.append(population[i])
    return new_pop

pop = init_tsp_pop(tsp_instance, 15)
fit = fitnesses(pop, tsp_instance)
roulette2(pop, fit)

def EA_TSP():
    pass