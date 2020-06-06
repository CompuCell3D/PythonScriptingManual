Passing information between steppables
======================================

When you work with more than one steppable (and it is a good idea to
work with several steppables each of which has a well defined purpose) you
may sometimes need to access or change member variable of one steppable
inside the code of another steppable. The most straightforward method to implement exchange of
information between steppables is to utilize the python dictionary ``shared_steppable_vars``,
which is a shared dictionary that every steppable can access as an attribute.

Say we have two steppables, where one steppable updates a shared variable ``x_shared``, and the
other steppable prints the current value of ``x_shared``. Let's call our steppables
``UpdaterSteppable`` and ``PrinterSteppable`` for our tasks of updating and printing ``x_shared``,
respectively:

.. code-block:: python

    class UpdaterSteppable(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def start(self):
            self.shared_steppable_vars['x_shared'] = 0

        def step(self, mcs):

            self.shared_steppable_vars['x_shared'] += 1


    class PrinterSteppable(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):

            print('x_shared=', self.shared_steppable_vars['x_shared'])

We see that ``UpdaterSteppable`` initializes a key ``x_shared`` with a value of ``0`` in the
shared dictionary and updates it every step. Meanwhile ``PrinterSteppable`` accesses and prints
the value of the same key in the shared dictionary.

The same can be done with simulation objects. Say we have two steppables, where one steppable
tests whether or not each cell undergoes mitosis, and the other steppable implements mitosis.
For this case, we'll call our steppable that checks for mitosis ``CheckMitosisSteppable``, and
we'll use the mitosis steppable base class to implement mitosis with a steppable called
``MitosisSteppable``. When checking for the occurrence of mitosis, we'll say that all cells
with a volume greater than 75 undergo mitosis:

.. code-block:: python

    class CheckMitosisSteppable(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):

            for cell in self.cell_list:
                if cell.volume > 75:
                    self.shared_steppable_vars['cells_to_divide'].append(cell)


    class MitosisSteppable(MitosisSteppableBase):
        def __init__(self, frequency=1):
            MitosisSteppableBase.__init__(self, frequency)
            self.set_parent_child_position_flag(0)

        def start(self):
            self.shared_steppable_vars['cells_to_divide'] = []

        def step(self, mcs):

            for cell in self.shared_steppable_vars['cells_to_divide']:
                self.divide_cell_random_orientation(cell)

            self.shared_steppable_vars['cells_to_divide'] = []

        def update_attributes(self):

            self.clone_parent_2_child()

We see that ``MitosisSteppable`` initializes the key ``cells_to_divide`` with an empty list in
the shared dictionary. ``CheckMitosisSteppable`` populates that same list every step with
cell objects according to results of our test for mitosis, each of
which ``MitosisSteppable`` then passes to the built-in method ``divide_cell_random_orientation``
for randomly-oriented mitosis. After processing all mitosis results, ``MitosisSteppable``
then returns the shared list to an empty list, so that each positive result of
our check for mitosis corresponds to one division of a mitotic cell (otherwise a cell in
``shared_steppable_vars['cells_to_divide']`` would divide every step!).