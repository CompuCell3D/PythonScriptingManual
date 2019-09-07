Changing cluster id of a cell.
==============================

Quite often when working with mitosis you may want to reassign cell's
cluster id i.e. to make a given cell belong to a different cluster than
it currently does. You might think that statement like:

.. code-block:: python

    cell.clusterId = 550

is a good way of accomplishing it. This could have worked with CC3D
versions prior to 3.4.2 . However, this is not the case anymore and in
fact this is an easy recipe for hard to find bugs that will crash your
simulation nd display very enigmatic messages. So what is wrong here? First of
all you need to realize that all the cells (strictly speaking pointers
to ``CellG`` objects) in the CompuCell3D are stored in a sorted container
called inventory. The ordering of the cells in the inventory is based on
cluster id and cell id. Thus when a cell is created it is inserted to
inventory and positioned according to cluster id and cell id. When you
iterate inventory cells with lowest cluster id will be listed first.
Within cells of the same cluster id cells with lowest cell id will be
listed first. In any case if the cell is in the inventory and you do
brute force cluster id reassignment the position of the cell in the
inventory will not be changed. Why should it be? However when this cell
is deleted CompuCell3D will first try to remove the cell from inventory
based on cell id and cluster id and it will not find the cell because
you have altered cluster id so it will ignore the request however it
will delete underlying cell object so the net outcome is that you will
end up with an entry in the inventory which has pointer to a cell that
has been deleted. Next time you iterate through inventory and try go
perform any operation on the cell the CC3D will crash because it will
try to perform something with a cell that has been deleted. To avoid
such situations always use the following construct to change clusterId
of the cell:

.. code-block:: python

    reassignIdFlag = self.reassign_cluster_id(cell, 550)

