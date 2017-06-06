Adding and managing extra fields for visualization purposes
===========================================================

Quite often in your simulation you will want to label cells using scalar
field, vector fields or simply create your own scalar or vector fields
which are fully managed by you from the Python level. CC3D allows you to
create four kinds of fields:

1. Scalar Field – to display scalar quantities associated with single
   pixels

2. Cell Level Scalar Field – to display scalar quantities associated
   with cells

3. Vector Field - to display vector quantities associated with single
   pixels

4. Cell Level Vector Field - to display vector quantities associated
   with cells

You can take look at ``CompuCellPythonTutorial/ExtraFields`` to see an
example of a simulation that uses all four kinds of fields. The Python
syntax used to create and manipulate custom fields is relatively simple
but quite hard to memorize. Fortunately Twedit++ has ``CC3DPython->Extra Fields``
menu that inserts code snippets to create/manage fields.

Scalar Field – pixel based
---------------------------

Let’s look at the steppable that creates and manipulates scalar cell
field. This field is implemented as Numpy float array and you can use
Numpy functions to manipulate this field.

.. code-block:: python

    from math import *

    class ExtraFieldVisualizationSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=10):
            SteppableBasePy.__init__(self, _simulator, _frequency)
            self.scalarField = CompuCellSetup.createScalarFieldPy(self.dim, "ExtraField")

        def step(self, mcs):

            self.scalarField[:, :, :] = 0.0  # clear field

            for x in xrange(self.dim.x):
                for y in xrange(self.dim.y):
                    for z in xrange(self.dim.z):

                        if (not mcs % 20):
                            self.scalarField[x, y, z] = x * y

                        else:
                            self.scalarField[x, y, z] = sin(x * y)


The scalar field (we called it ExtraField) is created in the
``__init__`` function of the steppable using

.. code-block:: python

    self.createScalarFieldPy(self.dim,"ExtraField").

**Important:** Make sure that all calls to functions creating fields are
in the ``__init__`` functions so that the Player can display them
correctly.

In the step function we initialize self.scalarField using slicing
operation:

.. code-block:: python

    self.scalarField[:, :, :]

In Python slicing convention, a single colon means all indices – here we
put three colons for each axis which is equivalent to selecting all
pixels.

Following lines in the step functions iterate over every pixel in the
simulation and if MCS is divisible by 20 then self.scalarField is
initialized with ``x*y`` value if MCS is not divisible by 20 than we
initialize scalar field with ``sin(x*y)`` function. Notice, that we
imported all functions from the math Python module so that we can get
sin function to work.

SteppableBasePy has convenience function called self.everyPixel (``CC3D Python->Visit->All Lattice Pixels``)
which allows us to compact triple loop to just one line:

.. code-block:: python

    for x,y,z in self.everyPixel():
        if (not mcs%20):
            self.scalarField[x,y,z]=x*y
        else:
            self.scalarField[x,y,z]=sin(x*y)


If we would like to iterate over x axis indices with step 5, over y
indices with step 10 and over z axis indices with step 4 we would
replace first line in the above snippet with.

.. code-block:: python

    for x,y,z in self.everyPixel(5,10,4):

You can still use triple loops if you like but shorter syntax leads to a
cleaner code.

Vector Field – pixel based
---------------------------

By analogy to pixel based scalar field we can create vector field. Let’s
look at the example code:

.. code-block:: python

    class VectorFieldVisualizationSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=10):
            SteppableBasePy.__init__(self, _simulator, _frequency)
            self.vectorField = self.createVectorFieldPy("VectorField")

        def step(self, mcs):
            self.vectorField[:, :, :, :] = 0.0  # clear vector field

            for x, y, z in self.everyPixel(10, 10, 5):
                self.vectorField[x, y, z] = [x * random(), y * random(), z * random()]

Th code is very similar to the previous steppable. In the ``__init__``
function we create pixel based vector field , in the step function we
initialize it first to with zero vectors and later we iterate over
pixels using steps ``10``, ``10``, ``5`` for ``x``, ``y``, ``z``
axes respectively and to these select lattice pixels we assign ``[x*random(), y*random(), z*random()]``
vector. Internally, ``self.vectorField`` is implemented as ``Numpy`` array:

.. code-block:: python

    np.zeros(shape=(_dim.x, _dim.y, _dim.z,3), dtype=np.float32)

Scalar Field – cell level
--------------------------

Pixel based fields are appropriate for situations where we want to
assign scalar of vector to particular lattice locations. If, on the
other hand, we want to label cells with a scalar or a vector we need to
use cell level field (scalar or vector). It is still possible to use
pixel-based fields but we assure you that the code you would write would
be ver ugly at best.

Internally cell-based scalar field is implemented as a map or a
dictionary indexed by cell id (although in Python instead of passing
cell id we pass cell object to make syntax cleaner). Let us look at an
example code:

.. code-block:: python

    class IdFieldVisualizationSteppable(SteppableBasePy):
        def __init__(self,_simulator,_frequency=10):
            SteppableBasePy.__init__(self,_simulator,_frequency)
            self.scalarCLField=self.createScalarFieldCellLevelPy("IdField")

        def step(self,mcs):
            self.scalarCLField.clear()
            for cell in self.cellList:
                self.scalarCLField[cell]=cell.id*random()

As it was the case with other fields we create cell level scalar field
in the ``__init__`` function using self.createScalarFieldCellLevelPy. In
the step function we first clear the field – this simply removes all
entries from the dictionary. If you forget to clean dictionary before
putting new values you may end up with stray values from the previous
step. Inside the loop over all cells we assign random value to each cell.
When we plot ``IdField`` in the player we will see that cells have different
color labels. If we used pixel-based field to accomplish same task we
would have to manually assign same value to all pixels belonging to a
given cell. Using cell level fields we save ourselves a lot of work and
make code more readable.

Vector Field – cell level
--------------------------

We can also associate vectors with cells. The code below is analogous to
the previous example:

.. code-block::python

    class VectorFieldCellLevelVisualizationSteppable(SteppableBasePy):
        def __init__(self,_simulator,_frequency=10):
            SteppableBasePy.__init__(self,_simulator,_frequency)

            self.vectorCLField=self.createVectorFieldCellLevelPy("VectorFieldCellLevel")

        def step(self,mcs):
            self.vectorCLField.clear()
            for cell in self.cellList:

                if cell.type==1:
                    self.vectorCLField[cell]=[cell.id*random(),cell.id*random(),0]


Inside ``__init__`` function we create cell-level vector field using
self.createVectorFieldCellLevelPy function. In the step function we
clear field and then iterate over all cells and assign random vector to
each cell. When we plot this field on top cell borders you will see that
vectors are anchored in “cells’ corners” and not at the COM. This is
because such rendering is faster.

You should remember that all those 4 kinds of field discussed here are
for display purposes only. They do not participate in any calculations
done by C++ core code and there is no easy way to pass values of those
fields to the CC3D computational core.
