import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.widgets as PltWidget
import pandas as pd

class IntStringVar:
    def __init__(self, root, IntVar: tk.IntVar):
        self.IntVar = IntVar
        self.StringVar = tk.StringVar(root, value=self.IntVar.get())
        self.IntVar.trace_add("write", self._IntVarUpdate)
        self.StringVar.trace_add("write", self._StringVarUpdate)

    def _IntVarUpdate(self, val1, val2, val3):
        if (self.StringVar.get() != str(self.IntVar.get())):
            self.StringVar.set(str(int(self.IntVar.get())))
    
    def _StringVarUpdate(self, val1, val2, val3):
        if (self.StringVar.get() != str(self.IntVar.get())):
            self.IntVar.set(self.StringVar.get())


class GUI():
    def __init__(self):
        self.root = None
        self.data = None
        self.dataMerged = None
        self.histData = None

    def GUI(self):
        self.root = tk.Tk()
        self.root.title("Swift Tools")
        self.root.geometry("600x600")

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menuFile = tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="File",menu=self.menuFile)
        self.menuFile.add_command(label="Open File(s)", command=self.OpenFiles)
        self.menuFile.add_command(label="Open Folder", command=self.OpenFolder)

        self.frameTools = tk.Frame(self.root)
        self.frameTools.pack(side=tk.LEFT, expand=True, fill="y")
        self.framePlot = tk.Frame(self.root, background="blue")
        self.framePlot.pack(side=tk.LEFT, expand=True, fill="both")

        self.figure = plt.Figure(figsize=(20,20), dpi=100)
        self.ax = self.figure.add_subplot() 
        self.canvas = FigureCanvasTkAgg(self.figure, self.framePlot)
        self.canvtoolbar = NavigationToolbar2Tk(self.canvas,self.framePlot)
        self.canvtoolbar.update()
        self.canvas.mpl_connect('resize_event', self._CanvasResize)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.draw()

        self.framePlotOptions = ttk.LabelFrame(self.frameTools, text="Plot Options")
        self.framePlotOptions.pack(anchor="nw", fill="x")
        tk.Grid.columnconfigure(self.framePlotOptions, 1, weight=1)
        tk.Label(self.framePlotOptions, text="Title").grid(row=0, column=0)
        tk.Label(self.framePlotOptions, text="X Axis Label").grid(row=1, column=0)
        tk.Label(self.framePlotOptions, text="Y Axis Label").grid(row=2, column=0)
        tk.Label(self.framePlotOptions, text="Bins").grid(row=3, column=0)
        tk.Label(self.framePlotOptions, text="Min").grid(row=4, column=0)
        tk.Label(self.framePlotOptions, text="Max").grid(row=5, column=0)
        self.txtTitleVar = tk.StringVar(value="mjd histogram weighted by mjd_n")
        self.txtXLabelVar = tk.StringVar(value="mjd")
        self.txtYLabelVar = tk.StringVar(value="weighted count")
        self.txtTitleVar.trace_add("write", self._EntryUpdate)
        self.txtXLabelVar.trace_add("write", self._EntryUpdate)
        self.txtYLabelVar.trace_add("write", self._EntryUpdate)
        self.binsVar = IntStringVar(self.root, tk.IntVar(self.root, value=20))
        self.minVar = IntStringVar(self.root, tk.IntVar(self.root, value=0))
        self.maxVar = IntStringVar(self.root, tk.IntVar(self.root, value=1000))
        self.txtTitle = tk.Entry(self.framePlotOptions, textvariable=self.txtTitleVar)
        self.txtXLabel = tk.Entry(self.framePlotOptions, textvariable=self.txtXLabelVar)
        self.txtYLabel = tk.Entry(self.framePlotOptions, textvariable=self.txtYLabelVar)
        self.scaleIntBins = ttk.Scale(self.framePlotOptions, from_=1, to=100, variable=self.binsVar.IntVar,  command=self._WidgetUpdate)
        self.scaleIntMin = ttk.Scale(self.framePlotOptions, from_=0, to=5000, variable=self.minVar.IntVar,  command=self._WidgetUpdate)
        self.scaleIntMax = ttk.Scale(self.framePlotOptions, from_=0, to=5000, variable=self.maxVar.IntVar,  command=self._WidgetUpdate)
        self.numIntBins = tk.Spinbox(self.framePlotOptions, width=6, textvariable=self.binsVar.StringVar, from_=1, to=100)
        self.numIntMin = tk.Spinbox(self.framePlotOptions, width=6, textvariable=self.minVar.StringVar, from_=0, to=5000)
        self.numIntMax = tk.Spinbox(self.framePlotOptions, width=6, textvariable=self.maxVar.StringVar, from_=0, to=5000)
        self.txtTitle.grid(row=0, column=1, columnspan=2, sticky="news")
        self.txtXLabel.grid(row=1, column=1, columnspan=2, sticky="news")
        self.txtYLabel.grid(row=2, column=1, columnspan=2, sticky="news")
        self.scaleIntBins.grid(row=3, column=1, sticky="news")
        self.scaleIntMin.grid(row=4, column=1, sticky="news")
        self.scaleIntMax.grid(row=5, column=1, sticky="news")
        self.numIntBins.grid(row=3, column=2)
        self.numIntMin.grid(row=4, column=2)
        self.numIntMax.grid(row=5, column=2)

        self.frameFiles = ttk.LabelFrame(self.frameTools, text="Files")
        self.frameFiles.pack(anchor="nw", fill="x")
        self.listFiles = tk.Listbox(self.frameFiles)
        self.listFiles.pack(fill="x")

        self.frameExport = ttk.LabelFrame(self.frameTools, text="Export")
        self.frameExport.pack(anchor="nw", fill="x")
        self.btnExportCSV = tk.Button(self.frameExport, text="Export Data (CSV)", command=self.ExportCSV)
        self.btnExportCSV.pack(side=tk.LEFT)
        self.btnExportFigure = tk.Button(self.frameExport, text="Save Figure", command=self.SaveFigure)
        self.btnExportFigure.pack(side=tk.LEFT)
        

        self.root.mainloop()

    def OpenFiles(self):
        filepaths = filedialog.askopenfilename(parent=self.root, title="Swift Tools: Open csv files", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")), multiple=True)
        if filepaths is not None and filepaths != "" and len(filepaths) > 0:
            self.ReadData(filepaths)

    def OpenFolder(self):
        path = filedialog.askdirectory(parent=self.root, title="Swift Tools: Open csv files")
        if path is not None and path != "":
            files = [os.path.abspath(os.path.join(path, f)) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if (len(files) > 0):
                self.ReadData(files)

    def ReadData(self, files):
        self.data = {}
        self.listFiles.delete(0,tk.END)
        for file in files:
            self.data[file] = pd.read_csv(file, sep=",", header=0)
            self.listFiles.insert(tk.END, os.path.basename(file))
        self.dataMerged = pd.concat([d for d in self.data.values()])
        self.Update()

    def Update(self):
        if self.dataMerged is None:
            self.ax.clear()
            return
        self.ax.clear()
        self.ax.set_title(self.txtTitleVar.get())
        self.ax.set_ylabel(self.txtYLabelVar.get())
        self.ax.set_xlabel(self.txtXLabelVar.get())
        range = (self.minVar.IntVar.get(), self.maxVar.IntVar.get())
        if range[0] > range[1]:
            range = (self.maxVar.IntVar.get(), self.minVar.IntVar.get())
        self.histData = self.ax.hist(self.dataMerged["mjd"], weights=self.dataMerged["mjd_n"], bins=self.binsVar.IntVar.get(), range=range)
        if self.framePlot.winfo_width() > 100:
            self.figure.tight_layout()
        self.canvas.draw()

    def ExportCSV(self):
        if self.histData is None:
            self.root.bell()
            return
        save_file = filedialog.asksaveasfile(parent=self.root, mode="w", title="Save as csv", filetypes=[("Comma-separated values", "*.csv"), ("All files", "*.*")], defaultextension=".csv")
        if save_file is None:
            return
        save_file.write("mjd_left,mjd_right,'mjd weighted by mjd_n'\n")
        for i in range(len(self.histData[0])):
            save_file.write("%s,%s,%s\n" % (round(self.histData[1][i],3),round(self.histData[1][i+1],3), self.histData[0][i]))
        save_file.close()

    def SaveFigure(self):
        if self.histData is None:
            self.root.bell()
            return
        save_file = filedialog.asksaveasfile(parent=self.root, mode="w", title="Save as PNG", filetypes=[("PNG", "*.png"), ("All files", "*.*")], defaultextension=".png")
        if save_file is None:
            return
        _fname = save_file.name
        save_file.close()
        self.figure.savefig(_fname)


    def _WidgetUpdate(self, val):
        self.Update()

    def _EntryUpdate(self, val1, val2, val3):
        self.Update()

    def _CanvasResize(self, event):
        if self.framePlot.winfo_width() > 100:
            self.figure.tight_layout()
            self.canvas.draw()
