## TO DO:
#   - Implement parent selection:
#       - Random 
#   - Survivor selection schemes:
#       - Fix FPS for survivors 
#       - Random 


import tsplib95
import random
import matplotlib.pyplot as plt
import networkx as nx


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
    """Creates relative fitnesses for minimization problem.

    Args:
        population (list): Population for which relative fitnesses are calculated. 
        tsp: an instance of the TSP problem.

    Returns:
        list: Relative fitnesses for minimization. 
    """
    fits = fitnesses_tsp(population, tsp)
    rel_fit = []
    s_fit = sum(fits)
    rel_fit = [(1/i)*s_fit for i in fits]
    return rel_fit




##########################################################
######### PARENT SELECTION SCHEMA (MINIMIZATION) ######### 
##########################################################

# def select_fps(population, fitnesses):
#     ### GENERAL -> USE FOR BOTH TSP AND KNPSCK
#     """Generates parents based on fitness proportional scheme.

#     Args:
#         population (list): the population on which  FPS is applied 
#         fitnesses (list): the fitnesses of the population on which FPS will be applied. 

#     Returns:
#         list: a list of size 2 containing two parent chromosomes.
#     """
#     parents = []
#     divs = []
#     probs = [fitnesses[i]/sum(fitnesses) for i in range(len(fitnesses))]

#     s_probs = 0
#     for i in range(len(probs)):
#         divs.append(s_probs+probs[i])
#         s_probs += probs[i]
#     while len(parents) < 2:
#         r = random.uniform(0, 1)
#         for i in range(len(population)):
#             if r > divs[i] and r < divs[i+1]:
#                 parents.append(population[i]) 
#                 continue 
#     return parents 

def select_fps(population, fitnesses):
    s_fit = 0
    cum_fit = []
    for i in range(len(population)):
        cum_fit.append(s_fit + fitnesses[i])
        s_fit += fitnesses[i]
    parents = random.choices(population, cum_weights=cum_fit, k=2)
    return parents


def select_bin_tour_min(population, tsp):
    """Generates a pair of parents using binary tournament scheme.

    Args:
        population (list): Population from which parents are chosen.
        tsp: An instance of the TSP problem.

    Returns:
        [list]: A pair of parents that would reproduce. 
    """
    parents = []
    while len(parents) < 2:
        best = None 
        for i in range(2):
            ind = population[random.randint(0, len(population)-1)]
            if (best == None) or (fitness_tsp(ind, tsp) > fitness_tsp(best, tsp)):
                best = ind
        parents.append(best)
    return parents 

def rank_select_min(population, tsp):
    """Rank based selection for minimization problem (TSP).

    Args:
        population (list): Population from which parents are chosen.
        tsp: An instance of the TSP problem.

    Returns:
        [list]: A pair of parents that would reproduce. 
    """
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

  

def select_trunc_min(population, num_offspring, tsp):
    parent_pop = survivor_trunc_min(population, tsp, num_offspring * 2)
    parents = select_bin_tour_min(parent_pop, tsp)
    return parents

def select_random(population):
    parents = random.choices(population, k=2)
    return parents  


########################################
######### REPRODUCTION METHODS ######### 
########################################

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

def create_offspring_min(population, parent_sel, tsp, num_offspring):
    """Creates a list of offspring for TSP problem. 

    Args:
        population (list): Population from which offspring are going to be created.
        parent_sel (string): Parent selection scheme.
        tsp: An instance of the TSP problem.
        num_offspring (int, optional): The number of offspring that are to be created.
                                    
    Returns:
        [type]: [description]
    """
    offspring = []
    while len(offspring) < num_offspring:
        parents = []
        if parent_sel == "fps":
            rel_fit = rel_fit_min(population, tsp)
            parents = select_fps(population, rel_fit)
        elif parent_sel == "bintour":
            parents = select_bin_tour_min(population, tsp)
        elif parent_sel == "rank":
            parents = rank_select_min(population, tsp)
        elif parent_sel == "trunc":
            parents = select_trunc_min(population, num_offspring, tsp)
        elif parent_sel == "rand":
            parents = select_random(population)
        child = []
        pot_parents = random.choices(parents, k=2)
        child = crossover(pot_parents)
        offspring.append(child)
    return offspring



###############################
###### VARIATION METHODS ######
###############################

def mutate(chrom):
    ### GENERAL 
    gene1 = random.randint(0, len(chrom)-1)
    gene2 = random.randint(0, len(chrom)-1)
    tmp = chrom[gene1]
    chrom[gene1] = chrom[gene2]
    chrom[gene2] = tmp
    return chrom


