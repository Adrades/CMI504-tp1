import hillclimbing
from random import randint
import graph


class TcpHc(hillclimbing.HillClimbing):
    def generate(self, **kwargs):
        """
        Génère un chemin aléatoire à partir de self.solution
        :param kwargs:
        :return: un chemin possible
        """
        tup = self.generate_random_tuple(0, len(self.solution)-1)
        lv = self.solution[:]
        lv[tup[0]], lv[tup[1]] = lv[tup[1]], lv[tup[0]]
        return lv

    @staticmethod
    def generate_random_tuple(mini, maxi):
        """"""
        while (temp_tuple := (randint(mini, maxi), randint(mini, maxi))) is not None and temp_tuple[0] == temp_tuple[1]:
            pass
        return temp_tuple

    def evaluate(self, value, **kwargs):

        s = 0
        for v in range(len(value) - 1):
            s += value[v].get_distance(value[v + 1])
        s += value[0].get_distance(value[- 1])
        return -s

    def get_meilleure_solution(self, **kwargs):
        return -self.evaluate(self.meilleur_solution_trouvee), [i.value for i in self.meilleur_solution_trouvee]

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

    # (1,4,13,7,8,6,17,14,15,3,11,10,2,5,9,12,16)
    tcp17 = TcpHc([liste_villes[v-1] for v in range(17)])
    tcp17.repeater()
    print(tcp17.get_meilleure_solution())

