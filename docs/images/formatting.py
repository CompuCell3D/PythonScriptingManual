class TypeSwitcherAndVolumeParamSteppable(SteppableBasePy):
    def __init__(self, _simulator, _frequency=100):
        SteppableBasePy.__init__(self, _simulator, _frequency)

    def start(self):
        for cell in self.cellList:
            if cell.type == 1:
                cell.targetVolume = 25
                cell.lambdaVolume = 2.0
            elif cell.type == 2:
                cell.targetVolume = 50
                cell.lambdaVolume = 2.0

    def step(self, mcs):
        for cell in self.cellList:
            if cell.type == 1:
                cell.type = 2
            elif cell.type == 2:
                cell.type = 1
