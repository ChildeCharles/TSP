# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 23:29:26 2017

@author: Charles
"""
import random, copy



class Population(object):
    def __init__(self, size=10, mutation_probability=0.02, crossover_probability=1):
        self.size = size
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.data = [(4, 4), (1, 10), (8, 8), (3, 10), (5, 9), (7, 8), (6, 5), (2, 7), (9, 6), (10, 3)]
        self.population = [[0 for j in range(len(self.data))] for i in range(self.size)]
        self.mutations = 0
        for i in range(self.size):
            copied_data = copy.copy(self.data)
            for j in range(len(self.data)):
                self.population[i][j] = copied_data.pop(random.randrange(0, len(copied_data)))
        # Statistics
        self.highest_distance = self.simple_count_distance(self.population[0])
        self.highest_distance_value = self.population[0]
        self.globally_min_distance = self.simple_count_distance(self.population[0])
        self.globally_min_distance_value = self.population[0]
        self.current_min_distance = self.simple_count_distance(self.population[0])
        self.current_min_distance_value = self.population[0]
        self.current_max_distance = self.simple_count_distance(self.population[0])
        self.current_max_distance_value = self.population[0]
        self.current_min_distance = self.simple_count_distance(self.population[0])

    def next_generation(self):
        self.mutate()
        self.crossover()
        self.reproduct()
        return None
    def mutate(self):
        for i in range(self.size):
            for j in range(len(self.data)):
                chance = random.random()
                if chance >= 1 - self.mutation_probability:
                    self.mutations += 1
                    randj = random.randint(0, len(self.data) - 1)
                    self.population[i][randj], self.population[i][j] = self.population[i][j], self.population[i][randj]  # SWAP
        return None

    # GOLDBERG modified to Python
    # city_index : int <not city>, tour : array
    def find_city(self, city_value, tour):
        i = -1
        while True:
            i = i + 1
            if i > len(tour) or tour[i] == city_value:
                result = i
                break
        return result
    # city1_index, city2_index : int, tour : array
    def swap_city(self, city1_index, city2_index, tour):
        tmp = tour[city1_index]
        tour[city1_index] = tour[city2_index]
        tour[city2_index] = tmp
        return tour
    def pmx_cross_tour(self, lenght, lo_cross, hi_cross, tour1, tour2):
        i = lo_cross
        tour1_new = copy.copy(tour1)
        tour2_new = copy.copy(tour2)
        hi_test = hi_cross + 1
        if hi_test > lenght:
            hi_test = 1
        while (i != hi_cross and lo_cross != hi_test):
            tour2_new = self.swap_city(i, self.find_city(tour1[i], tour2_new), tour2_new)
            tour1_new = self.swap_city(i, self.find_city(tour2[i], tour1_new), tour1_new)
            i = i + 1
            if i > lenght:
                i = 1
        return tour1_new, tour2_new

    def crossover(self):
        pairs = []
        # Making pairs
        while len(self.population) > 1:
            item1 = self.population.pop(random.randrange(0, len(self.population)))
            item2 = self.population.pop(random.randrange(0, len(self.population)))
            pairs.append((item1, item2))
        for p1, p2 in pairs:
            chance = random.random()
            if chance >= 1 - self.crossover_probability:
                crossover_point1 = crossover_point2 = random.randint(1, len(self.data) - 1)
                while crossover_point1 == crossover_point2:
                    crossover_point2 = random.randint(1, len(self.data) - 1)
                    if crossover_point2 < crossover_point1:
                        tmp = crossover_point1
                        crossover_point1 = crossover_point2
                        crossover_point2 = tmp
                p1, p2 = self.pmx_cross_tour(len(p1), crossover_point1, crossover_point2, p1, p2)
                self.population.append(p1)
                self.population.append(p2)
        return None

    def distance(self, ax, ay, bx, by):
        return ((ax - bx) ** 2 + (ay - by) ** 2)**(1/2)

    def simple_count_distance(self, tour):
        distances = 0
        for j in range(1, len(tour)):
            ax, ay = str(tour[j-1]).replace("(", "").replace(")", "").split(",")
            bx, by = str(tour[j]).replace("(", "").replace(")", "").split(",")
            ax = int(ax);bx = int(bx);ay = int(ay);by = int(by)
            distances += (self.distance(ax, ay, bx, by))
        return distances # how to use distance to count fitness

    def count_fitness_hardcoded(self):
        distances = []; fitness = []
        max_distance = self.simple_count_distance(self.population[0])
        for i in range(self.size):
            distances.append(self.simple_count_distance(self.population[i]))
            if distances[i] > max_distance:
                max_distance = distances[i]
        for i in range(len(distances)):
            fitness.append(max_distance - distances[i] + 1)
            if fitness[i] > self.highest_distance:
                self.highest_distance, self.highest_distance_value = distances[i], self.population[i]
        # MAX MIN AVERAGE for current generation
        self.current_min_distance = self.simple_count_distance(self.population[0])
        self.current_max_distance = self.simple_count_distance(self.population[0])
        self.current_average_distance = self.simple_count_distance(self.population[0])
        all_distances = 0
        for i in range(len(fitness)):
            dist = distances[i]
            all_distances += dist
            if (dist > self.current_max_distance):
                self.current_max_distance = dist
                self.current_max_distance_value = self.population[i]
            elif (dist < self.current_min_distance):
                self.current_min_distance = dist
                self.current_min_distance_value = self.population[i]
            self.current_average_distance = all_distances / self.size
        if(self.current_min_distance < self.globally_min_distance):
            self.globally_min_distance = self.current_min_distance
            self.globally_min_distance_value = self.current_min_distance_value
        return fitness

    def reproduct(self):
        next_population = []
        fitness = self.count_fitness_hardcoded()
        fitness_sum = 0
        for value in fitness:
            fitness_sum += value
        probability = []
        probability.append(0)
        for i in range(self.size):
            probability.append(((fitness[i]) / fitness_sum) + probability[i])
        probability.pop(0)
        for i in range(self.size):
            chance = random.random()
            j = 0
            while (chance > probability[j]):
                j += 1
                if j > self.size:
                    j = 0
                    chance = random.random
            next_population.append(self.population[j])
        self.population = next_population

        return None
    def print_pop(self):
        for i in range(self.size):
            print(self.population[i])
        return None