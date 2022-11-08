Interacting with PDE Solver Fields
==================================

Every field declared in a PDE solver is accessible by name in Python from every registered steppable using
the property ``field``, which allows us to retrieve and change the value of a field at a particular point by
using the coordinates of the point as indices of the field. For example, if we have a PDE solver running
with a field named ``ATTR`` and we would like to increment the value of ``ATTR`` at a point ``(10, 20, 30)``,
we could write in a steppable,

.. code-block:: python

    self.field.ATTR[10, 20, 30] += 1

Likewise we can manipulate a field using slicing operators, such as setting the value of our ``ATTR`` field
to a value of ``1.0`` along a line,

.. code-block:: python

    self.field.ATTR[0:11, 20, 0] = 1.0

.. note::

    The functionality described up to this point is also applicable for extra scalar and vector fields. They can also be accessed and manipulated using the ``field`` property of a steppable. For more on extra fields, see :ref:`AddingExtraFields`.

Field Secretion
---------------

PDE solvers in the CC3D allow users to specify secretion properties
individually for each cell type. However, there are situations where you
want only a single cell to secrete the chemical. In this case you have
to use ``Secretor`` objects. In Twedit++, go to ``CC3D Python->Secretion`` menu
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
                    attr_secretor.secreteInsideCellAtBoundaryOnContactWith(cell, 300, [self.WALL])
                    attr_secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, 300, [self.MEDIUM])
                    attr_secretor.secreteInsideCell(cell, 300)
                    attr_secretor.secreteInsideCellAtBoundary(cell, 300)
                    attr_secretor.secreteOutsideCellAtBoundary(cell, 500)
                    attr_secretor.secreteInsideCellAtCOM(cell, 300)

.. note::

    As we mentioned in the introductory section we switched Python functions capitalization conventions. For example we use ``get_field_secretor`` and not getFieldSecretor. However, there are function calls in the above snippet that do not follow this convention - e.g. ``secreteInsideCell``. This is because those functions belong to a C++ object (here, ``attr_secretor``) that is accessed through Python. We decided to keep those two conventions (snake-case for pure Python functions) and Pascal-case for C++ functions. It should help users with identification of where various functions come from.

In the step function we obtain a handle to field secretor object that
operates on diffusing field ``ATTR``. In the for loop where we go over all
cells in the simulation we pick cells which are of type 3 (notice we use
numeric value here instead of an alias). Inside the loop we use
``secreteInsideCell``, ``secreteInsideCellAtBoundary``,
``secreteOutsideCellAtBoundary``, and ``secreteInsideCellAtCOM`` member
functions of the secretor object to carry out secretion in the region
occupied by a given cell. ``secreteInsideCell`` increases concentration by a
given amount (here ``300``) in every pixel occupied by a cell.
``secreteInsideCellAtBoundary`` and ``secreteOutsideCellAtBoundary`` increase
concentration but only in pixels which at the boundary but are inside
cell or outside pixels touching cell boundary. Finally,
``secreteInsideCellAtCOM`` increases concentration in a single pixel that is
closest to cell center of mass of a cell.

Notice that ``SecretionSteppable`` inherits from ``SecretionBasePy``. We do this
to ensure that Python-based secretion plays nicely with PDE solvers.
This requires that such steppable must be called before MCS, or rather
before the PDE solvers start evolving the field. If we look at the
definition of ``SecretionBasePy`` we will see that it inherits from
``SteppableBasePy`` and in the ``__init__`` function it sets
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

In the code where we manually implement secretion at the cell’sCOM we use
strange looking variables ``lmf_length``, ``x_scale`` and ``y_scale``. CC3D allows
users to run simulations on square (Cartesian) or hexagonal lattices.
Under the hood these two lattices rely on the Cartesian lattice. However
distances between neighboring pixels are different on Cartesian and hex
lattice. This is what those 3 variables accomplish. The take home
message is that to convert COM coordinates on hex lattice to Cartesian
lattice coordinates we need to use converting factors. Please see
writeup **“Hexagonal Lattices in CompuCell3D”**
(http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf)
for more information. To convert between hex and Cartesian lattice
coordinates we can use ``SteppableBasePy`` built-in functions
(``self.cartesian_2_hex``, and ``self.hex_2_cartesian``) – see also Twedit++ CC3D
Python menu Distances, Vectors, Transformations:

.. code-block:: python

    hex_coords = self.cartesian_2_hex(coords=[10, 20, 11])
    pt = self.hex_2_cartesian(coords=[11.2, 13.1, 21.123])


Tracking Amount of Secreted (Uptaken) Chemical
-----------------------------------------------

While the ability to have fine control over how the chemicals get secreted/uptaken
is a useful feature, quite often we would like to know the total amount of the chemical that was added
to the simulation as a result of the call to one of the ``secrete`` or ``uptake`` functions from he secretor object.

Let us rewrite previous example using the API ythat facilitates tracking of the amount of
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

