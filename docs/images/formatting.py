class cellsortingSteppable(SteppableBasePy):
    def __init__(self, _simulator, _frequency=1)
        SteppableBasePy.__init__(self, _simulator, _frequency)

    def start(self):
        field = self.getConcentrationField("FGF")
        field[0, 0, 0] = 2000

    def step(self, mcs):
        field = self.getConcentrationField("FGF")

        for cell in self.cellList:
            if field[cell.xCOM, cell.yCOM, cell.zCOM] > 0.1:
                cell.type = self.CONDENSING
