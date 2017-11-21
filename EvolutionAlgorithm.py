# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 19:01:33 2017

@author: Charles
"""

from Population import Population
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene
from win32api import GetSystemMetrics
from Window import UIMainWindow
import sys
import ctypes

def main():
    app = QApplication(sys.argv)
    window = UIMainWindow(0, 0)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()