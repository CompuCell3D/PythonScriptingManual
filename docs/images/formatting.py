class SBMLSolverOscilatorDemoSteppable(SteppableBasePy):
    def __init__(self, _simulator, _frequency=10):
        SteppableBasePy.__init__(self, _simulator, _frequency)

    def start(self):
        self.pW = self.addNewPlotWindow(_title='S1 concentration', \
                                        _xAxisTitle='MonteCarlo Step (MCS)', _yAxisTitle='Variables')
        self.pW.addPlot('S1', _style='Dots', _color='red', _size=5)

        # iterating over all cells in simulation
        for cell in self.cellList:
            # you can access/manipulate cell properties here
            cell.targetVolume = 25
            cell.lambdaVolume = 2.0

        ...

    def step(self, mcs):
        ...

        self.pW.showAllPlots()
        self.timestepSBML()
