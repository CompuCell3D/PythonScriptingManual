FocalPointPlasticity Plugin
---------------------------

``FocalPointPlasticity`` puts constraints on the
distance between cells’ center of masses. A key feature of this plugin is that
the list of "focal point plasticity neighbors" can change as the
simulation evolves and user has to specifies the maximum number of "focal point
plasticity neighbors" a given cell can have. Let’s look at relatively
simple CC3DML syntax of ``FocalPointPlasticityPlugin`` (see
*Demos/PluginDemos/FocalPointPlasticity/FocalPointPlasticity* example and we will show more complex
examples later):

.. code-block:: xml

   <Plugin Name="FocalPointPlasticity">
      <Parameters Type1="Condensing" Type2="NonCondensing">
         <Lambda>10.0</Lambda>
         <ActivationEnergy>-50.0</ActivationEnergy>
         <TargetDistance>7</TargetDistance>
         <MaxDistance>20.0</MaxDistance>
         <MaxNumberOfJunctions>2</MaxNumberOfJunctions>
      </Parameters>

      <Parameters Type1="Condensing" Type2="Condensing">
         <Lambda>10.0</Lambda>
         <ActivationEnergy>-50.0</ActivationEnergy>
         <TargetDistance>7</TargetDistance>
         <MaxDistance>20.0</MaxDistance>
         <MaxNumberOfJunctions>2</MaxNumberOfJunctions>
      </Parameters>
      <NeighborOrder>1</NeighborOrder>
   </Plugin>

``Parameters`` section describes properties of links between cells.
``MaxNumberOfJunctions``, ``ActivationEnergy``, ``MaxDistance`` and ``NeighborOrder``
are responsible for establishing connections between cells. CC3D
constantly monitors pixel copies and during pixel copy between two
neighboring cells/subcells it checks if those cells are already
participating in focal point plasticity constraint. If they are not,
CC3D will check if connection can be made (e.g. ``Condensing`` cells can
have up to two connections with ``Condensing`` cells and up to 2 connections
with ``NonCondensing`` cells – see first line of ``Parameters`` section and
``MaxNumberOfJunctions`` tag). The ``NeighborOrder`` parameter determines the
pixel vicinity of the pixel that is about to be overwritten which CC3D
will scan in search of the new link between cells. ``NeighborOrder 1``
(which is default value if you do not specify this parameter) means that
only nearest pixel neighbors will be visited. The ``ActivationEnergy``
parameter is added to overall energy in order to increase the odds of
pixel copy which would lead to new connection.

Once cells are linked the energy calculation is carried out according to the formula:

.. math::
   :nowrap:

   \begin{eqnarray}
      E = \sum_{i,j,cell\ neighbors}\lambda_{ij}\left ( l_{ij}-L_{ij} \right )^2
   \end{eqnarray}

where :math:`l_{ij}` is a distance between center of masses of cells ``i`` and ``j`` and :math:`L_{ij}` is
a target length corresponding to :math:`l_{ij}`.

:math:`\lambda_{ij}` and :math:`L_{ij}` between different cell types are
specified using ``Lambda`` and ``TargetDistance`` tags. The ``MaxDistance``
determines the distance between cells’ center of masses past which the link
between those cells break. When the link breaks, then in order for the
two cells to reconnect they would need to come in contact again.
However it is usually more likely that there will be other
cells in the vicinity of separated cells so it is more likely to
establish new link than restore broken one.

The above example was one of the simplest examples of use of
``FocalPointPlasticity``. A more complicated one involves compartmental
cells. In this case each cell has separate "internal" list of links
between cells belonging to the same cluster and another list between
cells belonging to different clusters. The energy contributions from
both lists are summed up and everything that we have said when
discussing example above applies to compartmental cells. Sample syntax
of the ``FocalPointPlasticity`` plugin which includes compartmental cells is
shown below. We use ``InternalParameters`` tag/section to describe links
between cells of the same cluster (see *Demos/PluginDemos/FocalPointPlasticity/FocalPointPlasticityCompartments*
example):

