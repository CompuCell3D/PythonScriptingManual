Implementing Energy Functions in Python
=======================================

**Important**: This feature was implemented as a demo and should not be
use in the "production" simulations. Energy functions implemented in
Python are much slower than C++ counterparts. If you would like to write
your own energy function we strongly recommend that you do this in C++.
Twedit++ has C++ module assistant that generates template for any type
of CompuCell3D C++ module and makes overall C++ CompuCell3D module
development much easier. Go to CC3D C++ -> Generate New Module …

CompuCell3D allows users to develop energy functions and lattice
monitors in Python. However, we, recommend that if you do need to write
such module, you do it in C++. With parallel version of CC3D it makes
little sense to build Python modules which are called serially. Even if
we could call them in a truly parallel fashion they still would be a big
performance bottleneck. For completeness we provide brief description of
how to do it. Feel free to skip this section though. In practice modules
presented here are almost never used.

First let's take a look how to develop an energy function that
calculates a change in volume energy. We will use example from
``Demos/CompuCellPythonTutorial/PythonPlugin``. In the XML
file we make sure that instead of calling Volume energy plugin we call:

.. code-block:: xml

    <Plugin Name="VolumeTracker"/>

VolumeTracker module tracks changes in cells’ volume but does not
calculate any energy.The implementation of energy function will we done
in Python:

.. code-block:: python

    from PyPlugins import *


    class VolumeEnergyFunctionPlugin(EnergyFunctionPy):
        def __init__(self, _energyWrapper):
            EnergyFunctionPy.__init__(self)
            self.energyWrapper = _energyWrapper
            self.vt = 0.0
            self.lambda_v = 0.0

        def setParams(self, _lambda, _targetVolume):
            self.lambda_v = _lambda;
            self.vt = _targetVolume

        def changeEnergy(self):
            energy = 0
            newCell = self.energyWrapper.getNewCell()
            oldCell = self.energyWrapper.getOldCell()

            if (newCell):
                energy += self.lambda_v * (1 + 2 * (newCell.volume - self.vt))
            if (oldCell):
                energy += self.lambda_v * (1 - 2 * (oldCell.volume - self.vt))
            return energy


The most important here is changeEnergy function. This is where the
calculation takes place. Of course when we create the plugin object in
the main Python script we will need to make a call to setParams function
because, that is how we set parameters for this plugin. The changeEnergy
function calculates the difference in the volume energy for oldCell and
newCell. The volume energy is given by the formula:

.. math::
   :nowrap:

   \begin{eqnarray}
        E_{volume} = \lambda_{volume} \left(V_{cell}-V_{target} \right )^2
   \end{eqnarray}


Consequently the change in the volume energy for newCell (the one whose
volume will increase due to pixel-copy) is:

.. math::
   :nowrap:

   \begin{eqnarray}
        \Delta E_{newCell} = \lambda\left(V_{newCell}+1-V_{target} \right )^2 - \lambda\left(V_{newCell}-V_{target} \right )^2 = \lambda\left(1+2\left(V_{newCell}-V_{target} \right ) \right )
   \end{eqnarray}


for the old cell (the one whose volume will decrease after pixel-copy)
the corresponding formula is:

.. math::
   :nowrap:

   \begin{eqnarray}
        \Delta E_{newCell} = \lambda\left(V_{oldCell}-1-V_{target} \right )^2 - \lambda\left(V_{oldCell}-V_{target} \right )^2 = \lambda\left(1-2\left(V_{oldCell}-V_{target} \right ) \right )
   \end{eqnarray}


And overall change of energy is:

.. math::
   :nowrap:

   \begin{eqnarray}
        \Delta E = \Delta E_{oldCell}+  \Delta E_{newCell}
   \end{eqnarray}

As you can see, this ``changeEnergy`` function just implements the
formulas that we have just described. Notice that sometimes ``oldCell`` or
``newCell`` might be ``Medium`` cells so that is why we are doing checks for
cell being non-null to avoid segmentation faults when we try to access attribute of the null pointer in C++:

.. code-block:: python

    newCell = self.energyWrapper.getNewCell()
    oldCell = self.energyWrapper.getOldCell()

    if(newCell):
        ...

Notice also that references to ``newCell`` and ``oldCell`` are accessible
through ``energyWrapper`` object. This is a C++ object that stores pointers
to ``oldCell`` and ``newCell`` every pixel-copy attempt. It also stores ``Point3D``
object that contains coordinates of the lattice location at which a
given pixel-copy attempt takes place.

Now, if you look into ``cellsort_2D_with_py_plugin.py`` you will see how
we use Python plugins in the simulation:

.. code-block:: python

    import CompuCellSetup

    sim, simthread = CompuCellSetup.getCoreSimulationObjects()

    import CompuCell  # notice importing CompuCell to main script has to be done after call to getCoreSimulationObjects()

    # Create extra player fields here or add attributes or plugins
    energyFunctionRegistry = CompuCellSetup.getEnergyFunctionRegistry(sim)

    from cellsort_2D_plugins_with_py_plugin import VolumeEnergyFunctionPlugin

    volumeEnergy = VolumeEnergyFunctionPlugin(energyFunctionRegistry)
    volumeEnergy.setParams(2.0, 25.0)

    energyFunctionRegistry.registerPyEnergyFunction(volumeEnergy)

    CompuCellSetup.initializeSimulationObjects(sim, simthread)

    # Add Python steppables here
    steppableRegistry = CompuCellSetup.getSteppableRegistry()

    CompuCellSetup.mainLoop(sim, simthread, steppableRegistry)


After a call to ``getCoreSimulationObjects()`` we create special object
called ``energyFunctionRegistry`` that is responsible for calling Python
plugins that calculate energy every spin flip attempt. Then we create
volume energy plugin that we have just developed and initialize its
parameters. Subsequently, we register the plugin with
``EenergyFunctionRegistry``:

.. code-block:: python

    energyFunctionRegistry.registerPyEnergyFunction(volumeEnergy)

Let's run our simulation now. As you may have noticed the use of this
simple plugin slowed down CompuCell3D more than 10 times. So clearly
energy functions is not what you should be implementing in Python too
often.
