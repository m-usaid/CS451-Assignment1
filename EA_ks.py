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



maxWeight, items = load_items_ks("f7_l-d_kp_7_50")
pop = init_knpsk_pop(items, maxWeight, 4)
for p in pop:
    print(p)

print("hello")

##########################################################
######### PARENT SELECTION SCHEMA (MINIMIZATION) ######### 
##########################################################

def select_fps_ks(population):
    s_fit = 0
    cum_fit = []
    for i in range(len(population)):
        cum_fit.append(s_fit + population[i][0])
        s_fit += population[i][0]
    parents = random.choices(population, cum_weights=cum_fit, k=2)
    return parents


def uniform_crossover_ks(parent: list, maxWeight):
    """Crossover method to create child chromosome.

    Args:
        parent (list): A list of size 2 containing the parent chromosomes.

    Returns:
        [list]: A new child chromosome.
    """
    parent1 = parent[0][1]
    parent2 = parent[1][1]
    totalWeight = 0
    totalProfit = 0
    child = set()
    while (len(parent1) > 0 and len(parent2) > 0 and totalWeight != maxWeight){

        if (random < 0.5){
            if ((parent1[0]+totalWeight) <= maxWeight ){
                totalWeight += parent1[0][1]
                totalProfit += parent1[0][0]
                child.add(parent1.pop(0))
            }
        }
        else{
            if ((parent2[0]+totalWeight) <= maxWeight ){
                totalWeight += parent2[0][1]
                totalProfit += parent2[0][0]
                child.add(parent2.pop(0))
            }
        }
    
    
    }
    
    if (len(parent1) == 0 and totalWeight != maxWeight){
        while (len(parent2) > 0 and totalWeight != maxWeight){
            if ((parent2[1]+totalWeight) <= maxWeight ){
                totalWeight += parent2[0][1]
                totalProfit += parent2[0][0]
                child.add(parent2.pop(0))
            }
        }
    }
    else if (len(parent2) == 0 and totalWeight != maxWeight){
        while (len(parent1) > 0 and totalWeight != maxWeight){
            if ((parent1[1]+totalWeight) <= maxWeight ){
                totalWeight += parent1[0][1]
                totalProfit += parent1[0][0]
                child.add(parent1.pop(0))
            }
        }
    }

    return (totalProfit,list(child)) # Return the child

    