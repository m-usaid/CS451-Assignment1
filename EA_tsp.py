import tsplib95
import random
import matplotlib.pyplot as plt
import networkx as nx
from math import fsum

#############################################
######### POPULATION INITIALIZATION ######### 
#############################################

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


def init_knpsk_pop():
    pass

######################################
######### FITNESS EVALUATION ######### 
######################################


def fitness_tsp(chrom, tsp):
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

def fitnesses_tsp(population, tsp):
    """Creates a list of fitnesses of the population.

    Args:
        population: the population whose fitnesses need to be calculated.
        tsp: the instance of the TSP problem. 

    Returns:
        list: a list of fitnesses of the population.
    """
    fitnesses = []
    for i in range(len(population)):
        fitnesses.append(fitness_tsp(population[i], tsp))
    return fitnesses


def rel_fit_min(population, tsp):
    fits = fitnesses_tsp(population, tsp)
    rel_fit = []
    s_fit = sum(fits)
    rel_fit = [(1/i)*s_fit for i in fits]
    return rel_fit

def fitness_knpsk():
    pass


def fitnesses_knpsk():
    pass

#################################################################
#################################################################   


##########################################################
######### PARENT SELECTION SCHEMA (MINIMIZATION) ######### 
##########################################################

def select_fps(population, fitnesses):
    """Generates parents based on fitness proportional scheme.

    Args:
        population (list): the population on which  FPS is applied 
        fitnesses (list): the fitnesses of the population on which FPS will be applied. 

    Returns:
        list: a list of size 2 containing two parent chromosomes.
    """
    parents = []
    divs = []
    probs = [fitnesses[i]/sum(fitnesses) for i in range(len(fitnesses))]

    s_probs = 0
    for i in range(len(probs)):
        divs.append(s_probs+probs[i])
        s_probs += probs[i]
    while len(parents) < 2:
        r = random.uniform(0, 1)
        for i in range(len(population)):
            if r > divs[i] and r < divs[i+1]:
                parents.append(population[i]) 
                continue 
    return parents 

def select_bin_tour_min(population, tsp):
    parents = []
    while len(parents) < 2:
        best = None 
        for i in range(2):
            ind = population[random.randint(0, len(population)-1)]
            if (best == None) or (fitness_tsp(ind, tsp) < fitness_tsp(best, tsp)):
                best = ind
        parents.append(best)
    return parents 

def rank_select(population, tsp):
    parents = []
    pop = sorted(population, key=lambda fit: fitness_tsp(fit, tsp), reverse=True)
    N = len(pop)
    totalrank = N*(N+1) / 2
    
    probs = []
    divs = []
    s_probs = 0
    
    for i in range(1, len(pop)+1):
        probs.append(i/totalrank)

    for i in range(len(probs)):
        divs.append(s_probs+probs[i])
        s_probs += probs[i]
    while len(parents) < 2:
        r = random.uniform(0, 1)
        for i in range(len(pop)):
            if r > divs[i] and r < divs[i+1]:
                parents.append(pop[i]) 
                continue 
    return parents 
        

# def select_trunc_min(population, num, tsp):
#     surv = []
#     surv = sorted(population, key=lambda fit: fitness_tsp(fit, tsp))
#     surv = surv[:num]
#     return surv

#################################################################
#################################################################



########################################
######### REPRODUCTION METHODS ######### 
########################################

def crossover(parent: list):
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

def create_offspring(population, fitnesses, parent_sel, tsp, num_offspring = 10):
    offspring = []
    while len(offspring) < num_offspring:
        parents = []
        if parent_sel == "fps":
            rel_fit = rel_fit_min(population, tsp)
            parents = select_fps(population, rel_fit)
        elif parent_sel == "tourny":
            parents = select_bin_tour_min(population, tsp)
        elif parent_sel == "rank":
            parents = rank_select(population, tsp)
        child = []
        pot_parents = random.sample(parents, 2)
        child = crossover(pot_parents)
        offspring.append(child)
    return offspring

#################################################################
#################################################################

###############################
###### VARIATION METHODS ######
###############################

def mutate(chrom):
    gene1 = random.randint(0, len(chrom)-1)
    gene2 = random.randint(0, len(chrom)-1)
    tmp = chrom[gene1]
    chrom[gene1] = chrom[gene2]
    chrom[gene2] = tmp
    return chrom


def variate(offspring, p_m):
    for i in range(len(offspring)):
        if random.uniform(0,1) < p_m:
            offspring[i] = mutate(offspring[i])  
    return offspring

#################################################################
#################################################################


#############################################
######### SURVIVOR SELECTION SCHEMA ######### 
#############################################

## NOT WORKING
def selectsurvivors_fps(population, fitnesses, pop_size):
    nextgen = []
    while len(nextgen) < pop_size:
        tmp = select_fps(population, fitnesses)
        nextgen.append(tmp[0])
        nextgen.append(tmp[1])
    return nextgen

def survivor_trunc_min(population,tsp, pop_size):
    """Truncation based survivor scheme.

    Args:
        population (list): The population from which survivors are chosen.
        tsp: An instance of the TSP problem.
        pop_size (int, optional): The population size that is maintained in the EA. Defaults to 30.

    Returns:
        [list]: A list of survivors that will be the population for the next generation.
    """
    surv = []
    surv = sorted(population, key=lambda fit: fitness_tsp(fit, tsp))
    surv = surv[:pop_size]
    return surv

def survior_rank_based():
    pass

def survivor_select_min(population, fitnesses, tsp, pop_size, scheme):
    nextgen = []
    rel_fit = rel_fit_min(population, tsp)
    if scheme == "trunc":
        nextgen = survivor_trunc_min(population, tsp, pop_size)
    elif scheme == "fps":
        nextgen = selectsurvivors_fps(population, rel_fit, pop_size)
    return nextgen

#################################################################
#################################################################


def EA(tsp, parent_sel, surv_sel, num_gens = 100, p_m=0.3, pop_size=30):
    pop = init_tsp_pop(tsp_instance, pop_size)
    t = 0
    while t < num_gens:
        fits = fitnesses_tsp(pop, tsp)
        offspring = create_offspring(pop, fits, parent_sel, tsp)
        offspring = variate(offspring, p_m)
        pop += offspring 
        fits = fitnesses_tsp(pop, tsp)
        #pop = survivor_trunc_min(pop, tsp, pop_size)
        pop = survivor_select_min(pop, fits, tsp, pop_size, surv_sel)
        t += 1
        #print("generation {}: {}".format(t, sum(fits)/len(fits)))
        print("generation {}: {}".format(t, min(fits)))

####################################################################
####################################################################

# # p1 = [1,5,4,3,8,9]
# p2 = [3,7,2,1,4,5]
# p = [[1,5,4,3,8,9], [3,7,2,5,4,5], [3,7,2,1,4,5]]

tsp_instance = tsplib95.load('wi29.tsp')

pop = init_tsp_pop(tsp_instance, 50)
fit = fitnesses_tsp(pop, tsp_instance)
#print(select_fps_min(pop, fit))
newpop = selectsurvivors_fps(pop, fit, 30)
#print(fitnesses_tsp(newpop, tsp_instance))
#print(rank_select(pop, tsp_instance))
#print(select_bin_tour_min(pop, tsp_instance))
# #survivor_trunc(pop, tsp_instance)
EA(tsp_instance, "rank", "trunc")