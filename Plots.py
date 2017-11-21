from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator, MultipleLocator



class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)



        FigureCanvas.updateGeometry(self)

        self.ax = self.figure.add_subplot(111)
        self.mins = []
        self.maxes = []
        self.averages = []
        self.x_list = []
        self.y_list = []

    def clearData(self):
        self.ax.cla()
        self.mins = []
        self.maxes = []
        self.averages = []
        del self.x_list[:]
        del self.y_list[:]

        self.draw()


    def draw_history(self, distance_min, distance_max, distance_avg):
        self.mins.append(distance_min)
        self.maxes.append(distance_max)
        self.averages.append(distance_avg)
        if len(self.mins) > 25:
            self.mins = self.mins[-25:]
            self.maxes = self.maxes[-25:]
            self.averages = self.averages[-25:]
        self.ax.cla()
        self.ax.plot(self.mins, 'm', linewidth=0.7, label="Minimalna odległość")
        self.ax.plot(self.averages, 'r', linewidth=2, label="Średnia odległość")
        self.ax.plot(self.maxes, 'b', linewidth=0.7, label="Maksymalna odległość")
        self.ax.legend(bbox_to_anchor=(0.6, 0.1), loc=2, borderaxespad=0.01)

        self.ax.set_xbound(0, 25)
        self.ax.grid(b=True, which='both')
        major_locator = MultipleLocator(2)
        minor_locator = AutoMinorLocator(2)
        self.ax.xaxis.set_major_locator(major_locator)
        self.ax.xaxis.set_minor_locator(minor_locator)
        self.draw()

    def draw_map(self, tour):
        self.x_list = []; self.y_list = []; labels = []
        for i in range(0, len(tour)):
            x, y = str(tour[i]).replace("(", "").replace(")", "").split(",")
            self.x_list.append(x); self.y_list.append(y)
        self.ax.cla()
        for i in range(len(self.x_list)):
            labels.append('{name}({x},{y})'.format(name=chr(65+i), x = self.x_list[i], y = self.y_list[i]))
        self.ax.plot(self.x_list, self.y_list, 'bo')
        self.ax.plot(self.x_list, self.y_list, linestyle='-', linewidth = 0.8)
        for label, x, y in zip(labels, self.x_list, self.y_list):
            self.ax.annotate(label, xy=(x, y), xytext=(25,-4), textcoords='offset points', ha='right', va='top')
        self.draw()