.. code-block:: xml

   <Plugin Name="FocalPointPlasticity">

       <Parameters Type1="Top" Type2="Top">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions NeighborOrder="1">1</MaxNumberOfJunctions>
       </Parameters>

       <Parameters Type1="Bottom" Type2="Bottom">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions NeighborOrder="1">1</MaxNumberOfJunctions>
       </Parameters>

       <InternalParameters Type1="Top" Type2="Center">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions>1</MaxNumberOfJunctions>
       </InternalParameters>

       <InternalParameters Type1="Bottom" Type2="Center">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions>1</MaxNumberOfJunctions>
       </InternalParameters>

       <NeighborOrder>1</NeighborOrder>

   </Plugin>


We can also specify link constituent law and change it to different form
that "spring relation". To do this we use the following syntax inside
FocalPointPlasticity CC3DML plugin:

.. code-block:: xml

    <LinkConstituentLaw>
        <!--The following variables lare defined by default: Lambda,Length,TargetLength-->

        <Variable Name='LambdaExtra' Value='1.0'/>
        <Formula>LambdaExtra*Lambda*(Length-TargetLength)^2</Formula>

    </LinkConstituentLaw>


By default CC3D defines 3 variables (``Lambda``, ``Length``, ``TargetLength``) which
correspond to :math:`\lambda_{ij}` ,  :math:`l_{ij}` and :math:`L_{ij}` from the formula
above. We can also define extra variables in the CC3DML (e.g.
``LambdaExtra``). The actual link constituent law obeys ``muParser`` syntax
convention. Once link constituent law is defined it is applied to all
focal point plasticity links. The example demonstrating the use of
custom link constituent law can be found in
*Demos/PluginDemos/FocalPointPlasticityCustom*.

Sometimes it is necessary to modify link parameters individually for
every cell pair. In this case we would manipulate ``FocalPointPlasticity``
links using Python scripting. Example
*Demos/PluginDemos/FocalPointPlasticity/FocalPointPlasticityCompartments* demonstrates exactly this
situation. You still need to include CC3DML section as the one shown
above for compartmental cells, because we need to tell CC3D how to link
cells. The only notable difference is that in the CC3DML we have to
include ``<Local/>`` tag to signal that we will set link parameters (``Lambda``,
``TargetDistance``, ``MaxDistance``) individually for each cell pair:

.. code-block:: xml

   <Plugin Name="FocalPointPlasticity">
       <Local/>
       <Parameters Type1="Top" Type2="Top">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions NeighborOrder="1">1</MaxNumberOfJunctions>
       </Parameters>
      ...
   </Plugin>



Python steppable where we manipulate cell-cell focal point plasticity
link properties is shown below:

.. code-block:: python

   class FocalPointPlasticityCompartmentsParams(SteppablePy):
       def __init__(self, _simulator, _frequency=10):
           SteppablePy.__init__(self, _frequency)
           self.simulator = _simulator
           self.focalPointPlasticityPlugin = CompuCell.getFocalPointPlasticityPlugin()
           self.inventory = self.simulator.getPotts().getCellInventory()
           self.cellList = CellList(self.inventory)

       def step(self, mcs):
           for cell in self.cellList:
               for fppd in InternalFocalPointPlasticityDataList(self.focalPointPlasticityPlugin, cell):
                   self.focalPointPlasticityPlugin.setInternalFocalPointPlasticityParameters(cell, fppd.neighborAddress,
                                                                                             0.0, 0.0, 0.0)

The syntax to change focal point plasticity parameters (or as here
internal parameters) is as follows:

.. code-block:: python

   setFocalPointPlasticityParameters(cell1, cell2, lambda, targetDistance, maxDistance)

.. code-block:: python

   setInternalFocalPointPlasticityParameters(cell1, cell2, lambda, targetDistance, maxDistance)


Similarly, to inspect current values of the focal point plasticity
parameters we would use the following Python construct:

.. code-block:: python

   for cell in self.cellList:
       for fppd in InternalFocalPointPlasticityDataList(self.focalPointPlasticityPlugin, cell):
           print "fppd.neighborId", fppd.neighborAddress.id
           " lambda=", fppd.lambdaDistance


For non-internal parameters we simply use ``FocalPointPlasticityDataList``
instead of ``InternalFocalPointPlasticityDataList`` .

