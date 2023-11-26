ExternalPotential Plugin
------------------------

``Chemotaxis`` plugin is used to cause directional cell movement in response
to chemical gradient. Another way to achieve directional movement is to
use ``ExternalPotential`` plugin. This plugin is responsible for imposing a
directed pressure (or rather force) on cells. It is used to implement
persistent motion of cells and its applications can be very diverse.

Example usage of this plugin looks as follows:

.. code-block:: xml

     <Plugin Name="ExternalPotential">
        <Lambda x="-0.5" y="0.0" z="0.0"/>
     </Plugin>


``Lambda`` is a vector quantity and determines components of force along
three axes. In this case we apply force along ``x`` pointing in the positive
direction.

.. note::

    Positive component of Lambda vector pushes cell in the
    negative direction and negative component pushes cell in the positive
    direction

We can also apply external potential to specific cell types:

.. code-block:: xml

    <Plugin Name="ExternalPotential">
        <ExternalPotentialParameters CellType="Body1" x="-10" y="0" z="0"/>
        <ExternalPotentialParameters CellType="Body2" x="0" y="0" z="0"/>
        <ExternalPotentialParameters CellType="Body3" x="0" y="0" z="0"/>
    </Plugin>

Where in ``ExternalPotentialParameters`` we specify which cell type is
subject to external potential (``Lambda`` is specified using ``x , y , z``
attributes).

We can also apply external potential to individual cells. In that case,
in the CC3DML section we only need to specify:

.. code-block:: xml

    <Plugin Name="ExternalPotential"/>

and in the Python file we change ``lambdaVecX``, ``lambdaVecY``, ``lambdaVecZ``,
which are properties of cell. For example in Python we could write:

.. code-block:: python

    cell.lambdaVecX = -10

Calculations done by ``ExternalPotential`` Plugin are by default based on
direction of pixel copy (similarly as in chemotaxis plugin). One can,
however, force CC3D to do calculations based on movement of center of
mass of cell. To use algorithm based on center of mass movement we use
the following CC3DML syntax:

.. code-block:: xml

    <Plugin Name="ExternalPotential">

        <Algorithm>CenterOfMassBased</Algorithm>

        …

    </Plugin>

.. note::

    In the pixel-based algorithm the typical value of
    pixel displacement used in calculations is of the order of ``1`` (pixel)
    whereas typical displacement of center of mass of cell due to single
    pixel copy is of the order of 1/cell volume (pixels) – ~ ``0.1`` pixel. This
    implies that to achieve compatible behavior of cells when using center
    of mass algorithm we need to multiply ``lambda``’s by appropriate factor,
    typically of the order of ``10``.
