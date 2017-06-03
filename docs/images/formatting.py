class HistPlotSteppable(SteppableBasePy):
    def __init__(self, _simulator, _frequency=10):
        SteppableBasePy.__init__(self, _simulator, _frequency)

    def start(self):

        # initialize setting for Histogram
        self.pW = self.addNewPlotWindow(_title='HIstogram', _xAxisTitle='Cell #', _yAxisTitle='Volume')

        # _alpha is transparency 0 is transparent, 255 is opaque
        self.pW.addHistogramPlot(_plotName='Hist 1', _color='green', _alpha=100)
        self.pW.addHistogramPlot(_plotName='Hist 2', _color='red')
        self.pW.addHistogramPlot(_plotName='Hist 3', _color='blue')

    def step(self, mcs):
        volList = []
        for cell in self.cellList:
            volList.append(cell.volume)

        gauss = []
        for i in range(100):
            gauss.append(random.gauss(0, 1))

        self.pW.addHistogram(plot_name='Hist 1', value_array=gauss, number_of_bins=10)
        self.pW.addHistogram(plot_name='Hist 2', value_array=volList, number_of_bins=10)
        self.pW.addHistogram(plot_name='Hist 3', value_array=volList, number_of_bins=50)

        fileName = "HistPlots_" + str(mcs) + ".png"
        self.pW.savePlotAsPNG(fileName, 1000, 1000)  # here we specify size of the image

        fileName = "HistPlots_" + str(mcs) + ".txt"
        self.pW.savePlotAsData(fileName)
