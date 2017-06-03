import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON\_MODULE\_PATH"])

import CompuCellSetup

sim, simthread = CompuCellSetup.getCoreSimulationObjects()

CompuCellSetup.initializeSimulationObjects(sim, simthread)

# Add Python steppables here

steppableRegistry = CompuCellSetup.getSteppableRegistry()

from cellsortingSteppables import cellsortingSteppable

steppableInstance = cellsortingSteppable(sim, _frequency=1)

steppableRegistry.registerSteppable(steppableInstance)

CompuCellSetup.mainLoop(sim, simthread, steppableRegistry)
