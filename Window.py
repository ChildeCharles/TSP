# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 19:01:33 2017

@author: Charles
"""
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QVBoxLayout, QFrame
from matplotlib import figure as Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ApplicationLogic import *
from Plots import *

class UIMainWindow(QWidget):

    def __init__(self, width, lenght, parent = None):
        super(UIMainWindow, self).__init__(parent)
        self.width = width
        self.lenght = lenght
        self.logic = ApplicationLogic(self)
        self.init_ui()



    def init_ui(self):
        self.resize(self.width, self.lenght)
        self.move(0, 0)
        self.setWindowTitle('Genetic algorithm')

        #Upper panel

        self.current_population_label = QLabel(self)
        self.current_population_label.setText("Obecna populacja:")
        self.current_population_label.move(0, 0)
        self.current_population_label.resize(300, 30)

        self.cp_max_label = QLabel(self)
        self.cp_max_label.setText("Maksimum: ")
        self.cp_max_label.move(0, 40)
        self.cp_max_label.resize(500, 30)

        self.cp_min_label = QLabel(self)
        self.cp_min_label.setText("Minimum:")
        self.cp_min_label.move(0, 40*2)
        self.cp_min_label.resize(500, 30)

        self.cp_avg_label = QLabel(self)
        self.cp_avg_label.setText("Średnio:")
        self.cp_avg_label.move(0, 40*3)
        self.cp_avg_label.resize(500, 30)

        self.max_fitness_label = QLabel(self)
        self.max_fitness_label.setText("Maksymalne przystosowanie:")
        self.max_fitness_label.move(0, 150)
        self.max_fitness_label.resize(300, 30)

        self.iteration_number_label = QLabel(self)
        self.iteration_number_label.setText("Iteracja numer: 0")
        self.iteration_number_label.move(1000, 0)
        self.iteration_number_label.resize(300, 30)


        #Lower panel
        self.size_label = QLabel(self)
        self.size_label.setText("Liczebność populacji:")
        self.size_label.move(0, 780)
        self.size_label.resize(250, 30)

        self.size_box = QSpinBox(self)
        self.size_box.setMinimum(0)
        self.size_box.setSingleStep(2)
        self.size_box.setValue(6)
        self.size_box.move(250, 780)
        self.size_box.resize(100, 30)

        self.mutation_label = QLabel(self)
        self.mutation_label.setText("Prawdopodobieństwo mutacji:")
        self.mutation_label.move(0, 780 + 40 * 1)
        self.mutation_label.resize(250, 30)

        self.mutation_box = QDoubleSpinBox(self)
        self.mutation_box.setMinimum(0.0)
        self.mutation_box.setMaximum(1.0)
        self.mutation_box.setSingleStep(0.01)
        self.mutation_box.setValue(0.01)
        self.mutation_box.move(250, 780 + 40 * 1)
        self.mutation_box.resize(100, 30)

        self.crossing_label = QLabel(self)
        self.crossing_label.setText("Prawdopodobieństwo krzyżowania:")
        self.crossing_label.move(0, 780 + 40 * 2)
        self.crossing_label.resize(250, 30)

        self.crossing_box = QDoubleSpinBox(self)
        self.crossing_box.setMinimum(0.0)
        self.crossing_box.setMaximum(1.0)
        self.crossing_box.setSingleStep(0.01)
        self.crossing_box.setValue(1.0)
        self.crossing_box.move(250, 780 + 40 * 2)
        self.crossing_box.resize(100, 30)

        self.one_generation_button = QPushButton('Jedna generacja', self)
        self.one_generation_button.clicked.connect(self.logic.one_generation_buttonClicked)
        self.one_generation_button.move(500, 850)
        self.one_generation_button.resize(200, 50)

        self.auto_generation_button = QPushButton('Automatyczna generacja', self)
        self.auto_generation_button.clicked.connect(self.logic.auto_generation_buttonClicked)
        self.auto_generation_button.move(750, 850)
        self.auto_generation_button.resize(200, 50)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.logic.stop_buttonClicked)
        self.stop_button.setDisabled(True)
        self.stop_button.move(1000 , 850)
        self.stop_button.resize(200, 50)

        self.apply_button = QPushButton('Zastosuj', self)
        self.apply_button.clicked.connect(self.logic.apply_buttonClicked)
        self.apply_button.move(500, 775)
        self.apply_button.resize(200, 50)

        self.reset_button = QPushButton('Zresetuj', self)
        self.reset_button.clicked.connect(self.logic.reset_buttonClicked)
        self.reset_button.move(750, 775)
        self.reset_button.resize(200, 50)

        self.draw_check_box = QCheckBox('rysuj wykresy', self)
        self.draw_check_box.move(1000, 775)
        self.draw_check_box.resize(200, 50)

        self.current_label = QLabel(self)
        self.current_label.setText("Obecna populacja: ")
        self.current_label.move(700, 50)
        self.current_label.resize(150, 25)

        self.frame = QFrame(self)
        self.frame.setGeometry(QRect(500, 100, 500, 500))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        self.current_label = QLabel(self)
        self.current_label.setText("Przystosowania: ")
        self.current_label.move(1300, 50)
        self.current_label.resize(150, 25)


        self.frame_2 = QFrame(self)
        self.frame_2.setGeometry(QRect(1100, 100, 500, 500))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.function_plot = PlotCanvas(self.frame, width=self.frame.width() / 100, height=self.frame.height() / 100)
        self.function_plot.move(0, 0)
        self.history_plot = PlotCanvas(self.frame_2, width=self.frame_2.width() / 100,height=self.frame_2.height() / 100)
        self.history_plot.move(0, 0)

