
from EA_ks import *

#################################################################
#################################################################


def selectParents(parentSchemeType,pop,num_offspring,fitnesses=None):
    if parentSchemeType == "Random":
        return select_random(pop,2*num_offspring)
    elif parentSchemeType == "FPS":
        if fitnesses == None:
            fitnesses = fitnesses_ks(pop)
        return select_fps(pop,fitnesses,2*num_offspring)
    elif parentSchemeType == "Truncation":
        return select_truncation(pop,2*num_offspring)
    elif parentSchemeType == "RBS":
        return select_rbs(pop,2*num_offspring)

def selectSurvivors(survivorSchemeType,pop,killCount,fitnesses=None,sparedChromos=0):
    
    numOfSurvivors = len(pop) - killCount
    if survivorSchemeType == "Random":
        return select_random(pop, numOfSurvivors)
    elif survivorSchemeType == "FPS":
        return select_fps(pop,fitnesses,numOfSurvivors)
    elif survivorSchemeType == "Truncation":
        return select_truncation(pop,numOfSurvivors)
    elif survivorSchemeType == "RBS":
        return select_rbs(pop,numOfSurvivors)
    elif survivorSchemeType == "Truncation+RBS":
        return survival_selection_ksp(sortedPopulation,killCount,sparedChromos)



def EA_ks_general(filename,generations, popSize=50, num_offspring=10,p_m = 0.5,numOfMutations=1, parentSchemeType="FPS", survivorSchemeType="FPS",sparedChromos=0):

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
        parents = selectParents(pop,fitnesses,num_offspring,parentSchemeType)
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
        pop = selectSurvivors(pop,num_offspring,survivorSchemeType,sparedChromos)
        # Sort poppulation based on fitness

        pop.sort(key=lambda x: x[0],reverse=True)
        SumFitnesess = sum(x[0] for x in pop)
        BF_values.append(pop[0][0])
        AF_values.append(SumFitnesess/len(pop))
        #print("Generation",g,":","BF =",pop[0][0],"LF = ",pop[-1][0],"AF =", SumFitnesess/len(pop))
        
    #print("Optimal Chromosome: ", pop[0])

    return (BF_values,AF_values)


def test():
    s1 = "f7_l-d_kp_7_50"
    s2 = "f2_l-d_kp_20_878"
    
    # EA_ks_generalEA_ks_general(filename,generations, popSize=50, num_offspring=10,p_m = 0.5,numOfMutations=1, parentSchemeType="FPS", survivorSchemeType="FPS",sparedChromos=0):
    EA_ks_general(s2,100,50,10,0.5,1,"FPS","FPS",0)

test()