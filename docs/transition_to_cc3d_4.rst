Transitioning from CC3D 3.x to CC3D 4.x
================================

New CC3D 4.x switches from Python 2.x to python 3.6+. This offered us an opportunity to reorganize code and simplify
the way you describe your simulations. The good news is that the new way of specifying simulations in Python is
much simpler than before. However we did make some changes that will require you to update your existing code
to work with CC3D 4.x. We tried as much as possible to keep old API to limit the number of changes you need to make.

**As a translation method we recommend starting a new CompuCell3D model with twedit++ and copying over parts of your
old 3.x code into this new CompuCell3D 4.x model.**

The list below summarizes key API and coding convention changes. Later we are providing step-by-step guide on how to
port your simulations to CC3D 4.x .

1. Introduction of ``cc3d`` python module. Most of your cc3d imports will begin from ``import cc3d.xxx``

2. Switching from Pascal-case  to more Pythonic snake-case and dropped leading
underscore from function arguments ``self.addSBMLToCell(_cell)`` -> ``self.add_sbml_to_cell(cell)``.

3. Changes how we declare ``Steppable`` class

4. Changes in main Python script

Main Python Script
------------------

Old Python script was quite verbose and contained a lot of "boiler-plate" code.  We fixed it and now instead of typing

.. code-block:: python

    import sys
    from os import environ
    from os import getcwd
    import string

    sys.path.append(environ["PYTHON_MODULE_PATH"])

    import CompuCellSetup

    sim,simthread = CompuCellSetup.getCoreSimulationObjects()

    #Create extra player fields here or add attributes

    CompuCellSetup.initializeSimulationObjects(sim,simthread)

    #Add Python steppables here
    steppableRegistry=CompuCellSetup.getSteppableRegistry()

    from bacterium_macrophage_2D_steering_steppables import ChemotaxisSteering
    chemotaxisSteering=ChemotaxisSteering(_simulator=sim,_frequency=100)
    steppableRegistry.registerSteppable(chemotaxisSteering)

    CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)


we write something much simpler

.. code-block:: python

    from cc3d import CompuCellSetup
    from .bacterium_macrophage_2D_steering_steppables import ChemotaxisSteering

    CompuCellSetup.register_steppable(steppable=ChemotaxisSteering(frequency=100))

    CompuCellSetup.run()

We import CompuCellSetup module from ``cc3d`` package as well as the steppable we want to instantiate. After that we
register the steppable by calling

.. code-block:: python

    CompuCellSetup.register_steppable(steppable=ChemotaxisSteering(frequency=100))

and then start the simulation by calling

.. code-block:: python

    CompuCellSetup.run()

This is much simpler than before and main change is that we no longer store references to key CC3D objects ``sim`` - simulator object
and ``simthread`` - object representing Player in the main script. Those objects are now handled ``behind-the-scenes``
by the new code-base . You can still easily access them though.

Steppable Class
---------------

The new ``Steppable`` class is quite similar to the old one but as before we no longer need to pass ``simulator`` in
the constructor of the class. For exampmple.

.. code-block:: python

    from cc3d.core.PySteppables import *

    class ChemotaxisSteering(SteppableBasePy):
        def __init__(self, frequency=100):
            SteppableBasePy.__init__(self, frequency)

The rest of of the steppable structure is very similar as in the CC3D 3.x.

Note that we import steppable class using

.. code-block::

    from cc3d.core.PySteppables import *

As we mentioned before, most of the CC3D-related Python modules are now submodules of the ``cc3d`` python package

Deprecation Warnings for Old API
--------------------------------

Most of the old API still works in the new CC3D. If you notice absence of certain functions please let us know
and we will fix it. In the process of reworking CC3D API we removed deprecated functions or functions that
were eliminated because they were not needed anymore. Old API was preserved but we added depreciation warning. It is
quite likely, therefore, that when you run CC3D Simulation you may see a lot of depreciation warnings. MOsf of them will look as follows

.. code-block:: console

    SBMLSolverLegacy/Simulation/SBMLSolverLegacySteppables.py:47: DeprecationWarning: Call to deprecated method addSBMLToCell. (You should use : add_sbml_to_cell) -- Deprecated since version 4.0.0.

You may ignore those warnings for now but we highly encourage you to replace old API calls with eh new ones. Most
importantly, Twedit++ uses new API so if you need assistance you may always refer to ``CC3D Python`` of Twedit++

Simplified Programmatic Steering of CC3DML Parameters
------------------------------------------------------

