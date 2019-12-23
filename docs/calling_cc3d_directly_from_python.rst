Direct Call to CompuCell3D from Python
=======================================

In a typical situation, you will most often run CC3D using GUI. You create simulation, run it, look at the results,
modify parameters, run again and the process continues. But what if you would like to be more "methodical" in
finding optimal parameters? The new CC3D comes with a convenience module that allows you to directly call CC3D as
a Python function and get return value(s) from your simulations. As you can tell already, functionality like this
allows you to use various optimization packages and be able to find desired set of parameters for your simulation
- assuming you know how to define a proper metrics.

How does it work?
-----------------

If you want to call CC3D engine from a Python function and get return value you need to modify your existing
simulation to return such value. This is a very easy step - take a look at he code below:

.. code-block:: python

    from cc3d.core.PySteppables import *
    from cc3d import CompuCellSetup
    from random import random


    class CellsortSteppable(SteppableBasePy):
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)

        def start(self):
            pass

        def step(self, mcs):
            if mcs == 100:
                pg = CompuCellSetup.persistent_globals
                pg.return_object = 200.0 + random()


This is a "regular" steppable. The only new part is the line where we modify
``CompuCellSetup.persistent_globals.return_object``. This variable that will persist even after simulation is finished
is the way we pass simulation return value to the caller. Here, our return value is set to be a sum of number ``200.0``
and a random number between 0 and 1. This return value can be set at any point in the simulation.
In particular it often makes sense to set it in the ``finish`` function, but for illustration purposes we set it in
``step`` function. When accessing persistent_globals object , do not forget to include necessary import:
``from cc3d import CompuCellSetup``
