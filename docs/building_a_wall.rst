Building a wall (it is going to be terrific. Believe me)
========================================================

One of the side effects of the Cellular Potts Model occurring when
lattice is filled with many cells is that some of them will stick to
lattice boundaries. This happens usually when your contact energies are
positive numbers. When a cell touches lattice boundaries the interface
between lattice boundary and cell contributes ``0`` to the contact energy.
Thus, when all contact energies are positive touching cell boundary is
energetically favorable and as a result cell will try to lay itself
along lattice boundary. To prevent this type of behavior we can create a
wall of froze cells around the lattice and ensure that contact energies
between cells and the wall are very high. To build wall we first need to
declare ``Wall`` cell type in the CC3DML e.g.

.. code-block:: xml

   <Plugin Name="CellType">
      <CellType TypeId="0" TypeName="Medium"/>
      <CellType TypeId="1" TypeName="A"/>
      <CellType TypeId="2" TypeName="B"/>
      <CellType TypeId="3" TypeName="Wall" Freeze=""/>
   </Plugin>


Notice that ``Wall`` type is declared as ``Frozen``. Frozen cells do not
participate in pixel copies but they are taken int account when
calculating contact energies.

Next, in the start function we build a wall of frozen cells of type ``Wall``
as follows:

.. code-block:: python

    def start(self):
        self.build_wall(self.WALL)

If you go to ``CC3D Python->Simulation`` menu in Twedit++ you will find
shortcut that will paste appropriate code snippet to build wall.
