CenterOfMass Plugin
-------------------

``CenterOfMass`` plugin monitors changes n the lattice and updates centroids of the
cell:

.. math::
   :nowrap:

   \begin{align*}
      x_{CM}^{centroid} &= \sum_{i}x_{i} \\
      y_{CM}^{centroid} &= \sum_{i}y_{i} \\
      z_{CM}^{centroid} &= \sum_{i}z_{i}
   \end{align*}

where ``i`` denotes pixels belonging to a given cell. To obtain
coordinates of a center of mass of a given cell we divide centroids by
cell volume:

.. math::
   :nowrap:

   \begin{align*}
      x_{CM} &= \frac{x_{CM}^{centroid}}{V}  \\
      y_{CM} &= \frac{y_{CM}^{centroid}}{V}  \\
      z_{CM} &= \frac{z_{CM}^{centroid}}{V}
   \end{align*}

This plugin is aware of boundary conditions and centroids are calculated
properly regardless which boundary conditions are used. The CC3DML
syntax is very simple:

.. code-block:: xml

   <Plugin Name="CenterOfMass"/>

To access center of mass coordinates from Python we use the following
syntax:

.. code-block:: python

   print('x-component of COM is:', cell.xCOM)
   print ('y-component of COM is:', cell.yCOM)
   print ('z-component of COM is:', cell.zCOM)

.. warning::

   Center of mass parameters in Python are read only. Any
   attempt to modify them will likely mess up the simulation.