Previous version of CC3D allowed to programmatically change values of CC3DML parameters. For example, you could
run simulation and adjust chemotaxis ``lambda`` from a Python script. The code that was required to make those adjustments was , at best, quite confusing and therefore this feature was a source a frustration among users. The new CC3D fixes this issue. The solution comes from the world of JavaScript and HTML. All that is required is tagging of the CC3DML
element using ``id`` attribute and referring to it from Python script. we present a simple example below
and a separate section on programmatic steering can be found in later chapters of this manual

.. code-block:: xml

    <Plugin Name="Chemotaxis">
        <ChemicalField Name="ATTR">
            <ChemotaxisByType id="macro_chem" Type="Macrophage" Lambda="20"/>
        </ChemicalField>
    </Plugin>

Here in the CC3DML code we added ``id="macro_chem"`` tag to element that we want to modify from Python steppable script. One important thing to keep in mind is that the tags for different elements need to be distinct

In python script we modify ``Lambda`` attribute as follows:

.. code-block:: python

    def step(self, mcs):
        if mcs > 100 and not mcs % 100:
            vol_cond_elem = self.get_xml_element('macro_chem')
            vol_cond_elem.Lambda = float(vol_cond_elem.Lambda) - 3

where first statement ``vol_cond_elem = self.get_xml_element('macro_chem')`` fetches a reference to the CC3DML element
and the second modifies ``vol_cond_elem.Lambda = float(vol_cond_elem.Lambda) - 3`` assigns new value of ``Lambda``

As a reminder we present equivalent code in the old version of CC3D

.. code-block:: python

    def step(self,mcs):
        if mcs>100 and not mcs%100:

            attrVal=float(self.getXMLAttributeValue('Lambda',['Plugin','Name','Chemotaxis'],['ChemicalField','Name','ATTR'],['ChemotaxisByType','Type','Macrophage']))
            self.setXMLAttributeValue('Lambda',attrVal-3,['Plugin','Name','Chemotaxis'],['ChemicalField','Name','ATTR'],['ChemotaxisByType','Type','Macrophage'])
            self.updateXML()

As you can see the new code is easy to inderstand while the old one is quite a mouthful... For this reason
we completely removed the old way of programatic CC3DML steering from the new CC3D.

Accessing Fields
----------------

Staring with CC3D 4.0.0 all fields declared in the simulation can accessed using quite natural syntax:

.. code-block:: python

    self.field.FIELD_NAME

where ``FIELD_NAME`` is replaced with actual field name:

For example to access field called ``fgf8`` you type:

.. code-block:: python

    self.field.fgf_8


Like in previous releases if you are dealing with scalar fields (or a cell field) you may use slicing operators
familiar from ``numpy`` package. For example to assign a patch of concentration of you would type:

.. code-block:: python

    self.field.fgf_8[10:20, 20:30, 0] = 12.3

SBML Solver
-----------

We also changed the way you use SBML solver. While the old syntax still works we feel that the new way of interacting
with SBMLSolve submodule is more natural. Take a look at the example

.. code-block:: python

    model_file = 'Simulation/test_1.xml'

    self.add_free_floating_sbml(model_file=model_file, model_name='Medium_dp2')

    Medium_dp2 = self.sbml.Medium_dp2
    Medium_dp2['S1'] = 10
    Medium_dp2['S2'] = 0.5


Similarly, as in the case of regular fields, we access free floating sbml models using the followng syntax

.. code-block:: python

    self.sbml.Medium_dp2

where ``Medium_dp2`` is a label that we assigned to particular free-floating SBML model (i.e. the one not associated with a particular CC3D cell).

To add and access SBML model to a particular cell we use the following syntax:

.. code-block:: python

    model_file = 'Simulation/test_1.xml'

    cell_20 = self.fetch_cell_by_id(20)

    self.add_sbml_to_cell(model_file=model_file, model_name='dp', cell=cell_20)

    cell_20.sbml.dp['S1'] = 1.3

In the code snippet above we first access a cell with ``id=20`` using ``self.fetch_cell_by_id`` function - we assume that cel with ``id=20 exists``. Next we add SBML model to a cell with ``id=20`` and then use

.. code-block:: python

    cell.sbml.SBML_MODEL_NAME['SPECIES_NAME'] = VALUE

to modify concentration in the SBML model

In our example the above template looks as follows:

.. code-block:: python

    cell_20.sbml.dp['S1'] = 1.3

We will cover SBML solver in details in later chapters


This completes transition guide.