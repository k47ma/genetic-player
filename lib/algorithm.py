import sys
import random
import time
import numpy as np
import multiprocessing as mp
from game import Game
from field import Field
from util import *

class Algorithm:
    def __init__(self, population_size=200, mutation_rate=0.1, max_generation=10000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generation = max_generation
        self.population = None
        self.fitness = None
        self.fitness_weights = None
        self.avg_fitness = 0.0
        self.generation = 0
        self.history = []

        # maximum number of processes for multiprocessing
        self.MAX_PROCESS = 4

        # create obstacles and open a new game
        self.total_obs = 200
        self.min_distance = 200
        self.total_jumps = 400
        self.jump_min_distance = 100
        self.obstacle_pos = [random.randint(i * self.min_distance, (i + 1) * self.min_distance)
                             for i in range(self.total_obs)]

        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 400
        self.game = Game(self.obstacle_pos, auto_mode=True,
                         screen_width=self.SCREEN_WIDTH, screen_height=self.SCREEN_HEIGHT)

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
            elem = np.array([random.randint(i * self.jump_min_distance, (i + 1) * self.jump_min_distance) \
                             for i in range(self.total_jumps)])
            population.append(elem)
        self.population = population

    def update_fitness(self):
        population_parts = split_list(self.population, self.MAX_PROCESS)
        result_queue = mp.Queue()

        # create a new process for each part of the population and calculate the fitness
        processes = []
        for process_ind in range(self.MAX_PROCESS):
            process = mp.Process(target=pop_to_fitness, args=(self.obstacle_pos,
                                 population_parts[process_ind], result_queue, process_ind))
            process.daemon = True
            processes.append(process)
            process.start()

        # wait until all the processes are done
        while result_queue.qsize() < self.MAX_PROCESS:
            self.game.handle_events()
            self.game.update_screen()
            time.sleep(0.05)

        # recover the result from queue
        result_list = [result_queue.get() for i in range(self.MAX_PROCESS)]
        result_list = sorted(result_list, key=lambda x: x['process_ind'])
        new_fitness = []
        for part in result_list:
            new_fitness += part['data']

        # update fitness list
        self.fitness = new_fitness
        self.avg_fitness = np.average(self.fitness)

        # calculate the fitness weights,
        #   here we use powers of fitness for the weight so that elements
        #   with higher fitness has a much higher possibility to be chosen
        #   in crossover than weak elements
        pow_fitness = np.power(new_fitness, 4)
        total_fitness = np.sum(pow_fitness)
        self.fitness_weights = pow_fitness / total_fitness

    def crossover(self):
        new_population = []
        for i in range(self.population_size):
            parent1 = self._pick_parent()
            parent2 = self._pick_parent()

            # produce child element
            stack = np.vstack((parent1, parent2))
            child = np.mean(stack, axis=0, dtype=int)

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

    def get_best_ind(self):
        return np.argmax(self.fitness)

    def report_info(self):
        best_ind = self.get_best_ind()
        best_fitness = self.fitness[best_ind]
        best_population = self.population[best_ind]
        process_time = "{:.2f}s".format(time.time() - self.last_time)
        info = [("Highest Fitness", best_fitness), ("Population", self.population_size),
                ("Generation", self.generation), ("Average Fitness", "{:.2f}".format(self.avg_fitness)),
                ("Mutation Rate", self.mutation_rate), ("Process Time", process_time)]
        formatted_info = " | ".join(["{}: {}".format(key, val) for key, val in info])
        sys.stdout.write(formatted_info + "\n")
        sys.stdout.flush()

        # add the result to history
        self.history.append(dict(info))

        # show the best result in display
        self.game.show(best_population, info=info, history=self.history)

    def start(self):
        self.init_population()

        while self.generation < self.max_generation:
            # start new generation
            self.last_time = time.time()
            self.generation += 1

            # calculate the fitness score for each element
            self.update_fitness()

            # report generation information
            self.report_info()

            # crossover and mutate the population list to get the next generation
            self.crossover()


def get_fitness(obs, actions):
    """Create a new game and quickly finish it to get the score"""
    field = Field(640, 400, obstacle_pos=obs, player_actions=actions)
    score = field.quick_play()
    return score


def pop_to_fitness(obs, population, queue, process_ind):
    result = []
    for pop in population:
        fitness = get_fitness(obs, pop)
        result.append(fitness)
    queue.put({"process_ind": process_ind, "data": result})
