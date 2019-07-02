Iterating over cell neighbors
=============================

We have already learned how to iterate over cells in the simulation.
Quite often in the multi-cell simulations there is a need to visit
neighbors of a single cell. We define a neighbor as an adjacent cell
which has common surface area with the cell in mind. To enable neighbor
tracking you have to include NeighborTracker plugin in the XML or in
Python code which replaces XML. For details see
``CompuCellPythonTutorial/NeighborTracker`` example. Take a look at the
implementation of the step function where we visit cell neighbors:

.. code-block:: python

    from cc3d.core.PySteppables import *


    class NeighborTrackerPrinterSteppable(SteppableBasePy):
        def __init__(self, frequency=100):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):

            for cell in self.cell_list:

                for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):
                    if neighbor:
                        print("neighbor.id", neighbor.id, " common_surface_area=", common_surface_area)
                    else:
                        print("Medium common_surface_area=", common_surface_area)

In the outer for loop we iterate over all cells. During each iteration
this loop picks a single cell. For each such cell we construct the inner
loop where we access a list of cell neighbors:

.. code-block:: python

    for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):

Notice that during each iteration loop Python returns two objects:
neighbor and common surface area. neighbor points to a cell object that
has nonzero common surface area with the cell from the outer loop. It
can happen that the neighbor object returned by the inner loop is ``None``.
This means that this particular cell from the outer loop touches Medium.
Take a look at the if-else statement in the example code above. If you
want to paste neighbor iteration code template into your simulation go
to ``CC3D Python->Visit->Cell Neighbors`` in Twedit++.

If you are puzzled why loop above has two variables after ``for`` it is because ``self.get_cell_neighbor_data_list(cell)``
object when iterated over will return tuples of two objects. Let's do an experiment:

.. code-block:: python

    for neighbor_tuple in self.get_cell_neighbor_data_list(cell):
        print neighbor_tuple
        if neighbor_tuple[0]:
            print('Cell id = ', neighbor_tuple[0].id)
        else:
            print('Got Medium Cell ')
        print('Common Surface Area = ', neighbor_tuple[1])


The output will be:

.. code-block:: console

    neighbor_tuple= (<CompuCell.CellG; proxy of <Swig Object of type 'std::vector< CompuCell3D::CellG * >::value_type' at 0x0000000007388EA0> >, 5)
    Cell id =  11
    Common Surface Area =  5
    neighbor_tuple= (None, 4)
    Got Medium Cell
    Common Surface Area =  4


Now you can see ``neighbor_tuple`` is indeed an object that has two components. First one ``neighbor_tuple[0]`` points to
cell object, second one ``neighbor_tuple[1]`` is a common surface area.

In general, when Python iterates over a list-like object that returns tuples you have two choices how to write the ``for``
loop. You can either use

.. code-block:: python

    for neighbor_tuple in self.get_cell_neighbor_data_list(cell):
        print(neighbor_tuple[0], neighbor_tuple[1])

and refer to to the elements of the returned tuple using indices or you can be more explicit and ``unpack`` the tuple
directly into two variables and access them by different "names":

.. code-block:: python

    for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):
        print neighbor, common_surface_area


Neighbor Iteration Helpers
--------------------------

In addition to a plain-vanilla iteration over neighbors the ``CellNeighborDataList`` object that you get using
``self.get_cell_neighbor_data_list(cell)`` has few useful tools that summarize properties of cell neighbors.

Common Surface Area With Cells of Given Types
----------------------------

Sometimes we are interested in a common surface area of a given ``cell`` with ALL neighbors that are of specific type.
``CellNeighborDataList`` has a convenience function ``common_surface_area_with_cell_types`` that computes it. Here is an example

.. code-block:: python

    for cell in self.cell_list:
        neighbor_list = self.get_cell_neighbor_data_list(cell)
        common_area_with_types = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[1, 2])
        print 'Common surface of cell.id={} with cells of types [1,2] = {}'.format(cell.id, common_area_with_types)

The example output is:

.. code-block:: console

    Common surface of cell.id=10 with cells of types [1,2] = 24
    Common surface of cell.id=11 with cells of types [1,2] = 22

