import math, imp
from matplotlib.lines import Line2D
from pylab import (
    clf,
    plot,
    axes,
    show,
    xlabel,
    ylabel,
    savefig,
    ioff,
    draw_if_interactive,
)

branch_coverage_addData = {"branch_1": False, "branch_2": False}
branch_coverage_setLineStyle = {"branch_1": False, "branch_2": False, "branch_3": False, "branch_4": False, "branch_5": False}


class MultilinePlotter:
    """Basic plotting class build on pylab
    Implementing by instancing the class with the number of different plots to show.
    Every plot has an id so adding data is done by addData(id, xValue, yValue) of the given data point

    :todo: Add possibility to stick markers to the plots
    :todo: Some error checking and documentation
    :todo: Derive from this to make classes for trn/tst data plotting with different linestyles
    """

    # some nice color definitions for graphs (from colorbrewer.org)
    graphColor = [
        (0.894117647, 0.101960784, 0.109803922),
        (0.215686275, 0.494117647, 0.721568627),
        (0.301960784, 0.68627451, 0.290196078),
        (0.596078431, 0.305882353, 0.639215686),
        (1, 0.498039216, 0),
        (1, 1, 0.2),
        (0.650980392, 0.337254902, 0.156862745),
        (0.968627451, 0.505882353, 0.749019608),
        (0.6, 0.6, 0.6),
    ]

    def __init__(self, maxLines=1, autoscale=0.0, **kwargs):
        """
        :key maxLines: Number of Plots to draw and so max ID.
        :key autoscale: If set to a factor > 1, axes are automatically expanded whenever out-range data points are added
        :var indexList: The x-component of the data points
        :var DataList: The y-component of the data points"""
        self.indexList = []
        self.dataList = []
        self.Lines = []
        self.autoscale = autoscale
        clf()
        self.Axes = axes(**kwargs)
        self.nbLines = 0
        self.defaultLineStyle = {}
        self._checkMaxId(maxLines - 1)
        self.replot = True  # is the plot still current?
        self.currentID = None
        self.offset = 0  # external references to IDs are modified by this

    def _checkMaxId(self, id):
        """ Appends additional lines as necessary

    :key id: Lines up to this id are added automatically """
        if id >= self.nbLines:
            for i in range(self.nbLines, id + 1):
                # create a new line with corresponding x/y data, and attach it to the plot
                l = Line2D([], [], color=self.graphColor[i % 9], **self.defaultLineStyle)
                self.Lines.append(l)
                self.Axes.add_line(l)
                self.indexList.append([])
                self.dataList.append([])
            self.nbLines = id + 1

    def addData(self, id0, x, y):
        """The given data point or points is appended to the given line.

        :key id0: The plot ID (counted from 0) the data point(s) belong to.
        :key x: The x-component of the data point(s)
        :key y: The y-component of the data point(s)"""
        id = id0 + self.offset
        if not (isinstance(x, list) | isinstance(x, tuple)):
            branch_coverage_addData["branch_1"] = True
            self._checkMaxId(id)
            self.indexList[id].append(x)
            self.dataList[id].append(y)
            self.currentID = id
        else:
            branch_coverage_addData["branch_2"] = True
            for i, xi in enumerate(x):
                self.addData(id0, xi, y[i])
        self.replot = True
    
    def setLineStyle(self, id=None, **kwargs):
        """ hand parameters to the specified line(s), and set them as default for new lines

    :key id: The line or lines (list!) to be modified - defaults to last one added """
        if id is None:
            branch_coverage_setLineStyle["branch_1"] = True
            id = self.currentID

        if isinstance(id, list) | isinstance(id, tuple):
            branch_coverage_setLineStyle["branch_2"] = True
            # apply to specified list of lines
            self._checkMaxId(max(id) + self.offset)
            for i in id:
                self.Lines[i + self.offset].set(**kwargs)
        elif id >= 0:
            branch_coverage_setLineStyle["branch_3"] = True
            # apply to selected line
            self._checkMaxId(id + self.offset)
            self.Lines[id + self.offset].set(**kwargs)
        else:
            branch_coverage_setLineStyle["branch_4"] = True
            # apply to all lines
            for l in self.Lines:
                l.set(**kwargs)

        # set as new default linestyle
        if 'color' in kwargs:
            branch_coverage_setLineStyle["branch_5"] = True
            kwargs.pop('color')#NOTE: I chnged kwargs.popitem('color') changed kwargs.pop('color') since the dict.popitem() takes no arguments and usage is outdated
        self.defaultLineStyle = kwargs


def print_coverage(branch_coverage):
    totalHit = 0
    for branch, hit in branch_coverage.items():
        if hit:
            print(branch + " is hit")
            totalHit = totalHit + 1
        else:
            print(branch + " is not hit")
    print("Total coverage percent: " + (str)(totalHit / len(branch_coverage) * 100) + "%")


plotter = MultilinePlotter(maxLines=3)
print("-------------BRANCH COVERAGE FOR ADD_DATA-----------------")
print("Before any testcases: ")
print_coverage(branch_coverage_addData)


plotter.addData(0, 1, 2)
print("After first testcase:")
print_coverage(branch_coverage_addData)
print("After second testcase:")
plotter.addData(1, [3, 4], [5, 6])


print("Coverage:")
print_coverage(branch_coverage_addData)


print("-------------BRANCH COVERAGE FOR SET_LINE_STYLE-----------------")
print("Before any testcases: ")
print_coverage(branch_coverage_setLineStyle)

# Test default id (currentID)
plotter.currentID = 0
plotter.setLineStyle(color="red", linestyle="--")
print("After first testcase:")
print_coverage(branch_coverage_setLineStyle)

# Test list of ids
plotter.setLineStyle(id=[0, 1], color="blue", linestyle="-.")
print("After second testcase:")
print_coverage(branch_coverage_setLineStyle)

# Test single id
plotter.setLineStyle(id=1, color="green", linestyle=":")
print("After third testcase:")
print_coverage(branch_coverage_setLineStyle)

# Test all lines
plotter.setLineStyle(id=-1, color="black", linestyle="-")
print("After fourth testcase:")
print_coverage(branch_coverage_setLineStyle)
