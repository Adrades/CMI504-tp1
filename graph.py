MAX = 1000000


class Ville:
    def __init__(self, value):
        self.value = value
        self.Distances = {}
        self.Distances[self.value] = MAX
        self.moyenne = MAX
        self.medianne = MAX

    def get_ville_plus_proche(self, list_ville):
        return min(list_ville, key=lambda a: a.Distances[self.value])

    def get_villes_plus_proche(self, list_ville, n):
        n = min(n, len(list_ville))
        return sorted(list_ville, key=lambda a: a.Distances[self.value])[:n]

    def calc_moyenne(self):
        self.moyenne = (sum(self.Distances.values()) - MAX) / len(self.Distances.values())
        self.medianne = sorted(self.Distances.values())[len(self.Distances) // 4 * 3]

    def get_distance(self, ville):
        return self.Distances[ville.value]

    def __str__(self):
        return str(self.value)


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
        line = f.readline()
    for i in range(liste_chemin.count(0)):
        liste_villes.append(Ville(i))
    i, k = 0, 0
    for j in liste_chemin:
        if j != 0:
            liste_villes[k].Distances[i] = j
            liste_villes[i].Distances[k] = j
            i += 1
        else:
            k += 1
            i = 0
    return liste_villes
