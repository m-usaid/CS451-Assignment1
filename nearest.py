import tsplib95
import random

tsp_instance = tsplib95.load('qa194.tsp')
G = tsp_instance.get_graph()

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

# def roulette(population, fitnesses, num):
#     sum_fit = 0
#     degs = 0 
#     deg_int = []
#     new_pop = []
#     for chrom in population:
#         sum_fit += fitness(chrom)
#     for chrom in population:
#         prob = ((fitness(chrom) * 360) / sum_fit)
#         degs += prob
#         deg_int.append(degs-prob) 
#     print(deg_int)
    
#     while num > 0 :
#         r = random.uniform(0, 360)
#         print(r)
#         for i in range(len(population)):
#             if i < len(population) - 1:
#                 if r > deg_int[i] and r < deg_int[i+1]:
#                     new_pop.append(population[i])
#                     break
#             else:
#                 print("what")
#         num -= 1
#     print(new_pop)

def roulette(population, fitnesses, num):
    new_pop = []
    while num > 0:
        p = random.uniform(0, sum(fitnesses))
        for i, f in enumerate(fitnesses):
            if p <= 0:
                break
            p -=f
        new_pop.append(population[i]) 
        num -= 1
    return new_pop  

pop = [[1,3,5,41,6], [1,5,8,4,2], [2,7,4,15,1], [6,3,9,1,2], [1,5,8,3,6], [2,4,9,3,5]]
fit = fitnesses(pop)
print(roulette(pop, fit, 4))