Modifying attributes of CellG object
====================================

So far, the only attributes of a cell we have been modifying were those
that we attached during runtime, members of the cell dictionary.
However, CC3D allows users to modify core cell attributes i.e. those
which are visible to the C++ portion of the CC3D code. Those attributes
are members of ``CellG`` object (see ``Potts3D/Cell.h`` in the CC3D source code)
define properties of a CC3D cell. The full list of the attributes is
shown in Appendix B. Here we will show a simple example how to modify
some of those attributes using Python and thus alter the course of the
simulation. As a matter of fact, the way to build “dynamic” simulation
where cellular properties change in response to simulation events is to
write a Python function/class which alters CellG object variables as
simulation runs.

**CAUTION:** CC3D does not allow you to modify certain attributes, e.g.
cell volume, and in case you try you will get warning and simuation will
stop. Given that CC3D is under constant development with many new
features being added continuously, it may happen that CC3D will let you
modify attribute that should be read-only. In such a case you will most
likely get cryptic error and the simulation will crash. Therefore you
should be careful and double-check CC3D documentation to see which
attributes can be modified.

The steppable below shows how to change ``targetVolume`` and ``lambdaVolume`` of
a cell and how to implement cell differentiation (changing cell type):

.. code-block:: python

    class TypeSwitcherAndVolumeParamSteppable(SteppableBasePy):
        def __init__(self, frequency=100):
            SteppableBasePy.__init__(self, frequency)

        def start(self):
            for cell in self.cell_list:
                if cell.type == 1:
                    cell.targetVolume = 25
                    cell.lambdaVolume = 2.0
                elif cell.type == 2:
                    cell.targetVolume = 50
                    cell.lambdaVolume = 2.0

        def step(self, mcs):
            for cell in self.cell_list:
                if cell.type == 1:
                    cell.type = 2
                elif cell.type == 2:
                    cell.type = 1

As you can see in the step function we check if cell is of type 1. If it
is we change it to type 2 and do analogous check/switch for cell of type
2. In the start function we initialize target volume of type 1 cells to
25 and type 2 cells will get target volume 50. The only other thing we
need to remember is to change definition of ``Volume`` plugin in the XML
from:

.. code-block:: xml

    <Plugin Name="Volume">
       <TargetVolume>25</TargetVolume>
       <LambdaVolume>2.0</LambdaVolume>
    </Plugin>

to

.. code-block:: xml

    <Plugin Name="Volume"/>

to tell CC3D that volume constraint energy term will be calculated using
local values (i.e. those stored in CellG object – exactly the ones we
have modified using Python) rather than global settings.

Notice that we have referred to cell types using numbers. This is OK but
as we have mentioned earlier using type aliases leads to much cleaner
code.