Examples *Demos/PluginDemos/FocalPointPlasticity…* show in relatively simple way how
to use ``FocalPointPlasticity`` plugin. Those examples also contain useful
comments.

.. note::

   When using ``FocalPointPlasticity`` Plugin from ``Mitosis`` module one might
   need to break or create focal point plasticity links. To do so
   ``FocalPointPlasticity`` Plugin provides 4 convenience functions which can
   be invoked from the Python level:

   .. code-block:: python

      deleteFocalPointPlasticityLink(cell1, cell2)

      deleteInternalFocalPointPlasticityLink(cell1, cell2)

      createFocalPointPlasticityLink(cell1, cell2, lambda , targetDistance, maxDistance)

      createInternalFocalPointPlasticityLink(cell1, cell2, lambda , targetDistance, maxDistance)

Working on the Basis of Links
-----------------------------

.. note::

   All functionality described in this section is relevant for CC3D versions 4.2.4+.

CC3D performs all link calculations on the basis of link objects. That is,
every link as described so far is an object with properties and functions that, much like ``CellG``
objects, can be created, destroyed and manipulated. As such, CC3DML specification tells CC3D to simulate links
and what types of links should be automatically created, but links can also be individually accessed, manipulated,
created and destroyed in Python. ``FocalPointPlasticity`` Plugin always uses the basis of links for link calculations,
and so the ``<Local/>`` tag in CC3DML ``FocalPointPlasticity`` Plugin specification is no longer necessary.

CC3D describes three types of links

  1. ``FocalPointPlasticityLink``: a link between two cells
  2. ``FocalPointPlasticityInternalLink``: a link between two cells of the same cluster
  3. ``FocalPointPlasticityAnchor``: a link between a cell and a point

``FocalPointPlasticityLink`` objects are automatically created from the CC3DML ``FocalPointPlasticity`` Plugin
specification in the tag ``Parameters``,
``FocalPointPlasticityInternalLink`` objects are automatically created from CC3DML specification in the tag
``InternalParameters``, and ``FocalPointPlasticityAnchor`` objects are only created in Python.
*CompuCell3D/core/Demos/PluginDemos/FocalPointPlasticityLinks* demonstrates basic usage of
``FocalPointPlasticityLink``, the pattern of which is mostly the same for ``FocalPointPlasticityInternalLink``
and ``FocalPointPlasticityAnchor`` except for naming conventions of certain properties, functions and objects.

CC3D adopts the convention that for every link with a cell pair (*i.e.*, ``FocalPointPlasticityLink`` and
``FocalPointPlasticityInternalLink``), one cell is the *initiator* cell (*i.e.*, the cell that initated the link), and
the other cell is the *initiated* cell. Using this convention, every link has the following API for manipulating
link properties,

.. code-block:: python

   # --------------
   # | Properties |
   # --------------
   # Link length; automatically updated by CC3D
   length
   # Link tension = 2 * lambda * (distance - target_distance); automatically updated by CC3D
   tension
   # A general python dictionary
   dict
   # SBML solvers (as on CellG)
   sbml
   # -----------
   # | Methods |
   # -----------
   # Given one cell, returns the other cell of a link
   getOtherCell(self, _cell: CellG) -> CellG
   # Returns True if the cell is the initiator
   isInitiator(self, _cell: CellG) -> bool
   # Get lambda distance
   getLambdaDistance(self) -> float
   # Set lambda distance
   setLambdaDistance(self, _lm: float) -> None
   # Get target distance
   getTargetDistance(self) -> float
   # Set target distance
   setTargetDistance(self, _td: float) -> None
   # Get maximum distance
   getMaxDistance(self) -> float
   # Set maximum distance
   setMaxDistance(self, _md: float) -> None
   # Get maximum number of junctions
   getMaxNumberOfJunctions(self) -> int
   # Set maximum number of junctions
   setMaxNumberOfJunctions(self, _mnj: int) -> None
   # Get activation energy
   getActivationEnergy(self) -> float
   # Set activation energy
   setActivationEnergy(self, _ae: float) -> None
   # Get neighbor order
   getNeighborOrder(self) -> int
   # Set neighbor order
   setNeighborOrder(self, _no: int) -> None
   # Get initialization step; automatically recorded at instantiation
   getInitMCS(self) -> int

