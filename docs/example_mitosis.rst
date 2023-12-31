Examples: Mitosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Related: `Mitosis <mitosis.html>`_

**********************************

The folder containing this simulation is

*Demos/CompuCellPythonTutorial/steppableBasedMitosis*. 


File:

*Demos/CompuCellPythonTutorial/steppableBasedMitosis/Simulation/steppableBasedMitosisSteppables.py*

.. code-block:: python

    from PySteppables import *
    from PySteppablesExamples import MitosisSteppableBase
    import CompuCell

    class VolumeParamSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=1):
            SteppableBasePy.__init__(self, _simulator, _frequency)

        def start(self):
            for cell in self.cellList:
                cell.targetVolume = 25
                cell.lambdaVolume = 2.0

        def step(self, mcs):
            for cell in self.cellList:
                cell.targetVolume += 1

    class MitosisSteppable(MitosisSteppableBase):
        def __init__(self, _simulator, _frequency=1):
            MitosisSteppableBase.__init__(self, _simulator, _frequency)

            # 0 - parent child position will be randomized between mitosis event
            # negative integer - parent appears on the 'left' of the child
            # positive integer - parent appears on the 'right' of the child
            self.setParentChildPositionFlag(-1)

        def step(self, mcs):
            cells_to_divide = []
            for cell in self.cellList:
                if cell.volume > 50:
                    cells_to_divide.append(cell)

            for cell in cells_to_divide:
                # to change mitosis mode leave one of the below lines uncommented
                self.divideCellRandomOrientation(cell)

        def updateAttributes(self):
            self.parentCell.targetVolume /= 2.0  # reducing parent target volume
            self.cloneParent2Child()

            if self.parentCell.type == self.CONDENSING:
                self.childCell.type = self.NONCONDENSING
            else:
                self.childCell.type = self.CONDENSING

Two steppables: ``VolumeParamSteppable`` and ``MitosisSteppable`` are the
the essence of the above simulation. The first steppable initializes the volume
constraint for all the cells present at ``T=0`` MCS (only one cell) and then
every ``10`` MCS (see the frequency with which ``VolumeParamSteppable`` in
initialized to run -
*Demos/CompuCellPythonTutorial/steppableBasedMitosis/Simulation/steppableBasedMitosis.py*)
it increases the target volume of cells, effectively causing cells to grow.

.. code-block:: python

    from steppableBasedMitosisSteppables import VolumeParamSteppable
    volumeParamSteppable=VolumeParamSteppable(sim ,10)
    steppableRegistry.registerSteppable(volumeParamSteppable)

    from steppableBasedMitosisSteppables import MitosisSteppable
    mitosisSteppable=MitosisSteppable(sim, 10)
    steppableRegistry.registerSteppable(mitosisSteppable)


The second steppable checks every ``10`` MCS (we can, of course, run it
every MCS) if a cell has reached its doubling volume of ``50``. If it did, that 
cell is added to the list cells\_to\_divide. After construction of
``cells_to_divide`` is complete, we iterate over this list and divide all
the cells within it.

.. warning::

    It is important to divide cells outside the loop where we
    iterate over the entire cell inventory. If we keep dividing cells in this
    loop we are adding elements to the list over which we iterate and
    this might have unwanted side effects. The solution is to use a list
    of cells to divide as we did in the example.

Notice that we call ``self.divideCellRandomOrientation(cell``) function to
divide cells. Other modes of division are available as well and they are
as follows:

.. code-block:: python

    self.divideCellOrientationVectorBased(cell,1,0,0)
    self.divideCellAlongMajorAxis(cell)
    self.divideCellAlongMinorAxis(cell)