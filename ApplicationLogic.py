# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 19:01:33 2017

@author: Charles
"""
from PyQt5.QtCore import QThread
from matplotlib import pyplot

from Population import Population
class ApplicationLogic(object):

    def __init__(self, main_window):
        self.pop = Population()
        self.main_window = main_window
        self.iterator = 0
        self.thread = AutoGeneration(self)
    def one_generation_buttonClicked(self):
        if not self.thread.isRunning:
            self.thread.start()
        self.thread.activate("ONE")

    def auto_generation_buttonClicked(self):
        self.main_window.stop_button.setDisabled(False)
        self.main_window.reset_button.setDisabled(True)
        self.main_window.apply_button.setDisabled(True)
        self.main_window.one_generation_button.setDisabled(True)
        self.main_window.auto_generation_button.setDisabled(True)
        if not self.thread.isRunning:
            self.thread.start()
        self.thread.activate("INFINITY")


    def clear(self):
        self.main_window.function_plot.clearData()
        self.main_window.history_plot.clearData()
        self.iterator = 0
        self.main_window.iteration_number_label.setText("Iteracja numer: " + str(self.iterator))
        self.main_window.cp_max_label.setText("Maksimum: ")
        self.main_window.cp_min_label.setText("Minimum: ")
        self.main_window.cp_avg_label.setText("Średnio: ")
        self.main_window.max_fitness_label.setText("Maksymalne przystosowanie: ")
    def apply_buttonClicked(self):
        size = int(self.main_window.size_box.text())
        if size <= 0:
            self.main_window.size_box.setValue(2)
            size = 2
        mutation_probability = float(self.main_window.mutation_box.text().replace(',', '.'))
        crossing_probability = float(self.main_window.crossing_box.text().replace(',', '.'))
        self.pop = Population(size=size, mutation_probability=mutation_probability, crossover_probability=crossing_probability)
        self.clear()
        self.thread.__del__()
        self.thread = AutoGeneration(self)
    def stop_buttonClicked(self):
        self.thread.stop()
        self.main_window.stop_button.setDisabled(True)
        self.main_window.reset_button.setDisabled(False)
        self.main_window.apply_button.setDisabled(False)
        self.main_window.one_generation_button.setDisabled(False)
        self.main_window.auto_generation_button.setDisabled(False)
    def reset_buttonClicked(self):
        self.main_window.size_box.setValue(6)
        self.main_window.mutation_box.setValue(0.01)
        self.main_window.crossing_box.setValue(1)
        self.pop = Population(size = 6, mutation_probability=0.01, crossover_probability=1)
        self.clear()
        self.thread.__del__()
        self.thread = AutoGeneration(self)



class AutoGeneration(QThread):
    def __init__(self, logic):
        QThread.__init__(self)
        self.logic = logic
        self.main_window = logic.main_window
        self.pop = logic.pop
        self.isRunning = False
        self.mode = "ONE"
        self.counter = 0

    def run(self):
        while(True):
            if self.isRunning:
                max_fitness = self.logic.pop.highest_fitness
                self.logic.pop.next_generation()
                self.logic.iterator += 1
                self.logic.main_window.iteration_number_label.setText("Iteracja numer: " + str(self.logic.iterator))
                self.logic.main_window.cp_max_label.setText("Maksimum: "+str(self.logic.pop.current_max)+ " dla x = " + str(self.logic.pop.current_max_value ))
                self.logic.main_window.cp_min_label.setText("Minimum: " + str(self.logic.pop.current_min) + " dla x = " + str(self.logic.pop.current_min_value ))
                self.logic.main_window.cp_avg_label.setText("Średnio: " + str(round((float(self.logic.pop.current_average)), 2)) )
                self.logic.main_window.max_fitness_label.setText("Maksymalne przystosowanie: " + str(self.logic.pop.highest_fitness) + " dla x = " + str(self.logic.pop.highest_fitness_value ))
                if self.main_window.draw_check_box.checkState():
                    self.main_window.function_plot.draw_function(self.pop.fun, self.pop.minimum, self.pop.maximum, self.pop.population)
                    self.main_window.history_plot.draw_history(self.pop.current_min, self.pop.current_max, self.pop.current_average)

                # STOP CONDITION
                if self.mode == 'ONE':
                    self.isRunning = False

                if self.mode == "INFINITY":
                    if max_fitness == self.logic.pop.highest_fitness:
                        self.counter += 1
                    else:
                        self.counter = 0
                    if self.counter == 50:
                        self.counter = 0
                        self.isRunning = False
                        self.logic.stop_buttonClicked()


    def __del__(self):
        self.terminate()

    def stop(self):
        self.isRunning = False

    def activate(self, mode):
        self.isRunning = True
        self.mode = mode