As you can see ``common_surface_area_with_cell_types`` returns a number that is a total common surface area of a given cell
with other cells of the type that you specify as argument to ``common_surface_area_with_cell_types`` function as shown above


Common Surface Area With Cells of a Given Type - Detailed View
--------------------------------------------------------------

If you want to break the above common surface area by cell types. i.e. you want to know what was the common
surface area with cells of type 1, what was the common surface area with cells of type 2, *etc...*, you want to use
``neighbor_list.common_surface_area_by_type()`` call :

.. code-block:: python

    for cell in self.cellList:
        neighbor_list = self.get_cell_neighbor_data_list(cell)
        common_area_with_types = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[1, 2])
        print 'Common surface of cell.id={} with cells of types [1,2] = {}'.format(cell.id, common_area_with_types)

        common_area_by_type_dict = neighbor_list.common_surface_area_by_type()
        print 'Common surface of cell.id={} with neighbors \ndetails {}'.format(cell.id, common_area_by_type_dict)


The output may look as follows:

.. code-block:: console

    Common surface of cell.id=10 with cells of types [1,2] = 20
    Common surface of cell.id=10 with neighbors
     details defaultdict(<type 'int'>, {1L: 15, 2L: 5})

    Common surface of cell.id=11 with cells of types [1,2] = 24
    Common surface of cell.id=11 with neighbors
     details defaultdict(<type 'int'>, {1L: 15, 2L: 9})

For cell with ``id=10`` we have that the total common surface area with cell types 1 and 2 is 20 and if we "zoom-in"
we can see that cell with ``id=10`` had common surface area of ``15`` with cell of types ``1`` and ``5`` with cells of type ``2``
The two contact areas by type ad up to ``20`` as expected because this particular cell is in contact only with cells of type
``1`` and ``2``.

Similar thinking explains common surface areas for cell 11.

A more interesting thing is to look at cell with ``id==``. In this particular simulation this cell was in contact with ``Medium``
and the output looks as follows:

.. code-block:: bash

    Common surface of cell.id=1 with cells of types [1,2] = 12
    Common surface of cell.id=1 with neighbors
     details defaultdict(<type 'int'>, {0: 10, 1L: 1, 2L: 11})

Now you see that the overlap with cells of type ``0``, ``1``, ``2`` was   ``10``, ``1``, ``11`` and this does not add up
to ``12`` - the total contact area between cell with ``id=1`` and cells of type ``1`` and ``2``.
However if we replaced

.. code-block:: python

    common_area_with_types = neighbor_ist.common_surface_area_with_cell_types(cell_type_list=[1, 2])

with

.. code-block:: python

    common_area_with_types = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[0, 1, 2])

all the surfaced areas for cell with ``id=1`` would add up as they did for cells with ``id=10``


Counting Neighbors of Particular Type
-------------------------------------

If you want to know how many neighbors of a given type a given cell has you can do "manual" iteration of all neighbors
and keep track of how many of them were of a particular type or you can use a convenience function ``neighbor_count_by_type``.
``neighbor_count_by_type`` will return a dicitonary where the key is a type io the neighbor and the value is
how many neighbors of this type are in contact with a given cell

Here is an example:

.. code-block:: python

    for cell in self.cell_list:
        neighbor_list = self.get_cell_neighbor_data_list(cell)
        neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
        print 'Neighbor count for cell.id={} is {}'.format(cell.id, neighbor_count_by_type_dict)


and the output is:

.. code-block:: bash

    Neighbor count for cell.id=1 is defaultdict(<type 'int'>, {0: 1, 1L: 1, 2L: 2})
    Neighbor count for cell.id=2 is defaultdict(<type 'int'>, {0: 1, 1L: 2, 2L: 1})
    ...
    Neighbor count for cell.id=11 is defaultdict(<type 'int'>, {1L: 4, 2L: 2})
    Neighbor count for cell.id=12 is defaultdict(<type 'int'>, {1L: 2, 2L: 3})

Here is an explanation: cell with ``id==2`` had one neighbor of type Medium (key ``0``), two neighbor of type ``1`` (key ``1``),
and one neighbor of type ``2`` (key ``2``)

Cell with ``id=11`` was in contact with six cells - 4 of them were of type ``1`` and two were of type ``2``










