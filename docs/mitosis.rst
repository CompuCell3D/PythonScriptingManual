Mitosis
=======

In developmental simulations we often need to simulate cells which grow
and divide. In earlier versions of CompuCell3D we had to write quite
complicated plugin to do that which was quite cumbersome and
unintuitive. The only advantage of the plugin was that exactly after the
pixel copy which had triggered mitosis condition CompuCell3D called cell
division function immediately. This guaranteed that any cell which was
supposed divide at any instance in the simulation, actually did.
However, because state of the simulation is normally observed after
completion of full a Monte Carlo Step, and not in the middle of MCS it
makes actually more sense to implement Mitosis as a steppable. Let us
examine the simplest simulation which involves mitosis. We start with a
single cell and grow it. When cell reaches critical (doubling) volume it
undergoes Mitosis. We check if the cell has reached doubling volume at
the end of each MCS. The folder containing this simulation is
``CompuCellPythonTutorial/steppableBasedMitosis``

Let’s see how we implement mitosis steppable:

.. code-block:: python

    from cc3d.core.PySteppables import *


    class MitosisSteppable(MitosisSteppableBase):
        def __init__(self, frequency=1):
            MitosisSteppableBase.__init__(self, frequency)

            # 0 - parent child position will be randomized between mitosis event
            # negative integer - parent appears on the 'left' of the child
            # positive integer - parent appears on the 'right' of the child
            self.set_parent_child_position_flag(-1)

        def step(self, mcs):

            cells_to_divide = []
            for cell in self.cell_list:
                if cell.volume > 50:
                    cells_to_divide.append(cell)

            for cell in cells_to_divide:
                # to change mitosis mode leave one of the below lines uncommented
                self.divide_cell_random_orientation(cell)
                # Other valid options
                # self.divide_cell_orientation_vector_based(cell,1,1,0)
                # self.divide_cell_along_major_axis(cell)
                # self.divide_cell_along_minor_axis(cell)

        def update_attributes(self):

            # reducing parent target volume BEFORE cloning
            self.parent_cell.targetVolume /= 2.0

            self.clone_parent_2_child()

            # implementing
            if self.parent_cell.type == self.CONDENSING:
                self.child_cell.type = self.NONCONDENSING
            else:
                self.child_cell.type = self.CONDENSING


The ``step`` function is quite simple – we iterate over all cells in the
simulation and check if the volume of the cell is greater than 50. If it
is we append this cell to the list of cells that will undergo mitosis.
The actual mitosis happens in the second loop of the step function.

We have a choice there to divide cells along randomly oriented plane
(line in 2D), along major, minor or user specified axis. When using user
specified axis you specify vector which is perpendicular to the plane
(axis in 2D) along which you want to divide the cell. This vector does
not have to be normalized but it has to have length different than 0.The
updateAttributes function is called automatically each time you call any
of the functions which divide cells.

.. note::

    The name of the function where we update attributes after mitosis has to be exactly ``update_attributes``. If it is called differently CC3D will not call it automatically. We can obviously call such function by hand, immediately we do the mitosis but this is not very elegant solution.

The ``update_attributes`` of the function is actually the heart of the
mitosis module and you implement parameter adjustments for parent and
child cells inside this function. It is, in general, a good practice to
make sure that you update attributes of both parent and child
cells.Notice that we reset target volume of parent to 25:

.. code-block:: python

    self.parent_cell.targetVolume = 25.0

Had we forgotten to do that parent cell would keep high target volume
from before the mitosis and its actual volume would be, roughly 25
pixels. As a result, after the mitosis, the parent cell would "explode"
to get its volume close to the target target volume. As a matter of fact
if we keep increasing ``targetVolume`` without resetting, the target volume
of parent cell would be higher for each consecutive mitosis event.
Therefore you should always make sure that attributes of parent and
child cells are adjusted properly in the updateAttribute function.

The next call in the ``update_attributes`` function is
``self.clone_parent_2_child()``. This function is a convenience function that
copies all parent cell’s attributes to child cell. That includes python
dictionary attached to a cell. It is completely up to you to call this
function or do manula copy of select attributes from parent to child
cell.

