import sys
import random
import numpy as np
from game import Game

class Algorithm:
    def __init__(self, population_size=1000, mutation_rate=0.01, max_generation=10000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generation = max_generation
        self.population = None
        self.fitness = None
        self.fitness_weights = None
        self.avg_fitness = 0.0
        self.generation = 0

        # create obstacles and open a new game
        self.total_obs = 200
        self.min_distance = 200
        self.obstacle_pos = [random.randint(i * self.min_distance, (i + 1) * self.min_distance) \
                             for i in range(self.total_obs)]
        self.game = Game(self.obstacle_pos, auto_mode=True)

    def _pick_parent(self):
        random_ind = random.random()
        acc_weight = 0.0
        for ind, weight in enumerate(self.fitness_weights):
            acc_weight += weight
            if acc_weight >= random_ind:
                return self.population[ind]

    def init_population(self, random_state=42):
        random.seed(random_state)
        population = []
        for i in range(self.population_size):
            elem = np.array([random.randint(i * self.min_distance, (i + 1) * self.min_distance) \
                             for i in range(self.total_obs)])
            population.append(elem)
        self.population = population

    def get_fitness(self, element):
        return self.game.get_score(element)

    def update_fitness(self):
        new_fitness = np.array([], dtype=float)
        for elem in self.population:
            fitness = self.get_fitness(elem)
            np.append(new_fitness, fitness)

        # update fitness list
        self.fitness = new_fitness
        self.avg_fitness = np.average(self.fitness)

        # calculate the fitness weights
        total_fitness = np.sum(new_fitness)
        self.fitness_weights = new_fitness / total_fitness

    def crossover(self):
        new_population = []
        for i in range(self.population_size):
            parent1 = self._pick_parent()
            parent2 = self._pick_parent()

            # produce child element
            stack = np.vstack((parent1, parent2))
            child = np.mean(stack, axis=0)

            # mutate child list by mutation rate
            for ind in range(self.total_obs):
                if random.random() < self.mutation_rate:
                    # mutate the current value
                    start_value = 0 if not ind else child[ind - 1]
                    end_value = self.total_obs * self.min_distance if ind == self.total_obs - 1 else child[ind + 1]
                    new_value = random.randint(start_value, end_value)
                    child[ind] = new_value

            new_population.append(child)

        self.population = new_population
        self.generation += 1

    def get_best_guess(self):
        return np.max(self.fitness)

    def report_info(self):
        best_guess = self.get_best_guess()
        sys.stdout.write("\rHighest Fitness: {} | Population: {} | Generation: {} | "
                         "Average Fitness: {:.2f}% | Mutation Rate: {}\r"
                         .format(best_guess, self.population_size, self.generation,
                                 self.avg_fitness, self.mutation_rate))
        sys.stdout.flush()

    def start(self):
        self.init_population()

        while self.generation < self.max_generation:
            # calculate the fitness score for each element
            self.update_fitness()

            # crossover and mutate the population list
            self.crossover()

            # report generation information
            self.report_info()
