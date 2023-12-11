Secretion / SecretionLocalFlex Plugin
--------------------------------------

Related: 
    - `Secretion Reference <reference_field_secretor.html>`_
    - `Field Secretion <field_secretion.html>`_ 
    - `Secretion (legacy version for pre-v3.5.0) <legacy_secretion.html>`_

****************************************

`Download the sample code here <https://drive.google.com/drive/folders/1ZjLrFyHcX7iPV6WisxSRs4iMLN2vxDRI>`_, 
then watch the video from the latest workshop to follow along:

.. image:: https://img.youtube.com/vi/LgROO9LrzwM/maxresdefault.jpg
    :alt: Workshop Tutorial Video
    :target: https://www.youtube.com/watch?v=LgROO9LrzwM&list=PLiEtieOeWbMKTIF2mekBc9cABFPEDwCdj&index=24
    :width: 80%

..
    [Last Updated] November 2023

****************************************

Secretion "by cell type" can and should be handled by the appropriate
PDE solver. To implement secretion from individual cells using Python, we
first add the secretion plugin in CC3DML:

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

    Although the secretion plugin can be used to implement secretion by
    cell type, **we strongly advise against doing so**. Defining
    secretion by cell type in the ``Secretion`` plugin will lead to performance
    degradation on multi-core machines. Please see the section below for more
    information if you are still interested in using secretion by cell type
    inside the ``Secretion`` plugin.

Typical use of secretion from Python is demonstrated best in the example
below:

.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self, _simulator, _frequency=1):
            SecretionBasePy.__init__(self, _simulator, _frequency)

        def step(self, mcs):
            attrSecretor = self.get_field_secretor("ATTR")
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
    ``SecretionBasePy`` class. This ensures that 
    the secretion plugin will be performed before diffusion by
    calling the Python secretion steppable *before* each Monte Carlo
    Step. 

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
            attrSecretor=self.get_field_secretor("ATTR")
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
of Python coding is quite small. To secrete a chemical from a cell, 
we first create a field secretor object:

.. code-block:: python

    attrSecretor = self.get_field_secretor("ATTR")

which allows us to manipulate how much which cells secrete into the ``ATTR` field.

Then, we pick a cell, and using this field secretor, we simulate secretion of
chemical ``ATTR`` by a cell:

.. code-block:: python

    attrSecretor.secreteInsideCell(cell,300)



Secretion functions use the following syntax:

.. code-block:: python

    secrete*(cell, amount)
    #or...
    secrete*(cell, amount, list_of_cell_types)

.. note::

    The ``list_of_cell_types`` is used only for functions which
    implement such functionality *i.e.* ``secreteInsideCellAtBoundaryOnContactWith`` and
    ``secreteOutsideCellAtBoundaryOnContactWith``

Uptake functions use the following syntax:

.. code-block:: python

    uptake*(cell, max_amount, relative_uptake, list_of_cell_types)
    #or...
    uptake*(cell, max_amount, relative_uptake)

.. note::

    The ``list_of_cell_types`` is used only for functions which
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
        attrSecretor = self.get_field_secretor("ATTR")
        for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
            if neighbor.type in [self.WALL]:
                attrSecretor.secreteInsideCell(cell, 300)
