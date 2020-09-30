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