As you can see the calls to that return the total amount of chemical added/uptaked are the same calls as we
used in our previous example except we add ``TotalCount`` to the name of the function. The new function e.g.
``secreteInsideCellTotalCount`` returns object ``res`` that is an instance of ``FieldSecretorResult`` class
that contains the summary of the secreion/uptake operation. Most importantly when we access ``total_amount``
member of the ``res`` object we get the total amount that was added/uptaken from the chemical field e.g. :


.. code-block:: python

    res = attr_secretor.secreteInsideCellTotalCount(cell, 300)
    print('secreted  ', res.tot_amount, ' inside cell')

For completeness we present a complete list of C++ signatures of all the functions that can be used to fine-control
how uptake/secretion happens in CC3D. All those functions are members of the ``secretor`` object and are
accessible from Python

.. code-block:: cpp

    bool _secreteInsideCellConstantConcentration(CellG * _cell, float _amount);

    FieldSecretorResult _secreteInsideCellConstantConcentrationTotalCount(CellG * _cell, float _amount);

    bool _secreteInsideCell(CellG * _cell, float _amount);

    FieldSecretorResult _secreteInsideCellTotalCount(CellG * _cell, float _amount);

    bool _secreteInsideCellAtBoundary(CellG * _cell, float _amount);

    FieldSecretorResult _secreteInsideCellAtBoundaryTotalCount(CellG * _cell, float _amount);

    bool _secreteInsideCellAtBoundaryOnContactWith(CellG * _cell, float _amount,
    const std::vector<unsigned char> & _onContactVec);

    FieldSecretorResult _secreteInsideCellAtBoundaryOnContactWithTotalCount(CellG * _cell,
    float _amount, const std::vector<unsigned char> & _onContactVec);

    bool _secreteOutsideCellAtBoundary(CellG * _cell, float _amount);

    FieldSecretorResult _secreteOutsideCellAtBoundaryTotalCount(CellG * _cell, float _amount);

    bool _secreteOutsideCellAtBoundaryOnContactWith(CellG * _cell, float _amount,
    const std::vector<unsigned char> & _onContactVec);

    FieldSecretorResult  _secreteOutsideCellAtBoundaryOnContactWithTotalCount(CellG * _cell,
    float _amount, const std::vector<unsigned char> & _onContactVec);

    bool secreteInsideCellAtCOM(CellG * _cell, float _amount);

    FieldSecretorResult secreteInsideCellAtCOMTotalCount(CellG * _cell, float _amount);

    bool _uptakeInsideCell(CellG * _cell, float _maxUptake, float _relativeUptake);

    FieldSecretorResult _uptakeInsideCellTotalCount(CellG * _cell, float _maxUptake, float _relativeUptake);

    bool _uptakeInsideCellAtBoundary(CellG * _cell, float _maxUptake, float _relativeUptake);

    FieldSecretorResult _uptakeInsideCellAtBoundaryTotalCount(CellG * _cell, float _maxUptake, float _relativeUptake);

    bool _uptakeInsideCellAtBoundaryOnContactWith(CellG * _cell, float _maxUptake,
    float _relativeUptake,const std::vector<unsigned char> & _onContactVec);

    FieldSecretorResult _uptakeInsideCellAtBoundaryOnContactWithTotalCount(CellG * _cell,
    float _maxUptake, float _relativeUptake, const std::vector<unsigned char> & _onContactVec);

    bool _uptakeOutsideCellAtBoundary(CellG * _cell, float _maxUptake, float _relativeUptake);

    FieldSecretorResult _uptakeOutsideCellAtBoundaryTotalCount(CellG * _cell, float _maxUptake, float _relativeUptake);

    bool _uptakeOutsideCellAtBoundaryOnContactWith(CellG * _cell, float _maxUptake,
     float _relativeUptake,const std::vector<unsigned char> & _onContactVec);

    FieldSecretorResult _uptakeOutsideCellAtBoundaryOnContactWithTotalCount(CellG * _cell,
    float _maxUptake, float _relativeUptake, const std::vector<unsigned char> & _onContactVec);

    bool uptakeInsideCellAtCOM(CellG * _cell, float _maxUptake, float _relativeUptake);

    FieldSecretorResult  uptakeInsideCellAtCOMTotalCount(CellG * _cell, float _maxUptake, float _relativeUptake);

For example if we want to use ``uptakeInsideCellAtCOMTotalCount(CellG * _cell, float _maxUptake, float _relativeUptake);``
from python we would use the following code:

.. code-block:: python

    ...
    res = attr_secretor.uptakeInsideCellAtCOMTotalCount(cell, 3, 0.1)
    print('uptaken ', res.tot_amount, ' inside cell and the COM')

In this case  ``_cell`` is a ``cell`` object that we normally deal with in Python, ``_maxUptake`` has value of ``3``
and ``_relativeUptake`` is set to ``0.1``

In similar fashion we could use remaining functions listed above

Volume Integrals
----------------
Field secretor objects also provide convenience methods to easily and quickly compute a volume
integral of a PDE solver field over a particular cell or the entire simulation domain. Say we
would like to construct another steppable to be also simulated with the previously described
``SecretionSteppable``, and say this additional steppable computes the volume integral of the
diffusing field ``ATTR`` everywhere, and in each cell. Such a steppable could look like the following,

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