So, for example, the value of :math:`\lambda_{ij}` for a link can be retrieved with ``link.getLambdaDistance()``,
and can be set with ``link.setLambdaDistance(lambda_ij)`` for some float-valued variable ``lambda_ij``. Links
automatically created by CC3D according to CC3DML specification are initialized with properties accordingly.
Additionally, ``FocalPointPlasticityLink`` and ``FocalPointPlasticityInternalLink`` objects have the property
``cellPair``, which contains, in order, the initiator and initiated cells of the link, while
each ``FocalPointPlasticityAnchor`` has the property ``cell`` (*i.e.*, the linked cell) and additional methods related
to its anchor point,

.. code-block:: python
   # Attached cell
   cell
   # Get anchor point as a 3-component list of floats
   getAnchorPoint(self) -> list
   # Set anchor point; _ap is a 3-component list of floats
   setAnchorPoint(self, _ap: list) -> None
   # Get anchor id
   getAnchorId(self) -> int

Steppables have built-in method for creating and destroying each type of link,

.. code-block:: python

   # Create a link between two cells
   new_fpp_link(self, initiator: CellG, initiated: CellG, lambda_distance: float, target_distance: float,
                max_distance: float) -> FocalPointPlasticityLink
   # Create an internal link between two cells of a cluster
   new_fpp_internal_link(self, initiator: CellG, initiated: CellG, lambda_distance: float,
                         target_distance: float, max_distance: float) -> FocalPointPlasticityInternalLink
   # Create an anchor
   # Anchor point can be specified by individual components x, y and z, or by Point3D pt
   new_fpp_anchor(self, cell: CellG, lambda_distance: float, target_distance: float,
                  max_distance: float, x: float = 0.0, y: float = 0.0, z: float = 0.0,
                  pt: Point3D = None) -> FocalPointPlasticityAnchor
   # Destroy a link type FocalPointPlasticityLink, FocalPointPlasticityInternalLink or FocalPointPlasticityAnchor
   delete_fpp_link(self, _link) -> None
   # Destroy all links attached to a cell by link type
   # links, internal_links and anchors selects which type, or all types if not specified
   remove_all_cell_fpp_links(self, _cell: CellG, links: bool = False, internal_links: bool = False,
                             anchors: bool = False) -> None

Steppables also have built-in methods for retrieving information about links in simulation, by cell, and by cell pair.
These methods are as follows,

.. code-block:: python

   # Get number of links
   get_number_of_fpp_links(self) -> int
   # Get number of internal links
   get_number_of_fpp_internal_links(self) -> int
   # Get number of anchors
   get_number_of_fpp_anchors(self) -> int
   # Get link associated with two cells
   get_fpp_link_by_cells(self, cell1: CellG, cell2: CellG) -> FocalPointPlasticityLink
   # Get internal link associated with two cells
   get_fpp_internal_link_by_cells(self, cell1: CellG, cell2: CellG) -> FocalPointPlasticityInternalLink
   # Get anchor assicated with a cell and anchor id
   get_fpp_anchor_by_cell_and_id(self, cell: CompuCell.CellG, anchor_id: int) -> FocalPointPlasticityAnchor
   # Get list of links by cell
   get_fpp_links_by_cell(self, _cell: CellG) -> FPPLinkList
   # Get list of internal links by cell
   get_fpp_internal_links_by_cell(self, _cell: CellG) -> FPPInternalLinkList
   # Get list of anchors by cell
   get_fpp_anchors_by_cell(self, _cell: CellG) -> FPPAnchorList
   # Get list of cells linked to a cell
   get_fpp_linked_cells(self, _cell: CompuCell.CellG) -> mvectorCellGPtr
   # Get list of cells internally linked to a cell
   get_fpp_internal_linked_cells(self, _cell: CellG) -> mvectorCellGPtr
   # Get number of link junctions by type for a cell
   get_number_of_fpp_junctions_by_type(self, _cell: CellG, _type: int) -> int
   # Get number of internal link junctions by type for a cell
   get_number_of_fpp_internal_junctions_by_type(self, _cell: CompuCell.CellG, _type: int) -> int



