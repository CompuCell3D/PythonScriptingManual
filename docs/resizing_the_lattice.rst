Resizing the lattice
====================

When you have mitosis in your simulation the numbers of cells usualy
grows and cells need more space. Clearly, you need a bigger lattice.
CC3D lets you enlarge, shrink and shift lattice content using one simple
function. There are few caveats that you have to be aware of few issues
before using this functionality:

1. When resizing lattice, the new lattice is created and existing
   lattice is kept *alive* until all the information from old lattice is
   transferred to the new lattice. This might strain memory of your
   computer and even crash CC3D. If you have enough RAM you should be
   fine

2. Shrinking operation may crop portion of the lattice occupied by
   cells. In this case shrinking operation will be aborted.

3. When shifting lattice content, some cells might end up outside
   lattice boundaries. In this case operation will fail.

4. When you are using a wall of frozen cells you have to first destroy
   the wall, do resize/shifting operation and rebuild a wall again.

The example in ``CompuCellPythonTutorial/BuildWall3D`` demonstrates how to
deal with lattice resize in the presence of wall:

.. code-block:: python

    from cc3d.core.PySteppables import *

    class BuildWall3DSteppable(SteppableBasePy):

        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def start(self):
            self.build_wall(self.WALL)

        def step(self, mcs):
            print('MCS=', mcs)
            if mcs == 4:
                self.destroy_wall()
                self.resize_and_shift_lattice(new_size=(80, 80, 80), shift_vec=(10, 10, 10))
            if mcs == 6:
                self.build_wall(self.WALL)

In the step function, during ``MCS = 4`` we first destroy the wall (we have
built it in the start function), resize the lattice to dimension
``x, y, z = 80, 80, 80`` and shift content of the old lattice (but without the
wall , because we have just destroyed it) by a vector ``x, y, z = 10, 10, 10``.
Finally we rebuild the wall around bigger lattice.

Twedit++ offers help in case you forget the syntax – go to
``CC3D Python->Simulation`` menu and choose appropriate submenu option.

The ability to dynamically resize lattice can play an important role in
improving performance of your simulation. If you expect that number of
cells will grow significantly during the simulation you may start with
small lattice and as the number of cells increases you keep increasing
lattice size in a way that "comfortably" accommodates all cells. This
significantly shortens simulation run times compared to the simulation
where you start with big lattice. When you work with a big lattice but
have few cell,s CC3D will spend a lot of time probing areas occupied by
Medium and this wastes machine cycles.

Along with cell field CC3D will resize all PDE fields. When lattice
grows all new pixels of the PDE field are initialized with ``0.0``.
