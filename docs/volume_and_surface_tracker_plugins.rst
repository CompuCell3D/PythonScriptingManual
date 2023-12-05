VolumeTracker and SurfaceTracker plugins
----------------------------------------

Related: `Global Volume and Surface Constraints <global_volume_and_surface_plugins.html>`_

These two plugins monitor the lattice and update the volume and surface of the
cells once a pixel copy occurs. In most cases, users will not call those
plugins directly. They will be called automatically when either Volume
(calls ``VolumeTracker``) or Surface (calls ``SurfaceTracker``) or
``CenterOfMass`` (calls ``VolumeTracker``) plugins are requested. However, one
should be aware that in some situations, for example when doing foam
coarsening, where neither ``Volume`` nor ``Surface`` plugins are called, one may
still want to track changes in surface or volume of cells. In such
situations, we explicitly invoke ``VolumeTracker`` or ``Surface Tracker`` plugin
with the following syntax:

.. code-block:: xml

    <Plugin Name=”VolumeTracker”/>

or

.. code-block:: xml

    <Plugin Name=”SurfaceTracker”/>

This will enable you to access the current volume and surface in Python with ``cell.volume`` and ``cell.surface``.
