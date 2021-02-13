
from EA_ks import *

maxWeight, items = load_items_ks("f7_l-d_kp_7_50")
pop = init_knpsk_pop(items, maxWeight, 100)
for p in pop:
    print(p)

print("hello")