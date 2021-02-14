
from EA_ks import *

if (random.random() > 0.5):
    print("What up")

# data = [[1,2],[3,4],[5,6],[7,8],[9,10]]
# chunks = [data[x:x+2] for x in range(0, len(data), 2)]
# print(chunks)


s1 = "f7_l-d_kp_7_50"
s2 = "f2_l-d_kp_20_878"
maxWeight, items = load_items_ks(s2)
pop = init_knpsk_pop(items, maxWeight, 100)


print("\n"*2)

'''
print("Fitness:")
fitnesses = fitnesses_ks(pop)
print(fitnesses)

print("Parents:")
pars = select_fps(pop,fitnesses,2)
for par in pars:
    print(par)
print("Child:")
child = uniform_crossover_ks(pars,maxWeight)
print(child)

print("Mutated Child:")
mchild = mutation(child,items,maxWeight,1)
print(mchild)
print("hello")
'''


# EA_ks(filename,popSize,generations,reproductionRate,sparedChromos,mutationRate,numOfMutations=1)
EA_ks(s2,10,100,10,5,0.1,1)
