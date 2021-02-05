import tsplib95
import random
import matplotlib.pyplot as plt
import networkx as nx

tsp_instance = tsplib95.load('qa194.tsp')
G = tsp_instance.get_graph()
#print(tsp_instance.get_weight(1,2))

def init_tsp_pop(tsp, n):
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


# dummy fitness function 
def fitness(chrom, tsp):
    #nodes = list(tsp.get_nodes())
    fit = 0
    for i in range(len(chrom)-1):
        cost = tsp.get_weight(chrom[i], chrom[i+1])
        fit += cost
    return fit

def fitness2(chrom):
    return sum(chrom)

def fitnesses(population, tsp):
    fitnesses = []
    for i in range(len(population)):
        fitnesses.append(fitness(population[i], tsp))
    print(fitnesses)
    return fitnesses

def fitnesses2(population):
    fitnesses = []
    for i in range(len(population)):
        fitnesses.append(fitness2(population[i]))
    print(fitnesses)
    return fitnesses

def roulette(population, fitnesses, num):
    new_pop = []
    while num > 0:
        p = random.uniform(0, sum(fitnesses))
        for i, f in enumerate(fitnesses):
            if p <= 0:
                break
            p -= (1/f)
        new_pop.append(population[i]) 
        num -= 1
    print(new_pop)  
    return new_pop

def roulette2(population, fitnesses, num):
    new_pop = []
    s_fit = sum(fitnesses)
    rel_fit = [(1/i)*s_fit for i in fitnesses]
    probs = [rel_fit[i]/sum(rel_fit) for i in range(len(rel_fit))]
    print(probs)
    while num > 0:
        for i in range(len(fitnesses)):
            pass



pop = [[1,3,5,41,6], [1,5,8,4,2], [2,7,4,15,1], [6,3,9,1,2], [1,5,8,3,6], [2,4,9,3,5]]

#pop = init_tsp_pop(tsp_instance, 10)
fit = fitnesses2(pop)
roulette2(pop, fit, 4)