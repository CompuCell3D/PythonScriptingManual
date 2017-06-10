Appendix A
==========

In this appendix we present alphabetical list of member functions and
objects of the SteppableBasePy class from which all steppables should
inherit:

**addFreeFloatingSBML** - adds free floating SBML solver object to the
simulation

**addNewPlotWindow** - adds new plot windows to the Player display

**addSBMLToCell** - attaches SBML solver object to individual cell

**addSBMLToCellIds** - attaches SBML solver object to individual cells with
specified ids

**addSBMLToCellTypes** - attaches SBML solver object to cells with specified
types

**adhesionFlexPlugin** - a reference to C++ AdhesionFlexPlugin object. None
if plugin not used.

**areCellsDifferent** - function determining if two cell objects are indeed
different objects

**attemptFetchingCellById** - fetches cell from cell inventory with
specified id. Returns None if cell cannot be found.

**boundaryMonitorPlugin** - a reference to C++ BoundaryMonitorPlugin object.
None if plugin not used

**boundaryPixelTrackerPlugin** - a reference to C++
BoundaryPixelTrackerPlugin object. None if plugin not used

**buildWall** - builds wall of cells (They have to be of cell type which has
Freeze attribute set in the Cell Type Plugin) around the lattice

**cellField** - reference to cell field.

**cellList** - cell list. Allows iteration over all cells in the simulation

**cellListByType** - function that creates on the fly a list of cells of
given cell types.

**cellOrientationPlugin** - a reference to C++ CellOrientationPlugin object.
None if plugin not used

**cellTypeMonitorPlugin** - a reference to C++ CellTypeMonitorPlugin object.
None if plugin not used

**centerOfMassPlugin** - a reference to C++ CenterOfMassPlugin object. None
if plugin not used

**changeNumberOfWorkNodes** - function that allows changing number of
worknodes use dby the simulation

**checkIfInTheLattice** - convenience function that determines if 3D point
is within lattice boundaries

**chemotaxisPlugin** - a reference to C++ ChemotaxisPlugin object. None if
plugin not used

**cleanDeadCells** - function that calls step function from
VolumetrackerPlugin to remove dead cell. Advanced use only.

**cleaverMeshDumper** - a reference to C++ CleaverMeshDumper object. None if
module not used. Experimental

**cloneAttributes** - copies all attributes from source cell to target cell.
Typically used in mitosis. Allows specification of attributes that
should not be copied.

**cloneParent2Child** - used in mitosis plugin. Copies all parent cell
attributes to the child cell.

**cloneClusterAttributes** - typically used in mitosis with
compartmentalized cells. Copies attributes from cell in a source cluster
to corresponging cell in the target cluster. Allows specification of
attributes that should not be copied

**cloneParentCluster2ChildCluster** - used in mitosis with compartmentalized
cells. Copies all attributes from cell in a parent cluster to
corresponging cell in the child cluster

**clusterInventory** - reference to C++ that serves as inventory of clusters

**clusterList** - Python-iterable list of clusters. Obsolete

**clusterSurfacePlugin** - a reference to C++ ClusterSurfacePlugin object.
None if module not used.

**clusterSurfaceTrackerPlugin** - a reference to C++
ClusterSurfaceTrackerPlugin object. None if module not used.

**clusters** - Python-iterable list of clusters.

**compilerExeFile** - name of C compiler used by SBML Solver.

**compilerSupportPath** - path to C compiler working directory - used by
SBML Solver

**connectivityGlobalPlugin** - a reference to C++ ConnectivityGlobalPlugin
object. None if module not used.

**connectivityLocalFlexPlugin** - a reference to C++
ConnectivityLocalFlexPlugin object. None if module not used.

**contactLocalFlexPlugin** - a reference to C++ ContactLocalFlexPlugin
object. None if module not used.

**contactLocalProductPlugin** - a reference to C++ ContactLocalProductPlugin
object. None if module not used.

**contactMultiCadPlugin** - a reference to C++ ContactMultiCadPlugin object.
None if module not used.

**contactOrientationPlugin** - a reference to C++ ContactOrientationPlugin
object. None if module not used.

**copySBMLs** - function that copies SBML Solver objects from one cell to
another

**createNewCell** - functionfor creating new CC3D cell

**createScalarFieldCellLevelPy** - function creating cell-level scalar field
for Player visualization.

**createScalarFieldPy** - function creating pixel-based scalar field for
Player visualization.

