import tsplib95
import random
import matplotlib.pyplot as plt
import networkx as nx


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


def select_fps(population, fitnesses):
    """Generates a new population based on fitness proportional scheme.

    Args:
        population (list): the population on which  FPS is applied 
        fitnesses (list): the fitnesses of the population on which FPS will be applied. 

    Returns:
        list: a list of size 2 containing two parent chromosomes.
    """
    parents = []
    divs = []
    s_fit = sum(fitnesses)
    rel_fit = [(1/i)*s_fit for i in fitnesses]
    probs = [rel_fit[i]/sum(rel_fit) for i in range(len(rel_fit))]
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

def create_offspring(population, fitnesses, num_offspring = 10):
    offspring = []
    while len(offspring) < num_offspring:
        parents = []
        parents = select_fps(population, fitnesses)
        child = []
        pot_parents = random.sample(parents, 2)
        child = crossover(pot_parents)
        offspring.append(child)
    return offspring

def mutate(chrom):
    gene1 = random.randint(0, len(chrom)-1)
    gene2 = random.randint(0, len(chrom)-1)
    tmp = chrom[gene1]
    chrom[gene1] = chrom[gene2]
    chrom[gene2] = tmp
    return chrom


def variate(offspring, p_m = 0.3):
    for i in range(len(offspring)):
        if random.uniform(0,1) < p_m:
            offspring[i] = mutate(offspring[i])  
    return offspring

def selectsurvivors_fps(population, fitnesses, pop_size=30):
    nextgen = []
    while len(nextgen) < pop_size:
        tmp = select_fps(population, fitnesses)
        nextgen.append(tmp[0])
        nextgen.append(tmp[1])
    return nextgen

def survivor_trunc(population,tsp, pop_size=30):
    surv = []
    surv = sorted(population, key=lambda fit: fitness(fit, tsp))
    surv = surv[:pop_size]
    #sprint(fitnesses(surv, tsp))
    return surv

def EA(tsp, num_gens = 1000, p_m=0.5, pop_size=30):
    pop = init_tsp_pop(tsp_instance, pop_size)
    t = 0
    while t < num_gens:
        fits = fitnesses(pop, tsp)
        offspring = create_offspring(pop, fits)
        #print(fitnesses(offspring, tsp))
        offspring = variate(offspring)
        pop += offspring 
        fits = fitnesses(pop, tsp)
        pop = survivor_trunc(pop, tsp)
        t += 1
        print(min(fits))

# p1 = [1,5,4,3,8,9]
p2 = [3,7,2,1,4,5]
p = [[1,5,4,3,8,9], [3,7,2,5,4,5], [3,7,2,1,4,5]]

#tsp_instance = tsplib95.load('qa194.tsp')

#print(fitness(pop[9], tsp_instance))
# print(min(fitnesses(pop, tsp_instance)))
# fit = fitnesses(pop, tsp_instance)
# create_offspring(pop, fit)

# fit = fitnesses(pop, tsp_instance)

#print(survivor_trunc(p))

tsp_instance = tsplib95.load('wi29.tsp')
pop = init_tsp_pop(tsp_instance, 50)
#survivor_trunc(pop, tsp_instance)
EA(tsp_instance)