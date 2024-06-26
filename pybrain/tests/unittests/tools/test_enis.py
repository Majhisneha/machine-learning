from pybrain.tools.plotting.multiline import MultilinePlotter

plotter = MultilinePlotter(maxLines=3)
plotter.addData(0, 1, 2)
plotter.addData(1, [3, 4], [5, 6])
plotter.currentID = 0
plotter.setLineStyle(color="red", linestyle="--")
plotter.setLineStyle(id=[0, 1], color="blue", linestyle="-.")
plotter.setLineStyle(id=1, color="green", linestyle=":")
plotter.setLineStyle(id=-1, color="black", linestyle="-")
#Testing file for the functions addData and setLineStyle