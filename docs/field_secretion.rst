Field Secretion | Interacting with PDE Solver Fields
======================================================

Related: 
    - `Secretion Reference <reference_field_secretor.html>`_
    - `Secretion Guide <secretion.html>`_ 
    - `Secretion (legacy version for pre-v3.5.0) <legacy_secretion.html>`_
    
****************************************

Methods
****************************

1. fieldSecretor.``secreteInsideCellTotalCount`` – returns a ``FieldSecretorResult` object that contains the summary of the secretion/uptake operation.  Most importantly, when we access ``total_amount``
member of the ``res`` object we get the total amount that was added/uptaken from the chemical field e.g. :

2. ``cell.lambdaVolume`` – 

****************************

Every field declared in a PDE solver is accessible by name in Python from every registered steppable using
the property ``field``, which allows us to retrieve and change the value of a field at a particular point by
using the coordinates of the point as indices of the field. For example, if we have a PDE solver running
with a field named ``ATTR`` and we would like to increment the value of ``ATTR`` at a point ``(10, 20, 30)``,
we could write in a steppable,

.. code-block:: python

    self.field.ATTR[10, 20, 30] += 1

Likewise, we can manipulate a field using slicing operators, such as setting the value of our ``ATTR`` field
to a value of ``1.0`` along a line,

.. code-block:: python

    self.field.ATTR[0:11, 20, 0] = 1.0

.. note::

    The functionality described up to this point is also applicable for extra scalar and vector fields. They can also be accessed and manipulated using the ``field`` property of a steppable. For more on extra fields, see :ref:`AddingExtraFields`.

Field Secretion
---------------

PDE solvers in CC3D allow you to specify secretion properties
individually for each cell type. However, there are situations where **you
want only a single cell to secrete the chemical**. In this case, you have
to use ``Secretor`` objects. In Twedit++, go to the ``CC3D Python->Secretion`` menu
to see what options are available. Let us look at the example code to
understand what kind of capabilities CC3D offers in this regard (see
``Demos/SteppableDemos/Secretion``):

.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self, frequency=1):
            SecretionBasePy.__init__(self, frequency)

        def step(self, mcs):
            attr_secretor = self.get_field_secretor("ATTR")
            for cell in self.cell_list:
                if cell.type == self.WALL:
                    # Choose one of the secretion methods according to your use case
                    attr_secretor.secreteInsideCellAtBoundaryOnContactWith(cell, 300, [self.WALL])
                    attr_secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, 300, [self.MEDIUM])
                    attr_secretor.secreteInsideCell(cell, 300)
                    attr_secretor.secreteInsideCellAtBoundary(cell, 300)
                    attr_secretor.secreteOutsideCellAtBoundary(cell, 500)
                    attr_secretor.secreteInsideCellAtCOM(cell, 300)

.. note::

    [History] As we mentioned in the introductory section, we switched capitalization conventions for Python functions. For example, we use ``get_field_secretor`` and not getFieldSecretor. However, there are function calls in the above snippet that do not follow this convention - e.g. ``secreteInsideCell``. This is because those functions belong to a C++ object (here, ``attr_secretor``) that is accessed through Python. We decided to keep those two conventions (snake-case for pure Python functions) and Pascal-case for C++ functions. It provides a clue for where various functions come from.

In the step function, we obtain a handle to field secretor object that
operates on diffusing field ``ATTR``. In the for loop where we go over all
cells in the simulation we pick cells that are of type 3 (notice we use
a numeric value here instead of an alias). Inside the loop, we use
``secreteInsideCell``, ``secreteInsideCellAtBoundary``,
``secreteOutsideCellAtBoundary``, and ``secreteInsideCellAtCOM`` member
functions of the secretor object to carry out secretion in the region
occupied by a given cell. See the `secretion reference guide <secretion.html>`_ for more details.

``secreteInsideCell``: increases concentration by a
given amount (here ``300``) in every pixel occupied by a cell.

``secreteInsideCellAtBoundary`` and ``secreteOutsideCellAtBoundary``: increases
concentration but only in pixels at the cell's boundary. 
The "inside" version chooses the cell's pixels (recommended) whereas 
the "outside" version chooses pixels touching the cell's boundary. 

``secreteInsideCellAtCOM``: increases concentration for the single pixel that is
closest to the cell's center of mass.

Notice that ``SecretionSteppable`` inherits from ``SecretionBasePy``. We do this
to ensure that Python-based secretion plays nicely with PDE solvers.
This requires that such steppable must be called before MCS, or rather
before the PDE solvers start evolving the field. If we look at the
definition of ``SecretionBasePy``, we will see that it inherits from
``SteppableBasePy``. In the ``__init__`` function, it sets the 
``self.runBeforeMCS`` flag to ``1``:

.. code-block:: python

    class SecretionBasePy(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)
            self.runBeforeMCS = 1

Direct (but somewhat naive) Implementation
------------------------------------------
Now, for the sake of completeness, let us implement cell secretion at
the COM using alternative code:

.. code-block:: python

    field = self.field.ATTR
    lmf_length = 1.0;
    x_scale = 1.0
    y_scale = 1.0
    z_scale = 1.0
    # FOR HEX LATTICE IN 2D
    #         lmf_length = sqrt(2.0/(3.0*sqrt(3.0)))*sqrt(3.0)
    #         x_scale = 1.0
    #         y_scale = sqrt(3.0)/2.0
    #         z_scale = sqrt(6.0)/3.0

    for cell in self.cell_list:
        # converting from real coordinates to pixels
        x_cm = int(cell.xCOM / (lmf_length * x_scale))
        y_cm = int(cell.yCOM / (lmf_length * y_scale))

        if cell.type == 3:
            field[x_cm, y_cm, 0] = field[x_cm, y_cm, 0] + 10.0


As you can tell, it is significantly more work than our original
solution.

Lattice Conversion Factors
---------------------------

In the code where we manually implement secretion at the cell's COM, we use
strange-looking variables like ``lmf_length``, ``x_scale`` and ``y_scale``. 
CC3D allows users to run simulations on square (Cartesian) or hexagonal lattices.
Under the hood, these two lattices rely on the Cartesian lattice. However,
distances between neighboring pixels are different on Cartesian and hex
lattices. This is what those 3 variables accomplish. The take-home
message is that to convert COM coordinates on hex lattice to Cartesian
lattice coordinates, we need to use converting factors. Please see
writeup **“Hexagonal Lattices in CompuCell3D”**
(http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf)
for more information. To convert between hex and Cartesian lattice
coordinates we can use ``SteppableBasePy`` built-in functions
(``self.cartesian_2_hex``, and ``self.hex_2_cartesian``). 
You can use Twedit++'s Python snippets menu: Distances → Vectors → Transformations to get code like this:

.. code-block:: python

    hex_coords = self.cartesian_2_hex(coords=[10, 20, 11])
    pt = self.hex_2_cartesian(coords=[11.2, 13.1, 21.123])


Tracking Amount of Secreted (Uptaken) Chemical
-----------------------------------------------

While the ability to have fine control over how the chemicals get secreted/uptaken
is a useful feature, quite often we would like to know the total amount of the chemical that was added
to the simulation as a result of the call to one of the ``secrete`` or ``uptake`` functions from the secretor object.

Let us rewrite the previous example using the API that facilitates tracking the amount of
chemical that was added:


.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self, frequency=1):
            SecretionBasePy.__init__(self, frequency)

        def step(self, mcs):
            attr_secretor = self.get_field_secretor("ATTR")
            for cell in self.cell_list:
                if cell.type == 3:

                    res = attr_secretor.secreteInsideCellTotalCount(cell, 300)
                    print('secreted  ', res.tot_amount, ' inside cell')
                    res = attr_secretor.secreteInsideCellAtBoundaryTotalCount(cell, 300)
                    print('secreted  ', res.tot_amount, ' inside cell at the boundary')
                    res = attr_secretor.secreteOutsideCellAtBoundaryTotalCount(cell, 500)
                    print('secreted  ', res.tot_amount, ' outside the cell at the boundary')
                    res = attr_secretor.secreteInsideCellAtCOMTotalCount(cell, 300)
                    print('secreted  ', res.tot_amount, ' inside the cell at the COM')

As you can see, the calls that return the total amount of chemical added/uptaked are the same calls as we
used in our previous example except we add ``TotalCount`` to the name of the function. The new function, ``secreteInsideCellTotalCount``, returns an object called ``res`` that is an instance of the ``FieldSecretorResult`` class
that contains the summary of the secretion/uptake operation. 
Most importantly, when we access ``total_amount``
member of the ``res`` object we get the total amount that was added/uptaken from the chemical field e.g. :


.. code-block:: python

    res = attr_secretor.secreteInsideCellTotalCount(cell, 300)
    print('secreted  ', res.tot_amount, ' inside cell')


Volume Integrals
----------------
FieldSecretor objects also provide convenience methods to easily and quickly compute a volume
integral of a PDE solver field over a particular cell or the entire simulation domain. Say we
would like to construct another steppable to be also simulated with the previously described
``SecretionSteppable``, and say this additional steppable computes the volume integral of the
diffusing field ``ATTR`` everywhere for each cell. Such a steppable could look like the following...

Obtaining how much chemical the cell is exposed to (sampling)
-------------------------------------------------------------

To fetch the total amount of chemical a cell is exposed to we can simpli call ``secretor_object.amountSeenByCell(cell)``. In more detail

.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self,frequency=1):
            SecretionBasePy.__init__(self,frequency)

        def step(self,mcs):
            attr_secretor = self.get_field_secretor("ATTR")
            for cell in self.cell_list:
                print('Cell exposed to  ', attr_secretor.amountSeenByCell(cell), 'units of ATTR')

.. code-block:: python

    class IntegralSteppable(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):
            attr_secretor = self.get_field_secretor("ATTR")
            total_attr = attr_secretor.totalFieldIntegral()
            for cell in self.cell_list:
                cell_total_attr = attr_secretor.amountSeenByCell(cell)

Like in ``SecretionSteppable``, a field secretor object is obtained for the diffusing field
``ATTR``. However, ``IntegralSteppable`` computes the volume integral of the ``ATTR`` field over
the simulation domain using the field secretor method ``totalFieldIntegral`` (and stores it in
``total_attr``). Likewise, in a loop over every cell, ``IntegralSteppable`` then computes the
volume integral of the ``ATTR`` field over the domain of each cell using the field secretor method
``amountSeenByCell`` by simply passing as argument a cell of interest (and stores it in
``cell_total_attr``).

Algorithmic Considerations
--------------------------

Note that, in the previous example, ``IntegralSteppable`` inherits from ``SteppableBasePy`` instead
of from ``SecretionBasePy``. This distinction is important because CC3D calls ``step`` on all steppables
that inherit from ``SteppableBasePy`` `after` executing diffusion by the PDE solvers. In our case, we are
then enforcing that computing volume integrals occurs `after` diffusion and secretion have been
implemented for a simulation step. If we were to simulate ``SecretionSteppable`` and
``IntegralSteppable`` with a PDE solver, then the order of calls to ``step`` would be executed as follows,

- ``SecretionSteppable`` instance performs cell-based secretion for ``ATTR`` field
- PDE solver performs diffusion of ``ATTR`` field
- ``IntegralSteppable`` instance computes volume integrals of ``ATTR`` field