If you would like to use automatic copy of parent attributes but skip
certain dictionary elements (i.e. elements of the ``cell.dict``) you would
use the following call:

.. code-block:: python

    self.clone_attributes(source_cell=self.parent_cell,
                         target_cell=self.child_cell,
                         no_clone_key_dict_list=["ATTRIB_1", "ATTRIB_2"])


where the dictionary elements ``ATTRIB_1`` and ``ATTRIB_2``

.. code-block:: python

    no_clone_key_dict_list=["ATTRIB_1", "ATTRIB_2"]

are not copied. Remember that you can always ignore those convenience
functions and assign parent and child cell attributes manually if this
gives your code the behavior you want or makes code run faster.

For example the implementation of the ``update_attribute`` function where we
manually set ``parent`` and ``child`` properties could look like that:

.. code-block:: python

    def updateAttributes(self):
        parent_cell = self.mitosisSteppable.parentCell
        child_cell = self.mitosisSteppable.childCell

        child_cell.targetVolume = parentCell.targetVolume
        child_cell.lambdaVolume = parentCell.lambdaVolume
        if parent_cell.type == self.CONDENSING:
            child_cell.type = self.NONCONDENSING
        else:
            child_cell.type = self.CONDENSING

.. note::
    It is important to divide cells outside the loop where we iterate over entire cell inventory. If we keep dividing cells in this loop we are adding elements to the list over which we iterate over and this might have unwanted side effects. The solution is to use use list of cells to divide as we did in the example.

If you study the full example you will notice second steppable that we
use to tom implement cell growth. Here is this steppable:

.. code-block:: python

    class VolumeParamSteppable(SteppablePy):
        def __init__(self, frequency=1):
            SteppablePy.__init__(self, frequency)
            self.cellList = CellList(self.inventory)

        def start(self):
            for cell in self.cellList:
                cell.targetVolume = 25
                cell.lambdaVolume = 2.0

        def step(self, mcs):
            for cell in self.cell_list:
                cell.targetVolume += 1

Again, this is quite simple module where in start function we assign
``targetVolume`` and ``lambdaVolume`` to every cell. In the step function we
iterate over all cells in the simulation and increase target volume by 1
unit. As you may suspect to get it to work we have to make sure that we
use Volume without any parameters in the CC3DML plugin instead of ``Volume``
plugin with parameters specified in the CC3DML.

At this point you have enough tools in your arsenal to start building
complex simulations using CC3D. For example, combining steppable
developed so far you can write a steppable where cell growth is
dependent on the value of e.g. FGF concentration at the centroid of the
cell. To get x coordinate of a centroid of a cell use the following
syntax:
.. code-block:: python

    cell.xCOM

or in earlier versions of CC3D

.. code-block:: python

    cell.xCM/float(cell.volume)

Analogous code applies to remaining components of the centroid.
Additionally , make sure you include CenterOfMass plugin in the XML or
the above calls will return 0’s.

Python helper for mitosis is available from Twedit++ ``CC3D Python->Mitosis``.

Directionality of mitosis - a source of possible simulation bias
-----------------------------------------------------------------

When mitosis module divides cells (and, for simplicity, let’s assume
that division happens along vertical line) then the parent cell will
always remain on the same side of the line i.e. if you run have a “stem”
cell that keeps dividing all of it’s offsprings will be created on the
same side of the dividing line. What you may observe then that if you
reassign cell type of a child cell after mitosis than in certain
simulations cell will appear to be biased to move in one direction of
the lattice. To avoid this bias you need to set call
``self.set_parent_child_position_flag`` function from ``Base`` class of the ``Mitosis``
steppable. When you call this function with argument 0 then relative
position of parent and child cell after mitosis will be randomized (this
is default behavior). When the argument is negative integer the child
cell will always appear on the right of the parent cell and when the
argument is positive integer the child cell will appear always on the
left hand side of the parent cell.
