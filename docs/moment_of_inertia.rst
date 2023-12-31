MomentOfInertia Plugin
----------------------

Related: `Calculating Inertia Tensor in CC3D <inertia_tensor.html>`_ and `Calculating the Shape Constraint of a Cell – the Elongation Term <calculating_elongation_term.html>`_

The ``MomentOfInertia`` plugin keeps an up-to-date tensor of inertia for every cell. Internally, it uses
the parallel axis theorem to calculate the most up-to-date tensor of inertia. Although the plugin can be added directly with ``<Plugin Name="MomentOfInertia"/>``, 
it is most commonly called indirectly by other plugins like `LengthConstraint <length_constraint.html>`_.

``MomentOfInertia`` plugin gives users access (via Python scripting) to
current lengths of each cell’s semiaxes. Examples in *Demos/PluginDemos/MomentOfInertia*
demonstrate how to get lengths of semiaxes. For example, to get semiaxes lengths for
a given ``cell``, in Python we would type:

.. code-block:: python

   axes = self.momentOfInertiaPlugin.getSemiaxes(cell)

``axes`` is a 3-component vector with 0\ :sup:`th` element being length of
minor axis, 1\ :sup:`st` element being the length of the median axis (which is set to 0 in
2D) and 2\ :sup:`nd` element indicating the length of major semiaxis.

.. note::

   **Important:** Since calculating lengths of semiaxes involves many
   floating point operations, it may happen (usually on hexagonal
   lattice) that for cells composed of 1, 2, or 3 pixels, one moment the
   square of one of the semiaxes may end up being slightly negative leading
   to ``NaN`` (not a number) length. This is due to round-off error and whenever
   CC3D detects a very small absolute value of the square of the length of
   any of the semiaxes (10\ :sup:`-6`), it sets the length of the semiaxis to ``0.0`` regardless of 
   whether the squared value is positive or negative. However, it is a good
   practice to test whether the length of semiaxis is sane by adding a simple
   ``if`` statement as shown below (here we show how to test for a ``NaN``):

   .. code-block:: python

      if length != length:
          print("length is NaN")
      else:
          print("length is a proper floating point number")
