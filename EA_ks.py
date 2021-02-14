
from EA_general_functions import *
import random
from copy import deepcopy

###########################################
######### POPULATION INITIALIZATION ####### 
###########################################

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
    f.close()

    return [maxWeight,items]


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
        chrom = []
        totalWeight = 0
        totalProfit = 0
        i = 0
        while (len(items) > 0):
            randIndex = random.randint(0,len(items)-1)
            item = items.pop(randIndex) # remove item from items
            if (totalWeight+item[1]) <= maxWeight: # add to chromosone if it doesn't exceed weight
                totalWeight += item[1]
                totalProfit += item[0]
                chrom.append(item)
            i += 1
        
        chrom = [totalProfit, chrom]
        pop.append(chrom)
    
    
    return pop





###################################################
######### FITNESS FUNCTION SCHEMA #################
###################################################

def fitnesses_ks(pop):
    return [x[0] for x in pop]

########################################
######### REPRODUCTION METHODS ######### 
########################################


def uniform_crossover_ks(parent: list, maxWeight):
    """Crossover method to create child chromosome.

    Args:
        parent (list): A list of size 2 containing the parent chromosomes.
        maxWeight: Maximum weight of Knap sack to optimise fitting item

    Returns:
        [list]: A new child chromosome.
    """
    parent1 = deepcopy(parent[0][1])
    parent2 = deepcopy(parent[1][1])
    totalWeight = 0
    totalProfit = 0
    child = []
    i = 0
    while (len(parent1) > 0 and len(parent2) > 0 and totalWeight != maxWeight):
        if (random.randint(0,1) == 0):
            item = parent1.pop(random.randint(0,len(parent1)-1))
            if ((item[1]+totalWeight) <= maxWeight) and item not in child:
                totalWeight += item[1]
                totalProfit += item[0]                
                child.append(item)


        else:
            item = parent2.pop(random.randint(0,len(parent2)-1))
            if ((item[1]+totalWeight) <= maxWeight) and  item not in child:
                totalWeight += item[1]
                totalProfit += item[0]
                child.append(item)
    
    if (len(parent1) == 0 and totalWeight != maxWeight):
        while (len(parent2) > 0 and totalWeight != maxWeight):
            item = parent2.pop(random.randint(0,len(parent2)-1))
            if ((item[1]+totalWeight) <= maxWeight) and  item not in child:
                totalWeight += item[1]
                totalProfit += item[0]    
                child.append(item)



    elif (len(parent2) == 0 and totalWeight != maxWeight):
        while (len(parent1) > 0 and totalWeight != maxWeight):
            item = parent1.pop(random.randint(0,len(parent1)-1))
            if ((item[1]+totalWeight) <= maxWeight) and item not in child:
                totalWeight += item[1]
                totalProfit += item[0]
                child.append(item)

    return [totalProfit,child] # Return the child

###############################
###### MUTATION METHOD ########
###############################

def mutation(chrom,allItems,maxWeight,numOfMutations):
    """ Method to create mutate chromosome. Removes an item randomly and inserts another item
        that was not part of the chromosome earlier
    Args:
        chrom: A nested list containing the totalProfit and a list of items in knapsack
        allItems (list): All available items of Knap sack with their profit 
                         and weight in the form of nested list
    Returns:
        [list]: A new child chromosome.
    """

    for i in range(numOfMutations):
        X = random.randint(0,len(chrom)-1) # Randomly select index of an item in chromosome
        chrom[0] -= chrom[1][X][0] # Subtract profit from the total Profit in chromosome
        chrom[1].pop(X) # Remove the item


    totalWeight = sum(x[1] for x in chrom[1])
    # Difference between allItems and chrom[1]
    nonIncludedItems = []
    
    for i in allItems:
        if i not in chrom[1]:
            nonIncludedItems.append(i)

    while(len(nonIncludedItems) > 0):
        # Select and Remove an item from nonIncludedItems randomly
        item = nonIncludedItems.pop(random.randint(0,len(nonIncludedItems)-1))
        # add it to the chromosone if it doesn't exceed maximum weight
        if (totalWeight+item[1]) <= maxWeight: 
            totalWeight += item[1]
            chrom[0] += item[0] # Add profit into the total Profit in chromosome
            chrom[1].append(item)

    return chrom

#############################################
######### SURVIVOR SELECTION SCHEMA ######### 
#############################################

def survival_selection_ksp(sortedPopulation,killCount,sparedChromos):
    """ Method to delete excess chromosome. It removes them based on 
        fitness propotional selection on a truncated set of least fit 
        chromosomes

    Args:
        sortedPoppulation: A poppulation sorted descendingly based on fitness
        killCount: Number of excess chromosones in poppulation to remove
        sparedChromos: Num of top chromosomes which will not be selected for removal

    Returns:
        [list]: A poppulation with all the excess chromosomes removed
    """
    
    if killCount >= ( len(sortedPopulation) - sparedChromos):
        raise Exception("kill count too large, reduce it!")
    
    
    truncatedPopulation = sortedPopulation[sparedChromos+1:]
    Len = len(truncatedPopulation) - killCount

    fitnesses = fitnesses_ks(truncatedPopulation)
    survivors = select_fps(truncatedPopulation , fitnesses, Len)
    
    sortedPopulation = sortedPopulation[:sparedChromos+1] + survivors

    return sortedPopulation

#################################################################
#################################################################

def EA_ks(filename,generations,sparedChromos=25, popSize=50, num_offspring=50,p_m = 0.5,numOfMutations=1):

    # Initialization
    maxWeight, items = load_items_ks(filename)
    pop = init_knpsk_pop(items, maxWeight, popSize)
    BF_values = []
    AF_values = []
    for g in range(generations):

        children = []
        # Fitness Evaluation (In this case this has been stored in the poppulation already)
        fitnesses = fitnesses_ks(pop)
        # Parent Selection
        parents = select_fps(pop,fitnesses,2*num_offspring)
        # Make parents pairs for reproduction
        parentPairs = [parents[x:x+2] for x in range(0, len(parents), 2)]

        

        for parents in parentPairs:
            # Generate Offspring from Crossover
            children.append( uniform_crossover_ks(parents,maxWeight) )

        
        # Mutation
        for i in range(len(children)):
            if (random.random() < p_m):
                children[i] = mutation(children[i],items,maxWeight,numOfMutations)

        # Add Offspring to poppulation

        pop.extend(children)

        # Sort poppulation based on fitness
        pop.sort(key=lambda x: x[0],reverse=True)

        # Kill Excess Chromosones based on survival selection
        pop = survival_selection_ksp(pop,num_offspring,sparedChromos)
        # Sort poppulation based on fitness

        pop.sort(key=lambda x: x[0],reverse=True)
        SumFitnesess = sum(x[0] for x in pop)
        BF_values.append(pop[0][0])
        AF_values.append(SumFitnesess/len(pop))
        #print("Generation",g,":","BF =",pop[0][0],"LF = ",pop[-1][0],"AF =", SumFitnesess/len(pop))
        
    #print("Optimal Chromosome: ", pop[0])

    return (BF_values,AF_values)

