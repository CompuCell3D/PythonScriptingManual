BoundaryPixelTracker Plugin
---------------------------

``BoundaryPixelTracker`` plugin keeps a list of boundary pixels for each cell. The
syntax is as follows:

.. code-block:: xml

   <Plugin Name="BoundaryPixelTracker">
      <NeighborOrder>1</NeighborOrder>
   </Plugin>

This plugin is also used by other plugins as a helper module. Examples
use of this plugin is found in *Demos/PluginDemos/BoundaryPixelTracker_xxx*.

GlobalBoundaryPixelTracker Plugin
----------------------------------

``GlobalBoundaryPixelTracker`` plugin tracks boundary pixels of **all**
the cells including ``Medium``. It is used in a ``Boundary Walker`` algorithm
where instead of blindly picking pixel copy candidate we pick it from the set of pixels comprising
boundaries of non frozen cells. In situations when lattice is large and
there are not that many cells it makes sense to use ``BoundaryWalker``
algorithm to limit number of pixel picks that would not lead to actual pixel copy.

.. note::

   ``BoundaryWalkerAlgorithm`` does not really work with OpenMP
   version of CC3D which includes all versions starting with ``3.6.0``.

Take a look at the following example:

.. code-block:: xml

   <Potts>
      <Dimensions x="100" y="100" z="1"/>
      <Anneal>10</Anneal>
      <Steps>10000</Steps>
      <Temperature>5</Temperature>
      <Flip2DimRatio>1</Flip2DimRatio>
      <NeighborOrder>2</NeighborOrder>
      <MetropolisAlgorithm>BoundaryWalker</MetropolisAlgorithm>
      <Boundary_x>Periodic</Boundary_x>
    </Potts>

    <Plugin Name="GlobalBoundaryPixelTracker">
       <NeighborOrder>2</NeighborOrder>
    </Plugin>


Here we are using ``BoundaryWalker`` algorithm (``Potts`` section) and
subsequently we list ``GlobalBoundaryTracker`` plugin where we set neighbor
order to match that in the Potts section. The neighbor order determines
how "thick" the overall boundary of cells will be. The higher this
number the more pixels will belong to the boundary.

PixelTracker Plugin
-------------------

``PixelTracker`` plugin allows storing list of all pixels belonging to a given cell.
The syntax is as follows:

.. code-block:: xml

   <Plugin Name="PixelTracker">
      <TrackMedium/>
   </Plugin>

This plugin is also used by other modules (e.g. ``Mitosis``) as a helper
module. Simple example can be found in *Demos/PluginDemos/PixelTrackerExample*.
Beginning with ``4.1.2``, medium pixels can be optionally tracked using ``TrackMedium``.
This feature is automatically enabled by attaching a Fluctuation Compensator to a
PDE solver. 