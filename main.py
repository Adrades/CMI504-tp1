import graph
from random import randint

BEST = [2187, 2179, 2229, 2178, 2179, 2413, 2387, 2427, 2415, 2225, 2293, 2340, 2187, 2343, 2276, 2340, 2413]


def best_moyenne(func: callable, lv: list, args: list) -> list:
    """
    Fonction d'automatisation de test d'heuristique
    :param func: callable heuristique
    :param lv: liste des Villes
    :param args: liste des arguments pour func en tuples
    :return:
    """
    res = BEST[:]
    for a in args:
        temps = [func(lv, vil, *a) for vil in range(len(lv))]
        for b in range(len(lv)):
            if res[b] > temps[b]:
                res[b] = temps[b]
                print(f"les calculs ont trouvés une meilleure solution avec a={a}, b={b}, s={temps[b]}")

    return res


def heuristique1(liste_villesi, ii):
    a_passeri = liste_villesi[:]
    v = a_passeri.pop(ii)
    ordre = [v]

    s = 0
    for eeee in range(int(options["DIMENSION:"]) - 1):
        pv = v
        v = v.get_ville_plus_proche(a_passeri)
        a_passeri.remove(v)
        s += v.get_distance(pv)
        ordre.append(v)

    s += ordre[0].get_distance(ordre[-1])

    return s


def heuristique2(lv, deb, n_):
    lv = lv[:]
    v = lv.pop(deb)
    ordre = [v]
    s = 0

    for tour in range(int(options["DIMENSION:"]) - 1):
        pv = v
        v = max(v.get_villes_plus_proche(lv, n_), key=lambda a: a.moyenne)
        lv.remove(v)
        s += v.get_distance(pv)
        ordre.append(v)

    s += ordre[0].get_distance(ordre[-1])

    return s


def heuristique3(lv, deb, n_):
    lv = lv[:]
    v = lv.pop(deb)
    ordre = [v]
    s = 0

    for tour in range(int(options["DIMENSION:"]) - 1):
        pv = v
        v = max(v.get_villes_plus_proche(lv, n_), key=lambda a: a.medianne)
        lv.remove(v)
        s += v.get_distance(pv)
        ordre.append(v)

    s += ordre[0].get_distance(ordre[-1])

    return s


def heuristique6(lv, deb, n_):
    lv = lv[:]
    v = lv.pop(deb)
    ordre = [v]
    s = 0

    for tour in range(int(options["DIMENSION:"]) - 1):
        pv = v
        v = max(v.get_villes_plus_proche(lv, n_), key=lambda a: min(a.Distances.values()))
        lv.remove(v)
        s += v.get_distance(pv)
        ordre.append(v)

    s += ordre[0].get_distance(ordre[-1])
    return s, ordre


def tests_heuristiques():
    print(best_moyenne(heuristique2, liste_villes, [(ih,) for ih in range(1, 20)]))

    print(best_moyenne(heuristique3, liste_villes, [(ih,) for ih in range(1, 20)]))

    print(best_moyenne(heuristique6, liste_villes, [(ih,) for ih in range(1, 20)]))

    # for i in range(17):
    #     print(f"{heuristique2(liste_villes, i, 1)}")


def generate_random_tuple(n, mini, maxi):
    lt = list()
    for i in range(n):
        while (temp_tuple := (randint(mini, maxi), randint(mini, maxi))) in lt and temp_tuple[0]!=temp_tuple[1]:
            pass
        lt.append(temp_tuple)
    return lt


def swap(lv, tuple_v):
    lv = lv[:]
    lv[tuple_v[0]], lv[tuple_v[1]] = lv[tuple_v[1]], lv[tuple_v[0]]
    return lv


def eval_solution(chemin):
    s = 0
    for v in range(len(chemin)-1):
        s += chemin[v].get_distance(chemin[v + 1])
    s += chemin[0].get_distance(chemin[- 1])
    return s


def hill_climbing_1(best_chemin, best_distance, n, crit_a):
    it_crita = 0
    for tu_s in range(n):
        tuple_swap = generate_random_tuple(1, 0, len(best_chemin)-1)[0]
        lv = swap(best_chemin, tuple_swap)
        distance = eval_solution(lv)
        if distance < best_distance:
            best_chemin, best_distance = lv, distance
            it_crita = 0
        else:
            it_crita += 1
            if it_crita >= crit_a:
                # print("plus d'amélioration")
                break
    return best_chemin, best_distance


if __name__ == '__main__':
    tsp = input("Nom du fichir tsp: ")
    f = open(f"{tsp}.tsp", "r")
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
        liste_villes.append(graph.Ville(i))
    i = 0
    k = 0
    for j in liste_chemin:
        if j != 0:

            liste_villes[k].Distances[i] = j
            liste_villes[i].Distances[k] = j

            i += 1
        else:
            k += 1
            i = 0

    for j in liste_villes:
        j.calc_moyenne()

    solution = [liste_villes[v-1] for v in (1,4,13,7,8,6,17,14,15,3,11,10,2,5,9,12,16)]
    ds = eval_solution(solution)
    print("soluce: ", ds)
    # min_solution, min_chemin = heuristique6(liste_villes, 0, 8)
    min_solution, min_chemin = heuristique6(liste_villes, 6, 2)
    c, d = min([hill_climbing_1(min_chemin, min_solution, 100000000, 10) for _ in range(100000)], key=lambda a: a[1])
    print([str(i) for i in c], d, sep = '\n')
    print("fin")
