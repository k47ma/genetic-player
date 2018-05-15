import string
import random
import time
import sys

class GeneticGuess(object):
    def __init__(self, answer, population_size=100, mutation_rate=0.01):
        super(GeneticGuess, self).__init__()

        self.answer = answer
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation = 0

        # get all the possible characters
        self.chars = list(string.digits + string.letters + string.punctuation + ' ')
        random.shuffle(self.chars)

        # population words
        self.population = [self.generate_random_word(len(answer)) for i in range(population_size)]
        self.fitness = []
        self.fitness_weights = []

    def generate_random_word(self, length):
        random_word = "".join([random.choice(self.chars) for i in range(length)])
        return random_word

    def get_fitness(self, word):
        '''
        Calculate the fitness score for word
        '''
        score = 0
        for ind in range(len(word)):
            if word[ind] == self.answer[ind]:
                score += 1
        return score / float(len(self.answer))

    def update_fitness(self):
        '''
        Calculate the fitness for each element and update the fitness scores
        '''
        self.fitness = [self.get_fitness(word) for word in self.population]
        total_fitness = sum(self.fitness)
        self.fitness_weights = [fit / total_fitness for fit in self.fitness]
        self.avg_fitness = total_fitness / self.population_size * 100

    def get_best_guess(self):
        best_guess = self.population[0]
        best_fitness = 0
        for word in self.population:
            word_fitness = self.get_fitness(word)
            if word_fitness > best_fitness:
                best_fitness = word_fitness
                best_guess = word
        return best_guess

    def pick_parent(self):
        random_ind = random.random()
        acc_weight = 0
        for ind, weight in enumerate(self.fitness_weights):
            acc_weight += weight
            if acc_weight > random_ind:
                return self.population[ind]

    def crossover(self):
        '''
        Produce the child generation by crossover the current population
        '''
        new_population = []
        for i in range(self.population_size):
            # randomly pick up two parent elements by weight
            parent1 = self.pick_parent()
            parent2 = self.pick_parent()

            # produce child
            child = ""
            for ind in range(len(parent1)):
                if random.random() < self.mutation_rate:
                    # mutate the current character according to mutation rate
                    child += random.choice(self.chars)
                elif random.random() < 0.5:
                    child += parent1[ind]
                else:
                    child += parent2[ind]

            new_population.append(child)
        
        # replace current population with the new population,
        #   and increment generation counter
        self.population = new_population
        self.generation += 1

    def is_done(self):
        for word in self.population:
            if word == self.answer:
                return True
        return False

    def report_info(self):
        best_guess = self.get_best_guess()
        sys.stdout.write("\rBest Guess: {} | Population: {} | Generation: {} | "
                "Average Fitness: {:.2f}% | Mutation Rate: {}\r"
                         .format(best_guess, self.population_size, self.generation, 
                                 self.avg_fitness, self.mutation_rate))
        sys.stdout.flush()

    def start(self):
        start_time = time.time()
        while not self.is_done():
            # calculate the fitness score for each element
            self.update_fitness()

            # crossover and mutate the population list
            self.crossover()

            # report the best guess and other information
            self.report_info()
        
        print "\nFinished in {} sec".format(time.time() - start_time)


def get_input():
    word = raw_input("Please enter a word: ")
    while not word:
        print "Invalid word!"
        word = raw_input("Please enter a word: ")

    population = raw_input("Population (default=100): ")
    if not population:
        population = 100

    try:
        population = int(population)
    except ValueError:
        print "Invalid population!"
        population = 100

    mutation_rate = raw_input("Mutation Rate (default=0.01): ")
    if not mutation_rate:
        mutation_rate = 0.01

    try:
        mutation_rate = float(mutation_rate)
    except ValueError:
        print "Invalid mutation rate!"
        mutation_rate = 0.01

    return word, population, mutation_rate

if __name__ == '__main__':
    word, population, mutation_rate = get_input()

    guess = GeneticGuess(word, population, mutation_rate)
    guess.start()

