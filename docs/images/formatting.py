
import random

class DeltaNotchClass(SteppableBasePy):
    def __init__(self, _simulator, _frequency):
        SteppableBasePy.__init__(self, _simulator, _frequency)

    def start(self):

        modelFile = 'Simulation/DN_Collier.sbml'
        self.addSBMLToCellTypes(_modelFile=modelFile, _modelName='DN',
                                _types=[self.TYPEA], _stepSize=0.2)

        # Initial conditions
        state = {}  # dictionary to store state veriables of the SBML model

        for cell in self.cellList:
            state['D'] = random.uniform(0.9, 1.0)
            state['N'] = random.uniform(0.9, 1.0)
            self.setSBMLState(_modelName='DN', _cell=cell, _state=state)

            cellDict = self.getDictionaryAttribute(cell)
            cellDict['D'] = state['D']
            cellDict['N'] = state['N']

    def step(self, mcs):
        for cell in self.cellList:
            D = 0.0
            nn = 0
            for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                if neighbor:
                    nn += 1
                    state = self.getSBMLState(_modelName='DN', _cell=neighbor)

                    D += state['D']
            if nn > 0:
                D = D / nn

            state = {}
            state['Davg'] = D
            self.setSBMLState(_modelName='DN', _cell=cell, _state=state)

            state = self.getSBMLState(_modelName='DN', _cell=cell)
            cellDict = self.getDictionaryAttribute(cell)
            cellDict['D'] = D
            cellDict['N'] = state['N']
        self.timestepSBML()
