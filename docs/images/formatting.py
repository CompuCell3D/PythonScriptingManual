from cellsortingSteppables import cellsortingSteppable

steppableInstance = cellsortingSteppable(sim, _frequency=1)
steppableRegistry.registerSteppable(steppableInstance)
