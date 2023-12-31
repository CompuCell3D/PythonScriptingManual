.. _AddingExtraFields:

Adding and managing extra fields for visualization purposes
===========================================================

Quite often in your simulation you will want to label cells using scalar
field, vector fields or simply create your own scalar or vector fields
which are fully managed by you from the Python level. CC3D allows you to
create four kinds of fields:

#. Scalar Field – to display scalar quantities associated with single
   pixels

#. Cell Level Scalar Field – to display scalar quantities associated
   with cells

#. Vector Field - to display vector quantities associated with single
   pixels

#. Cell Level Vector Field - to display vector quantities associated
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

    from cc3d.core.PySteppables import *
    from random import random
    from math import sin


    class ExtraFieldVisualizationSteppable(SteppableBasePy):
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)
            self.create_scalar_field_py("ExtraField")

        def step(self, mcs):

            cell = self.field.Cell_Field[20, 20, 0]
            print('cell=', cell)

            # clear field
            self.field.ExtraField[:, :, :] = 10.0

            for x, y, z in self.every_pixel(4, 4, 1):
                if not mcs % 20:
                    self.field.ExtraField[x, y, z] = x * y
                else:
                    self.field.ExtraField[x, y, z] = sin(x * y)

The scalar field (we called it ``ExtraField``) is declared in the
``__init__`` function of the steppable using

.. code-block:: python

    self.create_scalar_field_py("ExtraField")

.. note::

    Ideally you would declare exrta fields in the ``__init__`` function but if you create them elsewhere they will work as well. HOwever in certain situations you may notice that fields declared outside ``__init__`` may be missing

from e.g. player menus. Normally it is not a big deal but if you want to have full functionality associated with the fields declare them inside ``__init__``


In the step function we initialize ``ExtraField`` using slicing operation:

.. code-block:: python

    self.field.ExtraField[:, :, :] = 10.0

In Python slicing convention, a single colon means all indices – here we
put three colons for each axis which is equivalent to selecting all
pixels. Notice how we use ``self.field.ExtraField`` construct to access the field.

It is perfectly fine (and faster too if you acces field repeatedly) to split this int two lines:

.. code-block:: python

    extra_field = self.field.ExtraField
    extra_field[:, :, :] = 10


Following lines in the step functions iterate over every pixel in the
simulation and if MCS is divisible by 20 then self.scalarField is
initialized with ``x*y`` value if MCS is not divisible by 20 than we
initialize scalar field with ``sin(x*y)`` function. Notice, that we
imported all functions from the ``math`` Python module so that we can get
sin function to work.

``SteppableBasePy`` provides convenience function called ``self.every_pixel`` (``CC3D Python->Visit->All Lattice Pixels``) that facilitates compacting triple loop to just one line:

.. code-block:: python

    for x,y,z in self.every_pixel():
        if not mcs % 20:
            self.field.ExtraField[x, y, z]=x*y
        else:
            self.field.ExtraField[x, y, z]=sin(x*y)


If we would like to iterate over x axis indices with step 5, over y
indices with step 10 and over z axis indices with step 4 we would
replace first line in the above snippet with.

.. code-block:: python

    for x, y, z in self.every_pixel(5,10,4):

You can still use triple loops if you like but shorter syntax leads to a
cleaner code.

Vector Field – pixel based
---------------------------

By analogy to pixel based scalar field we can create vector field. Let’s
look at the example code:

.. code-block:: python

    class VectorFieldVisualizationSteppable(SteppableBasePy):
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)
            self.create_vector_field_py("VectorField")

        def step(self, mcs):
            vec_field = self.field.VectorField

            # clear vector field
            vec_field[:, :, :, :] = 0.0

            for x, y, z in self.everyPixel(10, 10, 5):
                vec_field[x, y, z] = [x * random(), y * random(), z * random()]

Th code is very similar to the previous steppable. In the ``__init__``
function we create pixel based vector field , in the step function we
initialize it first to with zero vectors and later we iterate over
pixels using steps ``10``, ``10``, ``5`` for ``x``, ``y``, ``z``
axes respectively and to these select lattice pixels we assign ``[x*random(), y*random(), z*random()]``
vector. Internally, ``self.field.VectorField`` is implemented as ``numpy`` array:

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
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)

        def start(self):
            # note if you create field outside constructor this field will not be properly
            # initialized if you are using restart snapshots. It is OK as long as you are aware of this limitation
            self.create_scalar_field_cell_level_py("IdFieldNew")

        def step(self, mcs):
            # clear id field
            try:
                id_field = self.field.IdFieldNew
                id_field.clear()
            except KeyError:
                # an exception might occur if you are using restart snapshots to restart simulation
                # because field has been created outside constructor
                self.create_scalar_field_cell_level_py("IdFieldNew")
                id_field = self.field.IdFieldNew

            for cell in self.cell_list:
                id_field[cell] = cell.id * random()

As it was the case with other fields we create cell level scalar field
in the ``__init__`` function using ``self.create_scalar_field_cell_level_py``. In
the step function we first clear the field – this simply removes all
entries from the dictionary. If you forget to clean dictionary before
putting new values you may end up with stray values from the previous
step. Inside the loop over all cells we assign random value to each cell.
When we plot ``IdFieldNew`` in the player we will see that cells have different
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
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)

            self.create_vector_field_cell_level_py("VectorFieldCellLevel")

        def step(self, mcs):
            vec_field = self.field.VectorFieldCellLevel

            vec_field.clear()
            for cell in self.cell_list:

                if cell.type == 1:
                    vec_field[cell] = [cell.id * random(), cell.id * random(), 0]
                    vec = vec_field[cell]
                    vec *= 2.0
                    vec_field[cell] = vec

Inside ``__init__`` function we create cell-level vector field using
``self.create_vector_field_cell_level_py`` function. In the step function we
clear field and then iterate over all cells and assign random vector to
each cell. When we plot this field on top cell borders you will see that
vectors are anchored in “cells’ corners” and not at the COM. This is
because such rendering is faster.

You should remember that all those 4 kinds of field discussed here are
for display purposes only. They do not participate in any calculations
done by C++ core code and there is no easy way to pass values of those
fields to the CC3D computational core.
