# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 23:29:26 2017

@author: Charles
"""
import random



class Population(object):

    def simple_count_fitness(self, x):
        return self.fun(x)

    def __init__(self, minimum = -1, maximum =  21, size = 6, mutation_probability = 0.01, crossover_probability = 1):
        self.fun = lambda x: ((-x * x) / 4 + 5 * x + 6)
        #Offset must be used while counting fitness and changing values to presentable ones
        if minimum < 0:
            self.xoffset = -minimum
        elif minimum > 0:
            self.xoffset = minimum
        self.minimum = minimum
        self.maximum = maximum+1

        self.yoffset = 0
        for i in range(self.minimum, self.maximum):
            y = self.simple_count_fitness(i)
            if y < self.yoffset:
                self.yoffset = y

        self.bitlen = len("{0:b}".format(self.maximum))
        self.size = size
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.population = []
        for i in range(0, size):
            #Adding at the end of the list
            self.population.append( random.randint(self.minimum, self.maximum-1) )
            
        self.mutations = 0
        #Statistics
        self.highest_fitness_value = self.population[0]
        self.highest_fitness = self.simple_count_fitness(self.population[0])
        self.current_min = self.simple_count_fitness(self.population[0])
        self.current_min_value = self.population[0]
        self.current_max = self.simple_count_fitness(self.population[0])
        self.current_max_value = self.population[0]
        self.current_average = self.simple_count_fitness(self.population[0])
    def next_generation(self):
        self.mutate()
        self.crossover()
        self.reproduct()
        return None
    def mutate(self):
        for i in range(len(self.population)):
            value = self.population[i]
           # print('Stara:'+str(value))
            safe_value = value
            value_string = self.int_to_bit(value)
            new_value_string = ''
            for char in value_string:
                chance = random.random()
                if chance >= 1-self.mutation_probability:
                    self.mutations +=1
                    if char is "0":
                        new_value_string += "1"
                    elif char is "1":
                        new_value_string += "0" 
                else:
                        new_value_string += char
            value = self.bit_to_int(new_value_string)
          #  print('Nowa:'+str(value))
            if value < self.minimum or value > self.maximum:
                value = safe_value
            self.population[i] = value
        return None

    
    def crossover(self):
        pairs = []
        #Making pairs
        while len(self.population) > 1:
            item1 = self.population.pop(random.randrange(0, len(self.population)))
            item2 = self.population.pop(random.randrange(0, len(self.population)))
            pairs.append((item1, item2))
        for value1, value2 in pairs:
            value_string1 = self.int_to_bit(value1)
            value_string2 = self.int_to_bit(value2)
            #print("Para przed krzyżowaniem:")
            #print(value_string1, value_string2,)
            chance = random.random()
            if chance >= 1-self.crossover_probability:
                #crossover_point = random.randint(0,len(value_string1))
                crossover_point = random.randint(1,len(value_string1)-1)
                #print("SKRZYŻOWANO. Crossover point: "+str(crossover_point))
                value_string1_tail = value_string1[crossover_point : ]
                value_string2_tail = value_string2[crossover_point : ]
                value_string1 = value_string1[ : crossover_point]+value_string2_tail
                value_string2 = value_string2[ : crossover_point]+value_string1_tail 
            value1 = self.bit_to_int(value_string1)
            value2 = self.bit_to_int(value_string2)
            #print("Para po krzyżowaniu:")
            #print(value_string1, value_string2)
            value1 = self.clamp(value1)
            value2 = self.clamp(value2)
            self.population.append(value1)
            self.population.append(value2)
        return None

        
    def count_fitness_hardcoded(self):
        fitness = []
        for i in range(self.size):
            fitness.append(self.simple_count_fitness(self.population[i]))
            #MAX FITNESS
            if fitness[i] > self.highest_fitness:
                self.highest_fitness, self.highest_fitness_value   = fitness[i], self.population[i]
        #MAX MIN AVERAGE for current generation
        self.current_min = self.simple_count_fitness(self.population[0])
        self.current_max = self.simple_count_fitness(self.population[0])
        self.current_average = self.simple_count_fitness(self.population[0])
        all_fitnesses = 0
        for i in range(self.size):
            fit = self.simple_count_fitness(self.population[i])
            all_fitnesses += fit
            if(fit >= self.current_max):
                self.current_max = fit
                self.current_max_value = self.population[i]
            elif(fit <= self.current_min):
                self.current_min = fit
                self.current_min_value = self.population[i]
        self.current_average = all_fitnesses/self.size
        return fitness
        
    def reproduct(self):
        next_population = []
        fitness = self.count_fitness_hardcoded()
        fitness_sum = 0
        for value in fitness:
            fitness_sum += value + self.yoffset
        probability = []
        probability.append(0)
        for i in range(self.size):
            probability.append((  ( fitness[i] + self.yoffset )/fitness_sum) + probability[i])
        probability.pop(0)
        for i in range(self.size):
            chance = random.random()
            j = 0
            while(chance > probability[j]):
                j+=1
                if j > self.size:
                    j = 0
                    chance = random.random
            next_population.append(self.population[j])
       #     print("PP: "+str(chance))
       #     print("Wylosowano: "+str(self.population[j]))
      #  print("Stara populacja: \n"+str(self.population))
      #  for i in range(self.size):
      #      print(str(self.population[i])+' - '+str(fitness[i]/fitness_sum))
      #      print(str(probability[i]))
      #  self.population = next_population
      #  print("Nowa populacja: \n"+str(self.population)+'\n')
        return None
    def print_pop(self):
        pop = self.population.copy()
        code_pop = self.population.copy()
        print('Populacja:')
        print(list(pop))
        #print('Populacja w kodzie:')
        #print(list(code_pop))
        print('Mutacje:'+str(self.mutations))
        print("Najlepsza przystosowany: "+str(self.highest_fitness_value)+
              " o przystosowaniu: "+(str(self.highest_fitness) ))
        return True
  #  def int_to_bin(self, number):
  #      return "{0:b}".format(number)
    def int_to_bit(self, number):
        return ('{0:0'+str(self.bitlen)+'b}').format(number - self.xoffset)
    def bit_to_int(self, value):
        return int(value, 2) + self.xoffset
    def clamp(self, value):
        return max(self.minimum, min(value, self.maximum-1))
    