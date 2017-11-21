# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 19:01:33 2017

@author: Charles
"""
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QVBoxLayout, QFrame, \
    QDesktopWidget, QHBoxLayout, QMainWindow, QLayout, QGridLayout
from matplotlib import figure as Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ApplicationLogic import *
from Plots import *

class UIMainWindow(QWidget):

    def __init__(self, width, lenght, parent = None):
        super(UIMainWindow, self).__init__(parent)
        self.width = width
        self.lenght = lenght
        self.screen = QDesktopWidget().screenGeometry()
        self.minimum_width = 800
        self.minimum_height = 1000
        self.dpi_size = 500
        self.logic = ApplicationLogic(self)
        self.init_ui()



    def init_ui(self):
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint
        )
        self.setMinimumWidth(self.minimum_width)
        self.setMaximumWidth(self.screen.width())
        self.setMinimumHeight(self.minimum_height)
        self.setMaximumHeight(self.screen.height())
        self.showMaximized()
        self.setWindowTitle("Komiwjażer")


        self.size_box = QSpinBox(self)
        self.size_box.setMinimum(0)
        self.size_box.setMaximum(10000)
        self.size_box.setSingleStep(2)
        self.size_box.setValue(20)

        self.iterations_box = QSpinBox(self)
        self.iterations_box.setMinimum(0)
        self.iterations_box.setSingleStep(1)
        self.iterations_box.setValue(1)
        self.iterations_box.valueChanged.connect(self.logic.iterations_boxValueChanged)

        self.mutation_box = QDoubleSpinBox(self)
        self.mutation_box.setRange(0,1)
        self.mutation_box.setSingleStep(0.0001)
        self.mutation_box.setValue(0.02)
        self.mutation_box.setDecimals(4)

        self.start_button = QPushButton(self)
        self.start_button.clicked.connect(self.logic.start_buttonClicked)
        self.start_button.setText("Start")

        self.stop_button = QPushButton(self)
        self.stop_button.clicked.connect(self.logic.stop_buttonClicked)
        self.stop_button.setText("Stop")

        self.apply_button = QPushButton(self)
        self.apply_button.clicked.connect(self.logic.apply_buttonClicked)
        self.apply_button.setText("Zastosuj")

        self.reset_button = QPushButton(self)
        self.reset_button.clicked.connect(self.logic.reset_buttonClicked)
        self.reset_button.setText("Reset")

        self.size_label = QLabel(self)
        self.size_label.setText("Populacja: ")

        self.iterations_label = QLabel(self)
        self.iterations_label.setText("Iteracje: ")

        self.mutation_label = QLabel(self)
        self.mutation_label.setText("Mutacje: ")

        self.iteration_number_label = QLabel(self)
        self.iteration_number_label.setText("Iteracja numer: ")
        self.iteration_number_label.setMaximumHeight(20)

        self.min_map_label = QLabel(self)
        self.min_map_label.setText("Trasa o najmniejszej długości:")
        self.min_map_label.setMaximumHeight(20)

        self.max_map_label = QLabel(self)
        self.max_map_label.setText("Trasa o największej długości:")
        self.max_map_label.setMaximumHeight(20)

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setMaximumSize(self.dpi_size, self.dpi_size)
        self.history_plot = PlotCanvas(self.frame, width=self.dpi_size / 100,height=self.dpi_size / 100)

        self.frame2 = QFrame(self)
        self.frame2.setFrameShape(QFrame.Box)
        self.frame2.setFrameShadow(QFrame.Raised)
        self.frame2.setObjectName("frame")
        self.frame2.setMaximumSize(self.dpi_size, self.dpi_size)
        self.min_tour_plot = PlotCanvas(self.frame2, width=self.dpi_size / 100, height=self.dpi_size / 100)

        self.frame3 = QFrame(self)
        self.frame3.setFrameShape(QFrame.Box)
        self.frame3.setFrameShadow(QFrame.Raised)
        self.frame3.setObjectName("frame")
        self.frame3.setMaximumSize(self.dpi_size, self.dpi_size)
        self.max_tour_plot = PlotCanvas(self.frame3, width=self.dpi_size / 100, height=self.dpi_size / 100)




        self.button = QPushButton(self)
        self.button.setText("Tu jestemXXX")

        self.mainLayout = QHBoxLayout(self)
        self.leftLayout = QVBoxLayout(self)
        self.upperLeftLayout = QGridLayout(self)
        self.lowerLeftLayout = QVBoxLayout(self)
        self.leftLayout.addLayout(self.upperLeftLayout)
        self.leftLayout.addLayout(self.lowerLeftLayout)
        self.middleLayout = QVBoxLayout(self)
        self.rightLayout = QVBoxLayout(self)
        self.upperRightLayout = QVBoxLayout(self)
        self.lowerRightLayout = QVBoxLayout(self)
        self.rightLayout.addLayout(self.upperRightLayout)
        self.rightLayout.addLayout(self.lowerRightLayout)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.rightLayout)




       # self.upperLeftLayout.setColumnStretch(2,5)
        self.upperLeftLayout.addWidget(self.size_label, 0, 0)
        self.upperLeftLayout.addWidget(self.mutation_label, 1, 0)
        self.upperLeftLayout.addWidget(self.apply_button, 2, 0)
        self.upperLeftLayout.addWidget(self.iterations_label, 3, 0)
        self.upperLeftLayout.addWidget(self.start_button, 4, 0)

        self.upperLeftLayout.addWidget(self.size_box, 0, 1)
        self.upperLeftLayout.addWidget(self.mutation_box, 1, 1)
        self.upperLeftLayout.addWidget(self.reset_button, 2, 1)
        self.upperLeftLayout.addWidget(self.iterations_box, 3, 1)
        self.upperLeftLayout.addWidget(self.stop_button, 4, 1)

        self.lowerLeftLayout.addWidget(QLabel(""))

        self.middleLayout.addWidget(self.min_map_label)
        self.middleLayout.addWidget(self.min_tour_plot)
        self.middleLayout.addWidget(self.max_map_label)
        self.middleLayout.addWidget(self.max_tour_plot)

        self.upperRightLayout.addWidget(self.iteration_number_label)
        self.upperRightLayout.addWidget(self.frame)

        self.lowerRightLayout.addWidget(QLabel(""))



        self.setLayout(self.mainLayout)


