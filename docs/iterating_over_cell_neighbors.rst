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

    def step(self, mcs):
        for cell in self.cellList:
            print "*********NEIGHBORS OF CELL WITH ID ", cell.id,
            for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                if neighbor:
                    print "neighbor.id", neighbor.id, " commonSurfaceArea=", commonSurfaceArea
                else:
                    print "Medium commonSurfaceArea=", commonSurfaceArea

In the outer for loop we iterate over all cells. During each iteration
this loop picks a single cell. For each such cell we construct the inner
loop where we access a list of cell neighbors:

.. code-block:: python
    for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):

Notice that during each iteration loop Python returns two objects:
neighbor and common surface area. neighbor points to a cell object that
has nonzero common surface area with the cell from the outer loop. It
can happen that the neighbor object returned by the inner loop is ``None``.
This means that this particular cell from the outer loop touches Medium.
Take a look at the if-else statement in the example code above. If you
want to paste neighbor iteration code template into your simulation go
to ``CC3D Python->Visit->Cell Neighbors`` in Twedit++.
