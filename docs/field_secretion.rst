Field Secretion
===============

PDE solvers in the CC3D allow users to specify secretion properties
individually for each cell type. However, there are situations where you
want only a single cell to secrete the chemical. In this case you have
to use ``Secretor`` objects. In Twedit++, go to ``CC3D Python->Secretion`` menu
to see what options are available. Let us look at the example code to
understand what kind of capabilities CC3D offers in this regard (see
``Demos/SteppableDemos/Secretion``):

.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self,_simulator,_frequency=1):
            SecretionBasePy.__init__(self,_simulator, _frequency)

        def step(self,mcs):
            attrSecretor=self.getFieldSecretor("ATTR")
            for cell in self.cellList:
                if cell.type==3:
                    attrSecretor.secreteInsideCell(cell,300)
                    attrSecretor.secreteInsideCellAtBoundary(cell,300)
                    attrSecretor.secreteOutsideCellAtBoundary(cell,500)
                    attrSecretor.secreteInsideCellAtCOM(cell,300)

In the step function we obtain a handle to field secretor object that
operates on diffusing field ``ATTR``. In the for loop where we go over all
cells in the simulation we pick cells which are of type 3 (notice we use
numeric value here instead of an alias). Inside the loop we use
secreteInsideCell, secreteInsideCellAtBoundary,
secreteOutsideCellAtBoundary, and secreteInsideCellAtCOM member
functions of the secretor object to carry out secretion in the region
occupied by a given cell. ``secreteInsideCell`` increases concentration by a
given amount (here ``300``) in every pixel occupied by a cell.
``secreteInsideCellAtBoundary`` and ``secreteOutsideCellAtBoundary`` increase
concentration but only in pixels which at the boundary but are inside
cell or outside pixels touching cell boundary. Finally,
``secreteInsideCellAtCOM`` increases concentration in a single pixel that is
closest to cell center of mass of a cell.

Notice that ``SecretionSteppable`` inherits from ``SecretionBasePy11. We do this
to ensure that Python-based secretion plays nicely with PDE solvers.
This requires that such steppable must be called before MCS, or rather
before the PDE solvers start evolving the field. If we look at the
definition of ``SecretionBasePy`` we will see that it inherits from
``SteppableBasePy`` and in the ``__init__`` function it sets
``self.runBeforeMCS`` flag to ``1``:

.. code-block:: python

    class SecretionBasePy(SteppableBasePy):
        def __init__(self,_simulator,_frequency=1):
            SteppableBasePy.__init__(self,_simulator,_frequency)
            self.runBeforeMCS=1

Now, for the sake of completeness, let us implement cell secretion at
the COM using alternative code:

.. code-block:: python

    self.field = self.getConcentrationField('ATTR')
    lmfLength = 1.0;
    xScale = 1.0
    yScale = 1.0
    zScale = 1.0
    # FOR HEX LATTICE IN 2D
    #         lmfLength=sqrt(2.0/(3.0*sqrt(3.0)))*sqrt(3.0)
    #         xScale=1.0
    #         yScale=sqrt(3.0)/2.0
    #         zScale=sqrt(6.0)/3.0

    for cell in self.cellList:
        # converting from real coordinates to pixels
        xCM = int(cell.xCOM / (lmfLength * xScale))
        yCM = int(cell.yCOM / (lmfLength * yScale))

        if cell.type == 3:
            self.field[xCM, yCM, 0] = self.field[xCM, yCM, 0] + 10.0


As you can tell, it is significantly more work than our original
solution.

Lattice Conversion Factors
---------------------------

In the code where we manually implement secretion at the cell’sCOM we use
strange looking variables lmfLength, xScale and yScale. CC3D allows
users to run simulations on square (Cartesian) or hexagonal lattices.
Under the hood these two lattices rely on the Cartesian lattice. However
distances between neighboring pixels are different on Cartesian and hex
lattice. This is what those 3 variables accomplish. The take home
message is that to convert COM coordinates on hex lattice to Cartesian
lattice coordinates we need to use converting factors. Please see
writeup **“Hexagonal Lattices in CompuCell3D”**
(http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf)
for more information. To convert between hex and Cartesian lattice
coordinates we can use PySteppableBase built-in functions
(``self.cartesian2Hex``, ``and self.hex2Cartesian``) – see also Twedit++ CC3D
Python menu Distances, Vectors, Transformations:

.. code-block:: python

    hex_coords = self.cartesian2Hex(_in=[10, 20, 11])
    pt = self.hex2Cartesian(_in=[11.2, 13.1, 21.123])