def variate(offspring, p_m):
    ### GENERAL
    for i in range(len(offspring)):
        if random.uniform(0,1) < p_m:
            offspring[i] = mutate(offspring[i])  
    return offspring


#############################################
######### SURVIVOR SELECTION SCHEMA ######### 
#############################################

## NOT WORKING
# def survivor_fps(population, fitnesses, pop_size):
#     nextgen = []
#     while len(nextgen) < pop_size:
#         tmp = select_fps(population, fitnesses)
#         nextgen.append(tmp[0])
#         nextgen.append(tmp[1])
#     return nextgen

# def survivor_fps(population, fitnesses, pop_size):
#     next_gen = []
#     divs = []
#     probs = [fitnesses[i]/sum(fitnesses) for i in range(len(fitnesses))]
#     s_probs = 0
#     for i in range(len(probs)):
#         divs.append(s_probs+probs[i])
#         s_probs += probs[i]
#     while len(next_gen) < pop_size:
#         r = random.uniform(0, 1)
#         for i in range(len(population)):
#             if r > divs[i] and r < divs[i+1]:
#                 next_gen.append(population[i]) 
#                 continue 
#     return next_gen

def survivor_fps(population, fitnesses, pop_size):
    s_fit = 0
    cum_fit = []
    for i in range(len(population)):
        cum_fit.append(s_fit + fitnesses[i])
        s_fit += fitnesses[i]
    nextgen = random.choices(population, cum_weights=cum_fit, k=pop_size)
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

def survior_rank_min(population, tsp, pop_size):
    nextgen = []
    while len(nextgen) < pop_size:
        tmp = rank_select_min(population, tsp)
        nextgen.append(tmp[0])
        nextgen.append(tmp[1])
    return nextgen


def survivor_bintour_min(population, tsp, pop_size):
    nextgen = []
    while len(nextgen) < pop_size:
        best = None 
        for i in range(2):
            ind = population[random.randint(0, len(population)-1)]
            if (best == None) or (fitness_tsp(ind, tsp) < fitness_tsp(best, tsp)):
                best = ind
        nextgen.append(best)
    return nextgen

def survivor_random(population, pop_size):
    nextgen = random.choices(population, k=pop_size)
    return nextgen
        

def survivor_select_min(population, tsp, pop_size, scheme):
    nextgen = []
    if scheme == "trunc":
        nextgen = survivor_trunc_min(population, tsp, pop_size)
    elif scheme == "fps":
        rel_fit = rel_fit_min(population, tsp)
        nextgen = survivor_fps(population, rel_fit, pop_size)
    elif scheme == "bintour":
        nextgen = survivor_bintour_min(population, tsp, pop_size)
    elif scheme == "rand":
        nextgen = survivor_random(population, pop_size)
    elif scheme == "rank":
        nextgen = survior_rank_min(population, tsp, pop_size)
    return nextgen

#################################################################
#################################################################


def EA_tsp(tsp, parent_sel, surv_sel, num_gens = 2000, num_offspring = 35, p_m=0.5, pop_size=75):
    pop = init_tsp_pop(tsp_instance, pop_size)
    t = 0
    while t < num_gens:
        fits = fitnesses_tsp(pop, tsp)
        offspring = create_offspring_min(pop, parent_sel, tsp, num_offspring)
        offspring = variate(offspring, p_m)
        pop += offspring 
        fits = fitnesses_tsp(pop, tsp)
        pop = survivor_select_min(pop, tsp, pop_size, surv_sel)
        t += 1
        #print("generation {}: {}".format(t, sum(fits)/len(fits)))
        print("generation {}: {}".format(t, min(fits)))

####################################################################
####################################################################

tsp_instance = tsplib95.load('wi29.tsp')

# pop = init_tsp_pop(tsp_instance, 10)
# fit = fitnesses_tsp(pop, tsp_instance)
# print(fit)
# rfit = rel_fit_min(pop, tsp_instance)
#print(rfit)
#newpop = selectsurvivors_fps(pop, fit, 30)
#newpop = survivor_bintour_min(pop, tsp_instance, 5)
#print(fitnesses_tsp(newpop, tsp_instance))
EA_tsp(tsp_instance, "trunc", "fps")
#surv = survivor_fps(pop, rfit, 5)
#print(fitnesses_tsp(surv, tsp_instance))

