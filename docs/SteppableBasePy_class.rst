What is a Steppable? (SteppableBasePy class)
===================================================

``SteppableBasePy`` has built-in **functions that are called automatically** during the simulation.
The most important functions are ``start`` and ``step``.

Functions
****************************

**def __init__(self, frequency=1):** This code runs as the simulation is set up, and, in most cases, you will not need to edit it. 

**def start(self):** This is called after cells are created but before the simulation starts, so use it to assign custom cell properties or create `plots <example_plots_histograms.html>`_. 

**def step(self, mcs):** Almost everything will happen here. For example, you might grow, divide, or kill your cells here. 

**def on_stop(self):** This runs when you click the stop button.

**def finish(self):** This function is called at the end of the simulation, but it is used very infrequently. 
Be careful: it will only run if the simulation reaches the maximum number of steps as specified by the XML attribute ``<Steps>``.

**********************************************


A very common line in a Python steppable will read:

.. code-block:: python

        for cell in self.cell_list:

``cell_list`` is a variable of the ``SteppableBasePy`` class, which 
means that every steppable you create will automatically store
every cell it creates in that list. 

All steppables in CompuCell3D are extensions of SteppableBasePy, so they,
too, can use ``cell_list``. 

**If you're new to programming:** The word ``self`` refers to the class we're inside, which would the steppable.
Please see chapters on classes and inheritance from any Python manual if this looks unfamiliar. 
Also, if you want a full list of the cell attributes, see `Appendix B <appendix_b.rst>`_.

**If you're a programmer:** Under the hood, the ``self.cell_list`` is a handle, or a “pointer”, to the C++ object that stores all cells in the simulation. 
The content of cell inventory and cell ordering of cells there is fully
managed by C++ code. 
You can easily see what member variables the C++
cell object has by calling ``dir(cell)`` with one of the cells from the ``self.cell_list`` or by checking out `Appendix B <appendix_b.rst>`_.

.. note::

   Old syntax like ``self.cellList`` is still supported.
