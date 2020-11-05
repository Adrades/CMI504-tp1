import random
import matplotlib.pyplot as plt
import gaph

from deap import base
from deap import creator
from deap import tools


def uniques(v):
    return len(v) == len(set(v))


def init_graph(chemin):
    f = open(f"{chemin}.tsp", "r")
    line = f.readline()
    options = {}
    liste_chemin = []
    liste_villes = []
    i = 0
    while "EOF" not in line:
        i -= -1
        if line[0] != " ":
            temp = line.split()
            options[temp[0]] = "" if len(temp) < 2 else " ".join(temp[1:])
        else:
            liste_chemin.extend([int(i) for i in line[1:].split() if i != ""])

            # liste_chemin.append([int(i) for i in line[1:].split() if i != ""])
        line = f.readline()
    # print(liste_chemin)

    for i in range(liste_chemin.count(0)):
        liste_villes.append(gaph.Ville(i))
    i, k = 0, 0
    for j in liste_chemin:
        if j != 0:
            liste_villes[k].Distances[i] = j
            liste_villes[i].Distances[k] = j
            i += 1
        else:
            k += 1
            i = 0
    # random.shuffle(liste_villes)
    return liste_villes


liste_ville = init_graph("gr17")


def create_individual(x):
    l = list(range(x))
    random.shuffle(l)
    return l


def evaluate_tcp(value):
    s = 0
    for v in range(len(value) - 1):
        s += liste_ville[value[v]].get_distance(liste_ville[value[v + 1]])
    s += liste_ville[value[0]].get_distance(liste_ville[value[-1]])
    return s


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("list_villes", create_individual, 17)
# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.list_villes)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def eval_one_max(individual):
    return sum(individual),


def eval_tcp_min(individual):
    return evaluate_tcp(individual),


toolbox.register("evaluate", eval_tcp_min)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == '__main__':
    pop = toolbox.population(n=100)

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    # GMAX est le nombre de génération
    # CMAX est le plafond des courbes
    CXPB, MUTPB, GMAX, CMAX = 0.8, 0.2, 300, 5000

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    min_plt = []
    max_plt = []
    avg_plt = []
    std_plt = []

    # Begin the evolution
    while g < GMAX:
        g += 1
        print(f"-- Generation {g} --")
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)

        z_temp = zip(invalid_ind, fitnesses)
        for ind, fit in z_temp:
            ind.fitness.values = fit

        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print(f"  Min {min(fits)}")
        print(f"  Max {max(fits)}")
        print(f"  Avg {mean}")
        print(f"  Std {std}")

        min_plt.append(min(CMAX, min(fits)))
        max_plt.append(min(CMAX, max(fits)))
        avg_plt.append(min(CMAX, mean))
        std_plt.append(min(CMAX, std))

    plt.plot(min_plt)
    plt.plot(max_plt)
    plt.plot(avg_plt)
    plt.plot(std_plt)
    plt.show()

    soluce = min(pop, key=lambda a: a.fitness.values[0])
    print(soluce)
    print(evaluate_tcp(soluce))