**createVectorFieldCellLevelPy** - function creating cell-level vector field
for Player visualization.

**createVectorFieldPy** -- function creating pixel-based vector field for
Player visualization.

**deleteCell** - function deleting cell.

**deleteFreeFloatingSBML** - function deleting free floarting SBML Solver
object with a given name.

**deleteSBMLFromCell** - function deleting SBML Solver object with a given
name from individual cell.

**deleteSBMLFromCellIds** - function deleting SBML Solver object with a
given name from individual cells with specified ids.

**deleteSBMLFromCellTypes** - function deleting SBML Solver object with a
given name from individual cells of specified types.

**destroyWall** - function destroying wall of frozen cells around the
lattice (if the wall exists)

**dim** - dimension of the lattice

**distance** - convenience function calculating distance between two 3D
points

**distanceBetweenCells** - convenience function calculating distance between
COMs of two cells.

**distanceVector** - convenience function calculating distance vector beween
two 3D points

**distanceVectorBetweenCells** - convenience function calculating distance
vector beween COMs of two cells

**elasticityTrackerPlugin** - a reference to C++ ElasticityTrackerPlugin
object. None if module not used.

**everyPixel** - Python-iterable object returning tuples (x,y,z) for every
pixel in the simulation. Allows iteration with user-defined steps
between pixels.

**everyPixelWithSteps** - internal function used by everyPixel.

**extraInit** - internal function

**finish** - core function of each CC3D steppable. Called at the end of the
simulation. User provide implementation of this function.

**focalPointPlasticityPlugin** - a reference to C++
FocalPointPlasticityPlugin object. None if module not used.

**frequency** - steppable call frequency.

getAnchorFocalPointPlasticityDataList

**getCellBoundaryPixelList** - function returning list of boundary pixels

**getCellByIds** - function that attemts fetching cell by cell id and cluste
id. See also attemptFetchingCellById

**getCellNeighborDataList** - function returning Python-iterable list of
tuples (neighbor, common surface area) that allows iteration over cell
neighbors

**getCellNeighbors** - function returning Python-iterable list of
NeighborSurfaceData objects. Slightly obsolete

**getCellPixelList** - function returning Python-iterable list of pixels
belonging to a given cell

**getClusterCells** - function returning Python iterable list of cells in a
cluster with a given cluster id.

**getConcentrationField** - function returning reference to a concentration
field with a given name. Returns None if field not found

**getCopyOfCellBoundaryPixels** - function creating and returning new
Python-iterable list of cell pixels of all pixels belonging to a
boundary of a given cell.

**getCopyOfCellPixels** - function creating and returning new
Python-iterable list of cell pixels of all pixels belonging to a given
cell.

**getDictionaryAttribute** - function returning Python-dictionary attached
to each cell.

**getElasticityDataList** - function returning Python-iterable list of C++
ElasticityData objects. Used in conjunction with ElasticityPlugin

**getFieldSecretor** - function returning Secretor object that allows
implementation of secretion in a cell-by-cell fashion.

**getFocalPointPlasticityDataList** - function returning Python-iterable
list of C++ FocalPointPlasticityData objects. Used in conjunction with
FocalPointPlasticityPlugin.

**getInternalFocalPointPlasticityDataList** - function returning
Python-iterable list of C++ InternalFocalPointPlasticityData objects.
Used in conjunction with FocalPointPlasticityPlugin.

**getPixelNeighborsBasedOnDistance** - function returning Python-iterable
list of pixels which are withing given distance of the specified pixel

**getPixelNeighborsBasedOnNeighborOrder** - function returning
Python-iterable list of pixels which are withing given neighbor order of
the specified pixel

**getPlasticityDataList** - function returning Python-iterable list of C++
tPlasticityData objects. Used in conjunction with PlasticityPlugin.
Deprecated

**getSBMLSimulator** - gets RoadRunner object

**getSBMLState** - gets Python-dictionary describing state of the SBML
model.

**getSBMLValue** - gets numerical value of the SBML model parameter

**getSteppableByClassName** - fetches steppable object using class name

**getSteppableListByClassName** - fetches list of steppable objects using
class name.

**init** - internal use only

**invariantDistance** - calculates invariant distance between two 3D points

**invariantDistanceBetweenCells** - calculates invariant distance between
COMs of two cells.

**invariantDistanceVector** - calculates invariant distance vector between
two 3D points

**invariantDistanceVectorBetweenCells** - calculates invariant distance
vector between COMs of two cells.

