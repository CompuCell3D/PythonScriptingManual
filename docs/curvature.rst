Curvature Plugin
----------------

The ``Curvature`` plugin implements energy term for compartmental cells. The mathematics
and mechanics between the plugin have been described in
“A New Mechanism for Collective Migration in *Myxococcus xanthus*\ ”,
J. Starruß, Th. Bley, L. Søgaard-Andersen and A. Deutsch, *Journal of
Statistical Physics*, DOI: **10.1007/s10955-007-9298-9**, (2007). For a
"long" compartmental cell composed of many subcells (think of a snake-like elongated sequence of compartments)
it imposes a constraint on curvature of cells. The syntax is slightly complex:

.. code-block:: xml

   <Plugin Name="Curvature">

      <InternalParameters Type1="Top" Type2="Center">
         <Lambda>100.0</Lambda>
         <ActivationEnergy>-50.0</ActivationEnergy>
      </InternalParameters>

      <InternalParameters Type1="Center" Type2="Center">
         <Lambda>100.0</Lambda>
         <ActivationEnergy>-50.0</ActivationEnergy>
      </InternalParameters>

      <InternalParameters Type1="Bottom" Type2="Center">
         <Lambda>100.0</Lambda>
         <ActivationEnergy>-50.0</ActivationEnergy>
      </InternalParameters>

      <InternalTypeSpecificParameters>
         <Parameters TypeName="Top" MaxNumberOfJunctions="1" NeighborOrder="1"/>
         <Parameters TypeName="Center" MaxNumberOfJunctions="2" NeighborOrder="1"/>
         <Parameters TypeName="Bottom" MaxNumberOfJunctions="1" NeighborOrder="1"/>
      </InternalTypeSpecificParameters>

   </Plugin>


The ``InternalTypeSpecificParameter`` informs ``Curvature`` Plugin how many
neighbors a cell of given type will have. In the case of "snake-shaped" cell
the numbers that make sense are ``1`` and ``2``. The middle segment will have ``2``
connections and ``head`` and ``tail`` segments will have only one connection with neighboring
segments (subcells). The connections are established dynamically. The way
it happens is that during simulation CC3D constantly monitors pixel
copies and during pixel copy between two neighboring cells/subcells it
checks if those cells are already "connected" using curvature
constraint. If they are not, CC3D will check if connection can be made
(e.g. ``Center`` cells can have up to two connections and ``Top`` and ``Bottom``
only one connection). Usually establishing connections takes place at
the beginning of the simulation and often happens within first Monte
Carlo Step (depending on actual initial configuration, of course, but if
segments touch each other connections are established almost
immediately). The ``ActivationEnergy`` parameter is added to overall energy
in order to increase the odds of pixel copy which would lead to new
connection. ``Lambda`` tag/parameter determines "the strength" of curvature
constraint. The higher the ``Lambda`` the more stiffer cells will be *i.e.*
they will tend to align along straight line.
