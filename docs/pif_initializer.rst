PIF Initializer
---------------

To initialize the configuration of the simulation lattice we can write
custom **lattice initialization file**. Our experience suggests that
you will probably have to write your own initialization files rather
than relying on built-in initializers. The reason is simple: the
built-in initializers implement very simple cell layouts, and if you
want to study more complicated cell arrangements, the built-in
initializers will not be very helpful. Therefore, we encourage you to
learn how to prepare lattice initialization files. We have developed
``CellDraw`` tool which is a part of CC3D suite and it allows users to draw
initial cell layout in a very intuitive way. We encourage you to read
“Introduction to CellDraw” to familiarize yourself with this tool.

To import custom cell layouts, CompuCell3D uses very simple **Potts
Initial File** ``PIF`` file format. It tells CompuCell3D how to lay out
assign the simulation lattice pixels to cells.

The PIF consists of multiple lines of the following format:

.. code-block:: xml

    cell# celltype x1 x2 y1 y2 z1 z2

Where ``cell#`` is the unique integer index of a cell, ``celltype`` is a string
representing the cell's initial type, and ``x1`` and ``x2`` specify a *range* of
x-coordinates contained in the cell (similarly ``y1`` and ``y2`` specify a range
of y-coordinates and ``z1`` and ``z2`` specify a range of z-coordinates). Thus
each line assigns a rectangular volume to a cell. If a cell is not
perfectly rectangular, multiple lines can be used to build up the cell
out of rectangular sub-volumes (just by reusing the ``cell#`` and ``celltype``).

A PIF can be provided to CompuCell3D by including the steppable object
**PIFInitializer**

Let's look at a PIF example for foams:

.. code-block:: xml

    0 Medium 0 101 0 101 0 0
    1 Foam 13 25 0 5 0 0
    2 Foam 25 39 0 5 0 0
    3 Foam 39 46 0 5 0 0
    4 Foam 46 57 0 5 0 0
    5 Foam 57 65 0 5 0 0
    6 Foam 65 76 0 5 0 0
    7 Foam 76 89 0 5 0 0


These lines define a background of ``Medium`` which fills the whole lattice
and is then overwritten by seven rectangular cells of type ``Foam`` numbered
``1`` through ``7`` . Notice that these cells lie in the ``xy`` plane (``z1=0`` ``z2=0``
implies that cells have thickness =1) so this example is a
two-dimensional initialization.

You can write the PIF file manually, but using a script or program that
will write PIF file for you in the language of your choice (Perl,
Python, Matlab, Mathematica, C, C++, Java or any other programming
language) will save a great deal of typing.

Notice, that for the compartmental cell model, the format of the PIF file is
different:

.. code-block:: xml

    Include Clusters
    cluster # cell# celltype x1 x2 y1 y2 z1 z2


For example:

.. code-block:: xml

    Include Clusters
    1 1 Side1 23 25 47 56 10 14
    1 2 Center 26 30 50 54 10 14
    1 3 Side2 31 33 47 56 10 14
    1 4 Top 26 30 55 59 10 14
    1 5 Bottom 26 30 45 49 10 14
    2 6 Side1 35 37 47 56 10 14
    2 7 Center 38 42 50 54 10 14
    2 8 Side2 43 45 47 56 10 14
    2 9 Top 38 42 55 59 10 14
    2 10 Bottom 38 42 45 49 10 14

.. tip::

    An easy way to generate PIF file from the current
    simulation snapshot is to use Player ``Tools->Generate`` PIF file from
    current snapshot… menu option. Alternatively, we can use the PIFDumper
    steppable, which will be discussed next.


