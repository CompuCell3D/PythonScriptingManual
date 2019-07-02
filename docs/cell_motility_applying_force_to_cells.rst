Cell Motility. Applying force to cells.
=======================================

In some CC3D simulations we need make cells move in certain direction.
Sometimes we do it using chemotaxis energy term (if indeed in real
system that chemotaxis is the reason for directed motion) and sometimes
we simply apply energy term which simulates a force. In the CC3D manual
we show how to apply constant force to all cells or on a type-by-type
basis. Here let us concentrate on a situation where we apply force to
individual cells and how change its value and the direction. You can
check simulation code in ``Demos/CompuCellPythonTutorial/CellMotility``.
To be able to use force in our simulation ( we need to include
``ExternalPotential`` plugin in the CC3DML:

.. code-block:: xml

    <Plugin Name="ExternalPotential"/>

Let us look at the steppable code:

.. code-block:: python

    from random import uniform

    class CellMotilitySteppable(SteppableBasePy):
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)

        def start(self):

            # iterating over all cells in simulation
            for cell in self.cell_list:
                break
                # Make sure ExternalPotential plugin is loaded
                # negative lambdaVecX makes force point in the positive direction
                # force component along X axis
                cell.lambdaVecX = 10.1 * uniform(-0.5, 0.5)
                # force component along Y axis
                cell.lambdaVecY = 10.1 * uniform(-0.5, 0.5)
                #         cell.lambdaVecZ=0.0 # force component along Z axis

        def step(self, mcs):

            for cell in self.cell_list:
                # force component along X axis
                cell.lambdaVecX = 10.1 * uniform(-0.5, 0.5)
                # force component along Y axis
                cell.lambdaVecY = 10.1 * uniform(-0.5, 0.5)


Once ``ExternalPotential`` plugin has been loaded we assign a constant force
in a given direction by initializing ``lambdaVecX``, ``lambdaVecY``, ``lambdaVecZ``
cell attributes.

.. note::

    When pushing cell along X axis toward higher X values (i.e. to the right) use ``lambdaVecX`` negative. When pushing to the left use positive values.

In the start function we assign random values of ``X`` and ``Y`` components of
the force. The ``uniform(-0.5, 05)`` function from the Python random module
picks a random number from a uniform distribution between ``-0.5`` and ``0.5``.

In the step function we randomize forces applied to the cells in the
same way we did it in start function.

As you can see the whole operation of applying force to any given cell
in the CC3D is very simple.

The presented example is also very simple. But you can imagine more
complex scenarios where the force depends on the velocity, of
neighboring cels. This is however beyond the scope of this introductory