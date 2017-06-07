Setting cell membrane fluctuation ona cell-by-cell basis
========================================================

As you probably know the (in)famous ``Temperature`` parameter used in CPM
modeling represents cell membrane fluctuation amplitude. When you
increase ``temperature`` cell boundary gets jagged and if you decrease it
cells may freeze. One problem with global parameter describing membrane
fluctuation is that it applies to all cells. Fortunately in CC3D you may
set membrane fluctuation amplitude on per-cell-type basis or
individually for each cell. The code that does it is very simple:

.. code-block:: python

    cell.fluctAmpl = 50

From now on all calculations involving the cell for which we set
membrane fluctuation amplitude will use this new value. If you want to
undo the change and have global temperature parameter describe membrane
fluctuation amplitude you use the following code:

.. code-block:: python

    cell.fluctAmpl = -1

In fact, this is how CC3D figures out whether to use local or global
membrane fluctuation amplitude. If ``fluctAmpl`` is a negative number CC3D
uses global parameter. If it is greater than or equal to zero local
value takes precedence.

In Twedit++ go to ``CC3D Python->Cell Attributes-> Fluctuation Amplitude``
in case you forget the syntax.
