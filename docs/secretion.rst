Secretion / SecretionLocalFlex Plugin
--------------------------------------

Secretion "by cell type" can and should be handled by the appropriate
PDE solver. To implement secretion in individual cells using Python we
can use secretion plugin defined in the CC3DML as:

.. code-block:: xml

    <Plugin Name="Secretion"/>

or as:

.. code-block:: xml

    <Plugin Name="SecretionLocalFlex"/>


The inclusion of the above code in the CC3DML will allow users to
implement secretion for individual cells from Python.

.. note::

    Secretion for individual cells invoked via Python will be called only once per
    MCS.

.. warning::

    Secretion plugin can be used to implement secretion by
    cell type however **we strongly advise against doing so**. Defining
    secretion by cell type in the ``Secretion`` plugin will lead to performance
    degradation on multi-core machines. Please see section below for more
    information if you are still interested in using secretion by cell-type
    inside ``Secretion`` plugin

Typical use of secretion from Python is demonstrated best in the example
below:

.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self, _simulator, _frequency=1):
            SecretionBasePy.__init__(self, _simulator, _frequency)

        def step(self, mcs):
            attrSecretor = self.getFieldSecretor("ATTR")
            for cell in self.cellList:
                if cell.type == 3:
                    attrSecretor.secreteInsideCell(cell, 300)
                    attrSecretor.secreteInsideCellAtBoundary(cell, 300)
                    attrSecretor.secreteOutsideCellAtBoundary(cell, 500)
                    attrSecretor.secreteInsideCellAtCOM(cell, 300)
                elif cell.type == 2:
                    attrSecretor.secreteInsideCellConstantConcentration(cell, 300)

.. note::

    Instead of using ``SteppableBasePy`` class we are using
    ``SecretionBasePy`` class. The reason for this is that in order for
    secretion plugin with secretion modes accessible from Python to behave
    exactly as previous versions of PDE solvers (where secretion was done
    first followed by the "diffusion" step) we have to ensure that secretion
    steppable implemented in Python is called **before** each Monte Carlo
    Step, which implies that it will be also called before "diffusing"
    function of the PDE solvers. ``SecretionBasePy`` sets extra flag which
    ensures that steppable which inherits from ``SecretionBasePy`` is called
    before MCS (and before all "regular" Python steppables).

There is no magic to ``SecretionBasePy`` - if you still want to use
``SteppableBasePy`` as a base class for secretion do so, but remember that you need to set flag:

.. code-block:: python

    self.runBeforeMCS=1

to ensure that your new steppable will run before each MCS. See example
below for alternative implementation of ``SecretionSteppable`` using
``SteppableBasePy`` as a base class:

.. code-block:: python

    class SecretionSteppable(SteppableBasePy):
        def __init__(self,_simulator,_frequency=1):
            SteppableBasePy.__init__(self,_simulator, _frequency)
            self.runBeforeMCS=1
        def step(self,mcs):
            attrSecretor=self.getFieldSecretor("ATTR")
            for cell in self.cellList:
                if cell.type==3:
                    attrSecretor.secreteInsideCell(cell,300)
                    attrSecretor.secreteInsideCellAtBoundary(cell,300)
                    attrSecretor.secreteOutsideCellAtBoundary(cell,500)
                    attrSecretor.secreteOutsideCellAtBoundaryOnContactwith(cell,500,[2,3])
                    attrSecretor.secreteInsideCellAtCOM(cell,300)
                    attrSecretor.uptakeInsideCellAtCOM(cell,300,0.2)
                elif cell.type==2:
                    attrSecretor.secreteInsideCellConstantConcentration(cell,300)

The secretion of individual cells is handled through ``FieldSecretor``
objects. ``FieldSecretor`` concept is quite convenient because the amount
of Python coding is quite small. To secrete chemical (this is now done
for individual cell) we first create field secretor object:

.. code-block:: python

    attrSecretor = self.getFieldSecretor("ATTR")

which allows us to secrete into field called ``ATTR``.

Then we pick a cell and using field secretor we simulate secretion of
chemical ``ATTR`` by a cell:

.. code-block:: python

    attrSecretor.secreteInsideCell(cell,300)

Currently we support 7 secretion modes for individual cells:

1. ``secreteInsideCell`` – this is equivalent to secretion in every pixel
   belonging to a cell

2. ``secreteInsideCellConstantConcentration`` – this is equivalent to
   secretion in every pixel belonging to a cell and setting
   concentration to fixed, constant level

3. ``secreteInsideCellAtBoundary`` – secretion takes place in the pixels
   belonging to the cell boundary

4. ``secreteInsideCellAtBoundaryOnContactWith`` - secretion takes place in
   the pixels belonging to the cell boundary that touches any of the
   cells listed as the last argument of the function call

5. ``secreteOutsideCellAtBoundary`` – secretion takes place in pixels which
   are outside the cell but in contact with cell boundary pixels

6. ``secreteOutsideCellAtBoundaryOnContactWith`` - secretion takes place in
   pixels which are outside the cell but in contact with cell boundary
   pixels and in contact with cells listed the last argument of the
   function call

7. ``secreteInsideCellAtCOM`` – secretion at the center of mass of the cell

and 6 uptake modes:

1. ``uptakeInsideCell`` – this is equivalent to uptake in every pixel
   belonging to a cell

2. ``uptakeInsideCellAtBoundary`` – uptake takes place in the pixels
   belonging to the cell boundary

