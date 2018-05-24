from lib.algorithm import Algorithm

if __name__ == '__main__':
    algo = Algorithm(population_size=100, mutation_rate=0.1, max_generation=10000)
    algo.start()
