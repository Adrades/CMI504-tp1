import abc
import copy


class HillClimbing(metaclass=abc.ABCMeta):
    GENERATE = "generate"
    EVALUATE = "evaluate"

    def __init__(self, solution):
        """
        Initialisation du
        :param solution: Object
        """
        self.solution = copy.copy(solution)
        self.meilleur_solution_trouvee = copy.copy(solution)

    @abc.abstractmethod
    def evaluate(self, value, **kwargs):
        """
        Fonction qui permet d'évaluer une proposition de solution pour le hill-climbing
        :param value: Valeur à évaluer
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractmethod
    def generate(self, **kwargs):
        """
        Fonction qui génère une solution aléatoirement
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_meilleure_solution(self, **kwargs):
        pass

    def test(self, **kwargs):
        ev = {} if HillClimbing.EVALUATE not in kwargs else kwargs[HillClimbing.EVALUATE]
        ge = {} if HillClimbing.GENERATE not in kwargs else kwargs[HillClimbing.GENERATE]

        gen = self.generate(**ge)
        if self.evaluate(gen, **ev) > self.evaluate(self.solution, **ev):
            self.solution = gen
            return True
        return False

    def repeater(self, nb_parrallele=100, nb_erreurs=100, **kwargs):
        """
        répète la phase test un certain nombre de fois
        :return:
        """
        ev = {} if HillClimbing.EVALUATE not in kwargs else kwargs[HillClimbing.EVALUATE]
        back = self.solution
        for i in range(nb_parrallele):
            i = 0
            while nb_erreurs > i:
                if self.test():
                    i = 0
                else:
                    i += 1
            if self.evaluate(self.solution, **ev) > self.evaluate(self.meilleur_solution_trouvee, **ev):
                self.meilleur_solution_trouvee = self.solution
            self.solution = back
