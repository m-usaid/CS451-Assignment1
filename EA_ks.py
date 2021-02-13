#   TO DO:
#   - Implement population initialization 
#   - Fitness functions 

from EA_general_functions import *
from random import *
from copy import deepcopy

###########################################
######### POPULATION INITIALIZATION ######### 
#############################################

def load_items_ks(file_name):
    """ Loads poppulation from folder for knapsack

    Args:
        filename:  Name of the file without extension along (assuming it is in low-dimensional folder)

    Returns:
        tuple: Having the following two items
            max weight: Max Knap Sack Weight
            item list: A list with nested list of two items corresponding to profit, and weight respectively
        format:- ( maxWeight, [(p1,w1),(p2,w2)...]  )
    """    
    f = open("low-dimensional/" + file_name ,"r")
    items = f.readlines()
    items = [[ int(i) for i in x.split()] for x in items]
    maxWeight = items.pop(0)[1]
    print(items)
    f.close()

    return (maxWeight,items)


def init_knpsk_pop(availableItems, maxWeight,popSize):
    """ Selects random Knap Sack solutions
    to create the initial population.

    Args:
        availableItems: All available items of Knap sack with their profit 
                        and weight in the form of nested list
        maxWeight: Maximum weight of Knap sack to optimise fitting item
        popSize: Size of initial poppulation required

    Returns:
        list: a list of tuples containing random Knap Sack Problem solutions in a list and their total Profit.
    """    
    pop = []
    for i in range(popSize):
        items = deepcopy(availableItems)
        print("items: ",availableItems)
        chrom = []
        totalWeight = 0
        totalProfit = 0
        i = 0
        while (len(items) > 0):
            randIndex = randint(0,len(items)-1)
            item = items.pop(randIndex) # remove item from items
            if (totalWeight+item[1]) <= maxWeight: # add to chromosone if it doesn't exceed weight
                totalWeight += item[1]
                totalProfit += item[0]
                chrom.append(item)
            i += 1
        
        chrom = (totalProfit, chrom)
                
            
        pop.append(chrom)
    
    return pop

    
    

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



maxWeight, items = load_items_ks("f7_l-d_kp_7_50")
pop = init_knpsk_pop(items, maxWeight, 4)
for p in pop:
    print(p)

print("hello")


