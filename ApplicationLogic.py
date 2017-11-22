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
        self.iterations = 1
        self.thread = AutoGeneration(self)

    def start_buttonClicked(self):
        self.main_window.stop_button.setDisabled(False)
        self.main_window.reset_button.setDisabled(True)
        self.main_window.apply_button.setDisabled(True)
        self.main_window.start_button.setDisabled(True)
        if not self.thread.isRunning:
            self.thread.start()
        self.thread.activate()

    def clear(self):
        self.main_window.history_plot.clearData()
        self.iterator = 0
        self.main_window.iteration_number_label.setText("Iteracja numer: " + str(self.iterator))
        print("Wyczyść mię")
    def apply_buttonClicked(self):
        size = int(self.main_window.size_box.text())
        if size <= 0:
            self.main_window.size_box.setValue(20)
            size = 20
        mutation_probability = float(self.main_window.mutation_box.text().replace(',', '.'))
        self.iterations = int(self.main_window.iterations_box.text())
        self.pop = Population(size=size, mutation_probability=mutation_probability)
        self.clear()
        self.thread.__del__()
        self.thread = AutoGeneration(self)

    def iterations_boxValueChanged(self):
        self.iterations = int(self.main_window.iterations_box.text())

    def stop_buttonClicked(self):
        self.thread.stop()
        self.main_window.stop_button.setDisabled(True)
        self.main_window.reset_button.setDisabled(False)
        self.main_window.apply_button.setDisabled(False)
        self.main_window.start_button.setDisabled(False)
    def reset_buttonClicked(self):
        self.main_window.size_box.setValue(20)
        self.main_window.mutation_box.setValue(0.02)
        self.main_window.iterations_box.setValue(1)
        self.pop = Population(size = 20, mutation_probability=0.02)
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
        self.counter = 0

    def run(self):
        while(True):
            if self.isRunning:
                self.logic.pop.next_generation()
                self.logic.iterator += 1
                self.logic.main_window.iteration_number_label.setText("Iteracja numer: " + str(self.logic.iterator))
                self.main_window.history_plot.draw_history(self.pop.current_min_distance, self.pop.current_max_distance, self.pop.current_average_distance)
                self.main_window.min_tour_plot.draw_map(self.pop.current_min_distance_value)
                self.main_window.max_tour_plot.draw_map(self.pop.current_max_distance_value)
                self.counter += 1
                if self.counter == self.logic.iterations:
                    self.counter = 0
                    self.isRunning = False
                    self.logic.stop_buttonClicked()

    def __del__(self):
        self.terminate()

    def stop(self):
        self.isRunning = False

    def activate(self):
        self.isRunning = True