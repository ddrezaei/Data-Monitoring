import Tkinter as tk
import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.ticker import MaxNLocator
import math
import xlwt
import re

NP = 100
colors = ['blue', 'purple', 'green', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
pyplot.ion()

class tabFrame(tk.Frame) :
    def __init__(self, parent, **fDict):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.fDict = fDict
        self.widgets()

    def widgets(self) :
        pltLf = tk.LabelFrame(self)
        pltLf.grid(row=0, column=0, sticky='NW', padx=5, pady=5, ipadx=1)

        figL = 16 #9.9
        figW = 7 #5.8
        self.fig = Figure(figsize=(figL,figW))
        self.fig.subplots_adjust(top=0.95, hspace=0.4)

        self.numf = self.fDict['num']
        if self.numf == 2 :
            fig_dim = "21"
        elif self.numf == 3 :
            fig_dim = "31"
        elif self.numf == 4 :
            fig_dim = "22"
        else :
            fig_dim = "33"
            
        self.ax = []
        for i in range(0, self.numf) :
            n = int(fig_dim + str(i+1))
            self.ax.append(self.fig.add_subplot(n))
            self.ax[i].set_title(self.fDict[str(i+1)])
            self.ax[i].grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=pltLf)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='W', padx=5, ipadx=5, pady=5)

        self.book1 = xlwt.Workbook(encoding="utf-8")
        self.sheet11 = self.book1.add_sheet("Sheet 1", cell_overwrite_ok=True)
        self.sheet11.write(0, 0, "Row")
        for i in range(0, self.numf) :
            self.sheet11.write(0, i+1, self.fDict[str(i+1)])

        self.book1.save(self.fDict['outFile'])

        self.xy_data = []
        for i in range(0, self.numf) :
            sub_data = []
            self.xy_data.append(sub_data)

        self.offset = self.fDict['offset']
        self.counter = 0


    def plot(self, data):

        recd = re.split(' |\$|@|#', data)

        val = []
        if self.fDict['mag']==1 :
            mag = 0
            for j in range(0, self.numf-1) :
                v = float(recd[j + self.offset])
                mag += v*v
                val += [v]
            val += [math.sqrt(mag)]
        else :
            for j in range(0, self.numf) :
                val += [float(recd[j + self.offset])]

        i = len(self.xy_data[0])

        for k in range(0, self.numf) :
            self.xy_data[k] += [[self.counter,val[k]]]
            if self.counter > 0 and self.counter < NP :
                self.ax[k].plot ( [self.xy_data[k][i-1][0], self.xy_data[k][i][0]] ,
                                  [self.xy_data[k][i-1][1], self.xy_data[k][i][1]] ,
                                  color = colors[k] )
            else :
                self.ax[k].clear()
                self.ax[k].grid(True)
                x = [item[0] for item in self.xy_data[k]][i-NP+1:i+1]
                y = [item[1] for item in self.xy_data[k]][i-NP+1:i+1]
                self.ax[k].plot ( x , y , color = colors[k] )
            self.ax[k].set_title(self.fDict[str(k+1)] + str(val[k]))
        self.fig.canvas.draw()

        self.sheet11.write(self.counter+1, 0, str(self.counter))
        self.sheet11.write(self.counter+2, 0, str(self.counter+1))
        for k in range(0, self.numf) :
            if self.counter+1 > NP :
                del self.xy_data[k][0]
            self.sheet11.write(self.counter+1, k+1, str(val[k]))
            self.sheet11.write(self.counter+2, k+1, "*")

        self.book1.save(self.fDict['outFile'])

        self.counter += 1


    def clearPlots(self):
        self.counter = 0
        for k in range(0, self.numf) :
            self.xy_data[k] = []
            self.ax[k].clear()
            self.ax[k].grid(True)
            self.ax[k].set_title(self.fDict[str(k+1)])
        
        self.fig.canvas.draw()
        self.canvas.show()
        