3. ``uptakeInsideCellAtBoundaryOnContactWith`` - uptake takes place in the
   pixels belonging to the cell boundary that touches any of the cells
   listed as the last argument of the function call

4. ``uptakeOutsideCellAtBoundary`` – uptake takes place in pixels which are
   outside the cell but in contact with cell boundary pixels

5. ``uptakeOutsideCellAtBoundaryOnContactWith`` - uptake takes place in
   pixels which are outside the cell but in contact with cell boundary
   pixels and in contact with cells listed the last argument of the
   function call

6. ``uptakeInsideCellAtCOM`` – uptake at the center of mass of the cell

Secretion functions use the following syntax:

.. code-block:: python

    secrete*(cell,amount,list_of_cell_types)

.. note::

    The ``list_of_cell_types`` is used only for function which
    implement such functionality *i.e.* ``secreteInsideCellAtBoundaryOnContactWith`` and
    ``secreteOutsideCellAtBoundaryOnContactWith``

Uptake functions use the following syntax:

.. code-block:: python

    uptake*(cell,max_amount,relative_uptake,list_of_cell_types)

.. note::

    The ``list_of_cell_types`` is used only for function which
    implement such functionality *i.e.* ``uptakeInsideCellAtBoundaryOnContactWith`` and
    ``uptakeOutsideCellAtBoundaryOnContactWith``

.. note::

    **Important:** The uptake works as follows: when available concentration
    is greater than ``max_amount``, then ``max_amount`` is subtracted from
    ``current_concentration``, otherwise we subtract
    ``relative_uptake*current_concentration``.

As you may infer from above, the modes 1-5 require tracking of pixels
belonging to cell and pixels belonging to cell boundary. If you are not
using those secretion modes you may disable pixel tracking by including:

.. code-block:: xml

    <DisablePixelTracker/>

or

.. code-block:: xml

    <DisableBoundaryPixelTracker/>

as shown in the example below:

.. code-block:: xml

    <Plugin Name="Secretion">

        <DisablePixelTracker/>
        <DisableBoundaryPixelTracker/>

        <Field Name="ATTR" ExtraTimesPerMC=”2”>
            <Secretion Type="Bacterium">200</Secretion>
            <SecretionOnContact Type="Medium" SecreteOnContactWith="B">300</SecretionOnContact>
            <ConstantConcentration Type="Bacterium">500</ConstantConcentration>
        </Field>
    </Plugin>

.. note::

    Make sure that fields into which you will be secreting
    chemicals exist. They are usually fields defined in PDE solvers. When
    using secretion plugin you do not need to specify ``SecretionData`` section
    for the PDE solvers.

When implementing e.g. secretion inside cell when the cell is in contact
with other cell we use neighbor tracker and a short script in the spirit
of the below snippet:

.. code-block:: python

    for cell in self.cellList:
        attrSecretor = self.getFieldSecretor("ATTR")
        for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
            if neighbor.type in [self.WALL]:
                attrSecretor.secreteInsideCell(cell, 300)


Secretion Plugin (legacy version)
---------------------------------

.. warning::

    While we still support ``Secretion`` plugin as described
    in this section we observed performance degradation when when declaring
    ``<Field>`` elements inside the plugin. To resolve this issue we encourage
    users to implement secretion "by cell type" in the PDE solver and keep
    using secretion plugin to implement secretion on a per-cell basis using
    Python scripting.

.. note::

    In version 3.6.2 ``Secretion`` plugin should not be used with
    ``DiffusionSolverFE`` or any of the GPU-based solvers.

In earlier version os of CC3D secretion was part of PDE solvers. We
still support this mode of model description however, starting in 3.5.0
we developed separate plugin which handles secretion only. Via secretion
plugin we can simulate cellular secretion of various chemicals. The
secretion plugin allows users to specify various secretion modes in the
CC3DML file – CC3DML syntax is practically identical to the
SecretionData syntax of PDE solvers. In addition to this Secretion
plugin allows users to manipulate secretion properties of individual
cells from Python level. To account for possibility of PDE solver being
called multiple times during each MCS, the ``Secretion`` plugin can be
called multiple times in each MCS as well. We leave it up to user the
rescaling of secretion constants when using multiple secretion calls in
each MCS.

.. note::

    Secretion for individual cells invoked via Python
    will be called only once per MCS.

Typical CC3DML syntax for Secretion plugin is presented below:

.. code-block:: xml

    <Plugin Name="Secretion">
        <Field Name="ATTR" ExtraTimesPerMC=”2”>
            <Secretion Type="Bacterium">200</Secretion>
            <SecretionOnContact Type="Medium" SecreteOnContactWith="B">300</SecretionOnContact>
            <ConstantConcentration Type="Bacterium">500</ConstantConcentration>
        </Field>
    </Plugin>



By default ``ExtraTimesPerMC`` is set to ``0`` - meaning no extra calls to
``Secretion`` plugin per MCS.

Typical use of secretion from Python is demonstrated best in the example
below:

.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self, _simulator, _frequency=1):
            SecretionBasePy.__init__(self, _simulator, _frequency)

        def step(self, mcs):
            attrSecretor = self.getFieldSecretor("ATTR")
            for cell in self.cellList:
                if cell.type == 3:
                    attrSecretor.secreteInsideCell(cell, 300)
                    attrSecretor.secreteInsideCellAtBoundary(cell, 300)
                    attrSecretor.secreteOutsideCellAtBoundary(cell, 500)
                    attrSecretor.secreteInsideCellAtCOM(cell, 300)




