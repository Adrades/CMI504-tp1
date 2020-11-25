import random
import matplotlib.pyplot as plt
import graph
import csv

from deap import base
from deap import creator
from deap import tools

NOM_DEFAUT = "mon_super_csv_avec_les_données_de_l_algorithme_génétique"
NOM_FICHIER_GRAPHE = "gr17"


def create_individual(x: int) -> list:
    """
    Fonction permettant de creer les individus de cet ag.
    Ces invididus sont une list d'entiers de 0 au nombre de villes x.
    Cette fontion créé une liste de ce type et la mélange aléatoirment.
    :param x: Nombre de Villes
    :return: Une liste d'entier
    """
    liste_nombre_0_x = list(range(x))
    random.shuffle(liste_nombre_0_x)
    return liste_nombre_0_x


def evaluate_tcp(lv: list, value: list) -> int:
    """
    Fonction qui évalue les individus.
    :param lv: La liste des Villes
    :param value: L'individu (Liste d'entiers) évalué
    :return:
    """
    return sum([lv[value[v]].get_distance(lv[value[v + 1]]) for v in range(len(value) - 1)]) + lv[
        value[0]].get_distance(lv[value[-1]])


def eval_tcp_min(lv: list, individual: list) -> tuple:
    """
    Fonction utilisé pour retourner un tuple
    :param lv: Liste des villes
    :param individual: Individu
    :return: Un tuple avec un int
    """
    return evaluate_tcp(lv, individual),


def prep_tcp(lv: list, mut_taux: float, taille_tournoi: int) -> base.Toolbox:
    """
    Fonction préparant les méthodes via deap
    :param lv: Liste des Villes
    :param mut_taux: Taux de mutation
    :param taille_tournoi: Taille du tournoi.
    :return: La toolbox contenant les méthodes.
    """
    # Création du nécéssaire à un individu
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register("list_villes", create_individual, len(lv))
    # Structure initializers
    # Création de l'individu
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.list_villes)
    # Création d'un population
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # Évaluation d'un individu
    toolbox.register("evaluate", eval_tcp_min, lv)
    # Reproduction d'un individu
    toolbox.register("mate", tools.cxPartialyMatched)
    # Mutation d'un individu
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mut_taux)
    # Selection des meilleurs individus
    toolbox.register("select", tools.selTournament, tournsize=taille_tournoi)

    return toolbox


def run_ag_tcp(liste_villes: list, taille_pop: int, cx_pb: float, mut_pb: float, mut_taux: float, nb_gen: int,
               **kwargs):
    """
    Algorithmes de résolution de tcp via AG.
    :param liste_villes: Liste des villes
    :param taille_pop: Taille de la population
    :param cx_pb: La probabilité que deux individus soit croisés
    :param mut_pb: La probabilité qu'une mutation arrive sur un individu
    :param mut_taux: Le taux de mutation d'un individu lors d'une mutation
    :param nb_gen: Le nombre de générations
    :keyword courbes_max: Le plafond des courbes
    :key afficher_plot: Affiche les coubre avec math.pyplot
    :key affichage: Boolèen régissant l'affichage des résultats dans la console
    :key enregistrement: Booléen régissant l'enregistrement dans un .csv
    :key name: permet de choisir un nom pour le csv
    :key detailled: permet d'afficher min, max, avg et std à chaque génération
    """

    # initialistaion de la population
    toolbox = prep_tcp(liste_villes, mut_taux, 3)
    pop = toolbox.population(n=taille_pop)

    courbes_max = 2 ** 16 if "courbes_max" not in kwargs.keys() else kwargs["courbes_max"]

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Variable keeping track of the number of generations
    g = 0

    min_lst, max_lst, avg_lst, std_lst = [[] for _ in range(4)]

    # Begin the evolution
    while g < nb_gen:
        g += 1
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_pb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mut_pb:
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

        if "affichage" in kwargs.keys() and "detailled" in kwargs.keys():
            print(f"-- Generation {g} --")
            print(f"  Min {min(fits)}")
            print(f"  Max {max(fits)}")
            print(f"  Avg {mean}")
            print(f"  Std {std}")

        min_lst.append(min(courbes_max, min(fits)))
        max_lst.append(min(courbes_max, max(fits)))
        avg_lst.append(min(courbes_max, mean))
        std_lst.append(min(courbes_max, std))

    if "afficher_plot" in kwargs.keys():
        plt.plot(min_lst)
        plt.plot(max_lst)
        plt.plot(avg_lst)
        plt.plot(std_lst)
        plt.show()

    if "affichage" in kwargs.keys():
        soluce = min(pop, key=lambda a: a.fitness.values[0])
        print("Meilleure solution trouvée:", soluce, evaluate_tcp(liste_villes, soluce), sep="\n")

    if "enregistrement" in kwargs.keys():
        nom_fichier = NOM_DEFAUT if "name" not in kwargs.keys() else kwargs["name"]

        with open(nom_fichier + ".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Numéro de la génération', ''] + list(range(nb_gen)))
            writer.writerow(['Minimun', ''] + min_lst)
            writer.writerow(['Maximum', ''] + max_lst)
            writer.writerow(['Moyenne', ''] + avg_lst)
            writer.writerow(['Écart type', ''] + std_lst)


if __name__ == '__main__':
    liste_ville = graph.init_graph(NOM_FICHIER_GRAPHE)

    # exemple d'enregistrement en csv avec le nom Mon_super_test.csv
    run_ag_tcp(liste_ville, 50, 0.7, 0.2, 0.2, 20, enregistrement=1, name="Mon_super_test")

    # exemple d'affichage détaillé en console
    run_ag_tcp(liste_ville, 100, 0.5, 0.05, 0.4, 50, affichage = 1, detailled=1)

    # Affichage des résultats avec pyplot, et une limite des valeurs de la courbe à 5000
    run_ag_tcp(liste_ville, 100, 0.8, 0, 0, 300, afficher_plot=1, courbes_max=5000)
