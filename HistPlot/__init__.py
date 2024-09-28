import sys, os

if __name__ == "__main__":
    histplot_path = os.path.join(os.path.join(__file__, os.pardir), os.pardir)
    histplot_path = os.path.abspath(histplot_path)
    sys.path.insert(1, histplot_path)

from HistPlot.gui import GUI

if __name__ == "__main__":
    gui = GUI()
    gui.GUI()