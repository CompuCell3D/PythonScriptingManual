VolumeTracker and SurfaceTracker plugins
----------------------------------------

Related: `Global Volume and Surface Constraints <global_volume_and_surface_plugins.html>`_

These two plugins monitor the lattice and update the volume and surface of the
cells once a pixel copy occurs. In most cases, users will not call those
plugins directly. They will be called automatically when either Volume
(together with ``VolumeTracker``) or Surface or
``CenterOfMass`` (calls ``VolumeTracker``) plugins are requested. However, one
should be aware that in some situations, for example when doing foam
coarsening, where neither ``Volume`` nor ``Surface`` plugins are called, one may
still want to track changes in surface or volume of cells. In such
situations, we explicitly invoke the ``VolumeTracker`` or ``Surface`` plugins
with the following syntax:

.. code-block:: xml

    <Plugin Name="VolumeTracker"/>

As of version 4.6.0, all you have to do to the ``Surface`` plugin
to enable this behavior is add ``NeighborOrder``.

.. code-block:: xml

    <Plugin Name="Surface">
        <TargetSurface>120</TargetSurface>
        <LambdaSurface>0.5</LambdaSurface>
        <NeighborOrder>4</NeighborOrder>
    </Plugin>

This will enable you to access the current volume and surface in Python with ``cell.volume`` and ``cell.surface``.

.. note:: 

    **Legacy Version (Pre 4.6.0)**

    Previously, this arrangement of plugins was required.
    ``SurfaceTracker`` is now deprecated. 
    
    .. code-block:: xml

        <Plugin Name="SurfaceTracker">
            <NeighborOrder>4</NeighborOrder>
        </Plugin>

        <Plugin Name="Surface">
            <TargetSurface>120</TargetSurface>
            <LambdaSurface>0.5</LambdaSurface>
        </Plugin>