**invariantDistanceVectorInteger** - calculates invariant distance vector
between two 3D points. Keeps vector components as integer numbers

**inventory** - inventory of cells. C++ object

**lengthConstraintPlugin** - a reference to C++ LengthConstraintPlugin
object. None if module not used.

**momentOfInertiaPlugin** - a reference to C++ MomentOfInertiaPlugin object.
None if module not used.

**moveCell** - moves cell by a specified shift vector

**neighborTrackerPlugin** - a reference to C++ NeighborTrackerPlugin object.
None if module not used.

**newCell** - creates new cell of the user specified type

**normalizePath** - ensures that file path obeys rules of current operating
system

**numpyToPoint3D** - converts numpy vector to Point3D object

**openFileInSimulationOutputDirectory** - opens file using use specified
file open mode in the simulation output directory

**pixelTrackerPlugin** - a reference to C++ PixelTrackerPlugin object. None
if module not used.

**plasticityTrackerPlugin** - a reference to C++ PlasticityTrackerPlugin
object. None if module not used.

**point3DToNumpy** - converts Point3D to numpy vector

**polarization23Plugin** - a reference to C++ Polarization23Plugin object.
None if module not used.

**polarizationVectorPlugin** - a reference to C++ PolarizationVectorPlugin
object. None if module not used.

**potts** - reference to C++ Potts object

**reassignClusterId** - reassignes cluster id. **Notice:** you cannot type
cell.clusterId=20. This will corrupt cell inventory. Use
reassignClusterId instead

**removeAttribute** - internal use

**resizeAndShiftLattice** - resizes lattice and shifts its content by a
specified vector. Throws an exception if operation cannot be safely
performed.

**runBeforeMCS** - flag determining if steppable gets called before
(runBeforeMCS=1) Monte Carlo Step of after (runBeforeMCS=1). Default
value is 0.

secretionPlugin- a reference to C++ SecretionPlugin object. None if
module not used.

**setFrequency** - sets steppable call frequency (equivalend to
self.frequency=FREQ\_VALUE)

**setMaxMCS** - sets maximum MCS. Used to increase or decrease number of MCS
that simulation shuold complete.

**setSBMLState** - used to pass dictionary of values of SBML variables

**setSBMLValue** - sets single SBML variable with a given name

**setStepSizeForCell** - sets integration step for a given SBML Solver
object in a specified cell

**setStepSizeForCellIds** - sets integration step for a given SBML Solver
object in cells of specified ids

**setStepSizeForCellTypes** - sets integration step for a given SBML Solver
object in cells of specified types

**setStepSizeForFreeFloatingSBML** - sets integration step for a given free
floating SBML Solver object

**simulator** - a reference to C++ Simulator object

**start** - core function of the steppable. Users provide implementation of
this function

**step** - core function of the steppable. Users provide implementation of
this function

**stopSimulation** - function used to stop simulation immediately

**tempDirPath** - temporaty directory path used by SBML solver

**timestepCellSBML** - function carrying out integration of all SBML models
in the SBML Solver objects belonging to cells.

**timestepFreeFloatingSBML** - function carrying out integration of all SBML
models in the free floating SBML Solver objects

**timestepSBML** - function carrying out integration of all SBML models in
all SBML Solver objects

**typeIdTypeNameDict** - internal use only

**vectorNorm** - function calculating norm of a vector

**volumeTrackerPlugin** - a reference to C++ VolumeTrackerPlugin object.
None if module not used.

Additionally MitosisPlugin base has these functions:

**childCell** - a reference to a cell object that has jus been created as a
result of mitosis

**parentCell** - a reference to a cell object that underwent mitisos. After
mitosis this cell object will have smalle volume

**setParentChildPositionFlag** - function which sets flag determining
relative positions of child and parent cells after mitosis. Value 0
means that parent child position will be randomized between mitosis
event. Negative integer value means parent appears on the 'left' of the
child and positive integer values mean that parent appears on the
'right' of the child.

**getParentChildPositionFlag** - returns current value of
parentChildPositionFlag.

**divideCellRandomOrientation** - divides parent cell using randomly chosen
cleavage plane.

**divideCellOrientationVectorBased** - divides parent cell using cleavage
plane perpendicular to a given vector.

**divideCellAlongMajorAxis** - divides parent cell using cleavage plane
along major axis

**divideCellAlongMinorAxis** - divides parent cell using cleavage plane
along minor axis

**updateAttributes** - function called immediately after each mitosis
event.Users provide implementation of this function.
