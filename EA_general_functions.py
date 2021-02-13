##########################################################
######### PARENT SELECTION SCHEMAS (MINIMIZATION) ########
##########################################################

import random

def select_fps(population, fitnesses):
    s_fit = 0
    cum_fit = []
    for i in range(len(population)):
        cum_fit.append(s_fit + fitnesses[i])
        s_fit += fitnesses[i]
    parents = random.choices(population, cum_weights=cum_fit, k=2)
    return parents




