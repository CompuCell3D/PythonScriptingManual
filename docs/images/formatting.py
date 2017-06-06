def configureSimulation(sim):
    import CompuCellSetup
    from XMLUtils import ElementCC3D

    cc3d = ElementCC3D("CompuCell3D")
    potts = cc3d.ElementCC3D("Potts")
    potts.ElementCC3D("Dimensions", {"x": 100, "y": 100, "z": 1})

…
CompuCellSetup.setSimulationXMLDescription(cc3d)

import sys
from os import environ
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])

import CompuCellSetup

sim, simthread = CompuCellSetup.getCoreSimulationObjects()

configureSimulation(sim)

CompuCellSetup.initializeSimulationObjects(sim, simthread)

from PySteppables import SteppableRegistry

steppableRegistry = SteppableRegistry()

CompuCellSetup.mainLoop(sim, simthread, steppableRegistry)
