import tsplib95
import random

tsp_instance = tsplib95.load('qa194.tsp')
#G = tsp_instance.get_graph()

def init_tsp_pop(tsp):
    nodes = list(tsp.get_nodes())
    print(nodes)

# dummy fitness function 
def fitness(chrom):
    fit = 0
    for i in chrom:
        fit += i
    return fit

def fitnesses(population):
    fitnesses = []
    for chrom in population:
        fitnesses.append(fitness(chrom))
    return fitnesses


def roulette(population, fitnesses, num):
    new_pop = []
    while num > 0:
        p = random.uniform(0, sum(fitnesses))
        for i, f in enumerate(fitnesses):
            print(i, f)
            if p <= 0:
                break
            p -=f
        new_pop.append(population[i]) 
        num -= 1
    return new_pop  


#pop = [[1,3,5,41,6], [1,5,8,4,2], [2,7,4,15,1], [6,3,9,1,2], [1,5,8,3,6], [2,4,9,3,5]]
#fit = fitnesses(pop)

init_tsp_pop(tsp_instance)