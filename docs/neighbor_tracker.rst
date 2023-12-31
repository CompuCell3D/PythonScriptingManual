NeighborTracker Plugin
----------------------

This plugin, as its name suggests, tracks neighbors of every cell. In
addition, it calculates common contact area between cell and its
neighbors. We consider a neighbor this cell that has at least one common
pixel side with a given cell. This means that cells that touch each
other either "by edge" or by "corner" **are not** considered neighbors. See
the drawing below:

+-----+-----+-----+-----+-----+
| 5   | 5   | 5   | 4   | 4   |
+-----+-----+-----+-----+-----+
| 5   | 5   | 5   | 4   | 4   |
+-----+-----+-----+-----+-----+
| 5   | 5   | 4   | 4   | 4   |
+-----+-----+-----+-----+-----+
| 1   | 1   | 2   | 2   | 2   |
+-----+-----+-----+-----+-----+
| 1   | 1   | 2   | 2   | 2   |
+-----+-----+-----+-----+-----+

**Figure 1**. Cells 5,4,1 are considered neighbors as they have non-zero
common surface area. Same applies to pair of cells 4 ,2 and to 1 and 2.
However, cells 2 and 5 are not neighbors because they touch each other
"by corner". Notice that cell 5 has 8 pixels cell 4 , 7 pixels, cell 1 4
pixels and cell 2 6 pixels.

To include this plugin in your simulation , add the following code to the CC3DML

.. code-block:: xml

    <Plugin Name="NeighborTracker"/>

This plugin is used as a helper module by other plugins and steppables
e.g. ``FocalPointPlasticity`` plugin  uses NeighborTracker plugin.
