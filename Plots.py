from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator, MultipleLocator



class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, pie=False):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.ax = self.figure.add_subplot(111)
        self.mins = []
        self.maxes = []
        self.averages = []

    def clearData(self):
        self.ax.cla()
        self.mins = []
        self.maxes = []
        self.averages = []
        self.draw()


    def draw_history(self, current_min, current_max, current_avg):
        self.mins.append(current_min)
        self.maxes.append(current_max)
        self.averages.append(current_avg)
        if len(self.mins) > 25:
            self.mins = self.mins[-25:]
            self.maxes = self.maxes[-25:]
            self.averages = self.averages[-25:]
        self.ax.cla()
        self.ax.plot(self.mins, 'm', linewidth = 0.7)
        self.ax.plot(self.maxes, 'b', linewidth=0.7)
        self.ax.plot(self.averages, 'r', linewidth=2)
        self.ax.set_xbound(0, 25)
        self.ax.grid(b=True, which='both')
        major_locator = MultipleLocator(2)
        minor_locator = AutoMinorLocator(2)
        self.ax.xaxis.set_major_locator(major_locator)
        self.ax.xaxis.set_minor_locator(minor_locator)
        self.draw()

    def draw_function(self, function, minimum, maximum, population):
        y_points = []   #y_points = [function(member) for member in population]
        for member in population:
            y_points.append(function(member))

        y = []  # y = [function(value) for value in range(minimum, maximum)]
        for value in range(minimum, maximum):
            y.append(function(value))
        self.ax.cla()
        self.ax.plot(range(minimum, maximum), y)
        self.ax.plot(population, y_points, 'r*')
        self.ax.grid(b=True, which='both')
        self.draw()