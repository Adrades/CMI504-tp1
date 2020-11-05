import random
import matplotlib.pyplot as plt

from deap import base
from deap import creator
from deap import tools


def f(x, y):
    return (1 - x) * (1 - x) + 100 * (y - x * x) * (y - x * x)


def g(x, y):
    return (x * x + y - 11) * (x * x + y - 11) + (x + y * y - 7) * (x + y * y - 7)


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, -1000, 1000)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def eval_one_max(individual):
    return sum(individual),


def eval_f_min(individual):
    return f(*individual),

def eval_g_min(individual):
    return g(*individual),


toolbox.register("evaluate", eval_f_min)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == '__main__':
    pop = toolbox.population(n=300)

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    min_plt = []
    max_plt = []
    avg_plt = []
    std_plt = []


    # Begin the evolution
    while g < 25:  # max(fits) < 100
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print(f"  Min {min(fits)}")
        print(f"  Max {max(fits)}")
        print(f"  Avg {mean}")
        print(f"  Std {std}")

        min_plt.append(min(500, min(fits)))
        max_plt.append(min(500, max(fits)))
        avg_plt.append(min(500,mean))
        std_plt.append(min(500,std))

    plt.plot(min_plt)
    plt.plot(max_plt)
    plt.plot(avg_plt)
    plt.plot(std_plt)
    plt.show()

    print(min(pop, key=lambda a:a.fitness.values[0]))
