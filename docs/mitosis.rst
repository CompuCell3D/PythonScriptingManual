Mitosis
=======

**Related Examples**
    - `General Mitosis Examples <example_mitosis>`_
    - `Contact-Inhibited Cell Growth <example_contact_inhibited_cell_growth.html>`_

**********************************************

In developmental simulations, we often need to simulate cells that grow
and divide. We start with a single cell and grow it. 
When a cell reaches a **critical volume**, it undergoes Mitosis. 
We **check if the cell has reached this volume threshold** at
the end of every Monte Carlo Step (MCS). The folder containing this simulation is
``CompuCellPythonTutorial/steppableBasedMitosis``

.. note::

    *Tip:* Be sure to turn off mitosis for dying cells. `cell_death.rst`_`See how here`.

**How to Implement a Simple Mitosis Steppable**

.. code-block:: python

    from cc3d.core.PySteppables import *


    class MitosisSteppable(MitosisSteppableBase):
        def __init__(self, frequency=1):
            MitosisSteppableBase.__init__(self, frequency)

            # Optional: Customize where to place the new cell.
            # 0 - parent and child positions will be randomized between mitosis events
            # negative integer - parent appears on the 'left' of the child
            # positive integer - parent appears on the 'right' of the child
            self.set_parent_child_position_flag(-1)

        def step(self, mcs):

            cells_to_divide = []
            for cell in self.cell_list:
                if cell.volume > 50: #the critical mass, chosen arbitrarily
                    cells_to_divide.append(cell)

            for cell in cells_to_divide:
                # To change mitosis mode, leave one of the below lines uncommented
                self.divide_cell_random_orientation(cell)
                # Other valid options
                # self.divide_cell_orientation_vector_based(cell,1,1,0)
                # self.divide_cell_along_major_axis(cell)
                # self.divide_cell_along_minor_axis(cell)

        def update_attributes(self):

            # Reduce parent target volume BEFORE cloning
            self.parent_cell.targetVolume /= 2.0

            self.clone_parent_2_child()

            # Make the cell type change every time the cell divides
            if self.parent_cell.type == self.CONDENSING:
                self.child_cell.type = self.NONCONDENSING
            else:
                self.child_cell.type = self.CONDENSING

How does the ``step(…)`` function work?
    1. Check every cell to see if its volume is greater than 50.
    2. All cells with this critical volume are placed into a list, ``cells_to_divide``.
    3. Then, loop over all ``cells_to_divide`` to perform mitosis with a built-in function such as ``divide_cell_random_orientation(cell)``.
    4. ``update_attributes()`` is automatically called before each division. Use this to control the data of the parent and child cells. 
        * Here, ``self.clone_parent_2_child()`` copies over all data for you.

.. note::
    It's important to use two Python loops in ``step(…)`` to avoid iterating
    over a newly-created cell. If we keep dividing cells in this loop we are adding elements to the list over which we iterate over and this might have unwanted side effects. 
    The solution is to use use list of cells to divide as we did in the example.

We have a choice in step 3 to divide cells along a randomly-oriented plane
(line in 2D), along major, minor, or user-specified axis. When using a user
specified axis, you specify a vector which is perpendicular to the plane
(axis in 2D) along which you want to divide the cell. This vector does
not have to be normalized but it has to have length different than 0. The
``update_attributes`` function is called automatically each time you call any
of the functions which divide cells.

.. note::

    The name of the function where we update attributes after mitosis has to be exactly ``update_attributes``. If it is differen, CC3D will not call it automatically.

The ``update_attributes`` of the function is actually the heart of the
mitosis module and you implement parameter adjustments for parent and
child cells inside this function. It is, in general, a good practice to
make sure that you update attributes of both parent and child
cells. Notice that we reset target volume of the parent to 25:

.. code-block:: python

    self.parent_cell.targetVolume = 25.0

Had we forgotten to do that, the parent cell would keep the high target volume
from before the mitosis and its actual volume would be, roughly 25
pixels. As a result, after the mitosis, the parent cell would "explode"
to get its volume close to the target target volume. As a matter of fact,
if we keep increasing ``targetVolume`` without resetting, the target volume
of parent cell would be higher for each consecutive mitosis event.
Therefore, you should always make sure that the attributes of parent and
child cells are adjusted properly in the ``update_attributes`` function.

The next call in the ``update_attributes`` function is
``self.clone_parent_2_child()``. This function is a convenience function that
copies all parent cell’s attributes to the child cell. It is completely up to you to call this
function or do a manual copy of select attributes from parent to child
cell.



Deep-Copy a Cell (recommended)
*********************************
``clone_parent_2_child()``: Copies all attributes of the parent cell to the child cell, including ``cell.dict``.


Shallow-Copy a Cell
***************************
``clone_attributes(source_cell, target_cell, no_clone_key_dict_list)``: Creates a shallow copy of a cell. 
Parent attributes are copied, but dictionary elements, such as ``cell.dict``, are skipped.

**Example:**

.. code-block:: python

    self.clone_attributes(source_cell=self.parent_cell,
                         target_cell=self.child_cell,
                         no_clone_key_dict_list=["ATTRIB_1", "ATTRIB_2"])


The dictionary elements ``ATTRIB_1`` and ``ATTRIB_2``

.. code-block:: python

    no_clone_key_dict_list=["ATTRIB_1", "ATTRIB_2"]

are not copied. Remember that you can always ignore those convenience
functions and assign parent and child cell attributes manually if this
gives your code the behavior you want or makes code run faster.

For example, the implementation of the ``update_attributes`` function where we
manually set ``parent`` and ``child`` properties could look like that:

.. code-block:: python

    def update_attributes(self):

        self.child_cell.targetVolume = self.parent_cell.targetVolume
        self.child_cell.lambdaVolume = self.parent_cell.lambdaVolume
        if self.parent_cell.type == self.CONDENSING:
            self.child_cell.type = self.NONCONDENSING
        else:
            self.child_cell.type = self.CONDENSING



Remember to Grow Your Cells
**********************************

You can use either one of the two XML plugins to grow your cells to the target volume of 50.
Let CC3D define this for you by clicking on **CCDML -> Plugins -> Volume** in Twedit++.

.. code-block:: xml

    <Plugin Name="Volume">
        <VolumeEnergyParameters CellType="Condensing" LambdaVolume="2.0" TargetVolume="50.0"/>
        <VolumeEnergyParameters CellType="NonCondensing" LambdaVolume="2.0" TargetVolume="50.0"/>
    </Plugin>

or 

.. code-block:: xml

    <Plugin Name="Volume">
        <TargetVolume>50</TargetVolume>
        <LambdaVolume>2.0</LambdaVolume>
    </Plugin>

**********************************************

Directionality of mitosis - a source of possible simulation bias
-----------------------------------------------------------------

When the mitosis module divides cells (and, for simplicity, let’s assume
that division happens along a vertical line), then the parent cell will
always remain on the same side of the line. For example, if you run have a “stem”
cell that keeps dividing, all of its offspring will be created on the
same side of the dividing line. What you may observe then is that, if you
reassign the cell type of a child cell after mitosis, then, in certain
simulations, the cell will appear to be biased to move in one direction of
the lattice. 

To avoid this bias, you need to call the 
``self.set_parent_child_position_flag`` function from the ``Base`` class of the ``Mitosis``
steppable. When you call this function with argument 0, then the relative
position of parent and child cells after mitosis will be randomized (this
is the default behavior). When the argument is a negative integer, the child
cell will always appear on the right of the parent cell. Conversely, when the
argument is a positive integer, the child cell will appear always on the
left-hand side of the parent cell.
