How to Check if Two Cells are Unique
=========================================================================

In the above examples we were printing cell attributes such as cell
type, cell id etc. Sometimes in the simulations you will have two cells
and you may want to test if they are different. The most straightforward
Python construct would look as follows:

.. code-block:: python

    cell1 = self.cellField.get(pt)
    cell2 = self.cellField.get(pt)
    if cell1 != cell2:
        # do something
        ...


Because ``cell1`` and ``cell2`` point to cell at pt i.e. the same cell then
``cell1 != cell2`` should return false. Alas, written as above the condition
is evaluated to true. The reason for this is that what is returned by
``cellField`` is a Python object that wraps a C++ pointer to a cell.
Nevertheless two Python objects cell1 and cell2 are different objects
because they are created by different calls to ``self.cellField.get()``
function. Thus, although logically they point to the same cell, you
cannot use ``!=`` operator to check if they are different or not.

The solution is to use the following function

.. code-block:: python

    self.are_cells_different(cell1,cell2)

or write your own Python function that would do the same:

.. code-block:: python

    def are_cells_different(self, cell1, cell2):
        if (cell1 and cell2 and cell1.this != cell2.this) or\
           (not cell1 and cell2) or (cell1 and not cell2):
            return 1
        else:
            return 0
