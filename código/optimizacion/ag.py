#!/usr/bin/env python3

import random


class Individual():
    genes = (0, 1)
    max_weight = 102

    def __init__(self, elements, chromosome=None):
        # structures after elements to simplify later calculus
        self.values, self.weights = zip(*elements)
        self.size = len(elements)

        # if the chromosome is not specified build a random one
        if chromosome is None:
            chromosome = [random.choice(self.genes) for _ in range(self.size)]
        self.chromosome = chromosome

        # these two values will be set on evaluation
        self.fitness = None
        self.weight = None

    def evaluate(self):
        """Calculate own weight and fitness value.

        This is not done on __init__ because the chromosome may change after creation, it
        will be called automatically before comparison.
        """
        self.fitness = sum(gene * value for gene, value in zip(self.chromosome, self.values))
        self.weight = sum(gene * weight for gene, weight in zip(self.chromosome, self.weights))
        if self.weight > self.max_weight:
            # not fit at all
            self.fitness = -1

    def mutate(self):
        """Change a random gene (maybe)."""
        self.fitness = self.weight = None
        self.chromosome[random.randrange(self.size)] = random.choice(self.genes)

    def __lt__(self, other):
        # ensure fitness is useful
        if self.fitness is None:
            self.evaluate()
        if other.fitness is None:
            other.evaluate()

        return other.fitness < self.fitness

    def __str__(self):
        return f"<Individual {id(self)} fitness={self.fitness}>"
    __repr__ = __str__


class Population():

    def __init__(
        self,
        size=20,                # Cantidad de individuos
        max_gen=50,             # Máximo número de generaciones
        crossover_p=0.9,        # Probabilidad de crossover
        mutation_p=0.05,        # Probabilidad de mutación
        optimo=None,            # Valor óptimo de finalización
        replacement_ratio=0.5,  # Tasa de reemplazo (elitismo)
        elements=None,          # Pares (valor, peso) de los ítems
    ):
        if size % 2:
            raise ValueError("Population size must be even.")
        self.size = size

        # set of individuals, always kept sorted (best at beginning)
        self.individuals = sorted(Individual(elements) for _ in range(size))

        self.elements = elements
        self.crossover_p = crossover_p
        self.mutation_p = mutation_p
        self.max_gen = max_gen
        self.optimo = optimo
        self.replacement_ratio = replacement_ratio
        self.generation = 0

    def best(self):
        """Return the best individual in the population."""
        return self.individuals[0]

    def run(self):
        while not self.final():
            self.step()

    def final(self):
        return self.generation > self.max_gen or self.best().fitness == self.optimo

    def step(self):
        parents = self.selection()
        children = self.do_crossover(parents)
        self.do_mutation(children)
        self.do_new_population(children)
        self.generation += 1

    def selection(self):
        return [self.tournament() for _ in range(self.size)]

    def tournament(self, size=3, goliat=0.9):
        """Tournament selection."""
        competidores = random.choices(self.individuals, k=size)
        competidores.sort()
        if random.random() < goliat:
            return competidores[0]
        else:
            return random.choice(competidores[1:])

    def do_crossover(self, parents):
        """Create a population of children from parents, maybe altering their chromosomes."""
        children = []
        crom_size = parents[0].size

        for _ in range(self.size // 2):
            parent1, parent2 = random.choices(parents, k=2)
            if random.random() < self.crossover_p:
                new_chromo1 = parent1.chromosome.copy()
                new_chromo2 = parent2.chromosome.copy()

                # cross the "randomly central" part of one chromosome with the other
                x_i = random.randrange(0, crom_size - 1)
                x_d = random.randrange(x_i + 1, crom_size)
                new_chromo1[x_i:x_d] = parent2.chromosome[x_i:x_d]
                new_chromo2[x_i:x_d] = parent1.chromosome[x_i:x_d]

                child1 = Individual(self.elements, chromosome=new_chromo1)
                child2 = Individual(self.elements, chromosome=new_chromo2)
            else:
                child1 = parent1
                child2 = parent2
            children.extend((child1, child2))
        return children

    def do_mutation(self, children):
        """Mutate some of the children."""
        for child in children:
            if random.random() < self.mutation_p:
                child.mutate()

    def do_new_population(self, children):
        """Select a portion of the children into current population."""
        children.sort()
        cut_position = int(self.replacement_ratio * self.size)
        self.individuals[self.size - cut_position:] = children[:cut_position]
        self.individuals.sort()


if __name__ == "__main__":
    # Martello-Toth Example 2.1 pg 31: Optimo en {1, 1, 1, 1, 0, 1, 0, 0) valor=280 cap. 102
    # conjunto de pares (valor, peso) para cada elemento a poner en la mochila
    elements = [
        (15, 2),
        (100, 20),
        (90, 20),
        (60, 30),
        (40, 40),
        (15, 30),
        (10, 60),
        (1, 10),
    ]
    population = Population(elements=elements, size=20, max_gen=50)
    population.run()
    print("Mejor individuo:")
    print(population.best().chromosome)
    print("Valor:", population.best().fitness)
    print("Peso:", population.best().weight)

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
