Accessing concentration fields managed by PDE solvers
=====================================================

Many of CC3D simulations have at least one diffusing field which
represents some sort of chemical it can be growth factor, toxin or
nutrient. The concentration fields are created by CC3D PDE solvers. One
of the most common tasks that modelers implement is modifying cellular
behaviours based on the chemical concentration at the center of mass of
a cell (or for that matter any other point belonging to a given cell).

In this example, we will show you how to extract and modify values of the
concentration fields.

You can take a look at ``CompuCellPythonTutorial/diffusion`` example if you
want a quick preview of code that deals with diffusion fields. The task
here is quite simple. We first have to get a handle to the field and
then using Numpy-like syntax either read or modify field values.

The example that we will implement here is the following. We will start
with "regular" cell-sorting cell layout where condensing and non-condensing cells are mixed together. In the corner of the lattice, we
will place the pulse of the chemical and will let the chemical diffuse. We
will monitor the values of the concentration at the center of mass of
each cell and if this value is greater than ``0.1`` we will change cell
type to ``Condensing``. Assuming that the concentration pulse is big enough all
cells will become ``Condensing`` after some time. Let’s take a look at the
code:

.. code-block:: python

    class CellsortingSteppable(SteppableBasePy):
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

In the start function we get a handle to a diffusion field ``FGF``. This
field is defined in the XML using the following code:

.. code-block:: xml

    <Steppable Type="FlexibleDiffusionSolverFE">
       <DiffusionField>
          <DiffusionData>
             <FieldName>FGF</FieldName>
             <DiffusionConstant>0.1</DiffusionConstant>
             <DecayConstant>1e-05</DecayConstant>
          </DiffusionData>
       </DiffusionField>
    </Steppable>


The XML code above defines diffusion and decay constants but says nothing
about initial conditions. We could have defined initial conditions in
the XML but we chose to do this in the start function of the
Python-based steppable.

The content of the start function is almost self-explanatory. In the
first line of the function we get a handle to concentration field.
Notice that we pass "FGF" to self.getConcentrationField function. It is
exactly the same name as we declared in XML. If you use field name that
is undefined in the XML you will get None object in return. In the second
line we initialize field to have concentration 2000 units at location
``x = 0``, ``y = 0``,  ``z = 0`` . If we wanted to extend the area of initial concentration, we could have used the following Numpy slicing operation:

.. code-block:: python

    field[0:5:1, 0:5:1 ,0] = 2000

and this would put 2000 units of concentration in the 5x5 square at the
origin of the lattice. Like ``range()`` in Python, slicing works as follows: the first number specifies the lower bound, second specifies upper bound (the maximum index is upper
bound minus one), and third specifies step. In our example, ``0:5:1`` will
select indices ``0, 1, 2, 3, 4``.

When we type ``0:6:2`` then we will select indices ``0, 2, 4`` – again ``6`` being
upper bound is not selected. For more information about Numpy slicing
please see numpy tutorial online:

http://wiki.scipy.org/Tentative_NumPy_Tutorial

In the start function we first get a handle to the FGF field, and then
we iterate over each cell in the simulation. We check if FGF
concentration at the center of mass of each cell is greater than 0.1:

.. code-block:: python

    if field[cell.xCOM, cell.yCOM, cell.zCOM] > 0.1:
        ...

and if so we change the cell type to ``Condensing``. Notice that to access
center of mass of a cell we need to include the ``CenterOfMass`` plugin in
the XML using the following code:

.. code-block:: xml

    <Plugin Name="CenterOfMass">

All Twedit++ -generated templates put this plugin by default, but if you
type XML manually you need to remember about this module. ``CenterOfMass``
plugin tracks and keeps an up-to-date center of mass of each cell. To access
COM value from Python, we use the following syntax:

.. code-block:: python

    cell.xCOM
    cell.yCOM
    cell.zCOM

When you run the simulation you will notice that gradually all of the
cells will turn into Condensing.

Min/Max field values
---------------------

To access min or max of concentration fields (i.e. defined in the PDE
solver) you simply type

.. code-block:: python

    minVal = field.min()

or

.. code-block:: python

    maxVal=field.max()
