
from EA_ks import *

if (random.random() > 0.5):
    print("What up")


s1 = "f7_l-d_kp_7_50"
s2 = "f2_l-d_kp_20_878"
maxWeight, items = load_items_ks(s2)
pop = init_knpsk_pop(items, maxWeight, 100)


print("\n"*4)
print("Parents:")
pars = select_fps_ks(pop)
for par in pars:
    print(par)
print("Child:")
child = uniform_crossover_ks(pars,maxWeight)
print(child)

print("Mutated Child:")
mchild = mutation(child,items,maxWeight,1)
print(mchild)
print("hello")


EA_ks(s1,200,100,2,2,0.1,1)
