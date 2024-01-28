Appendix A: List of Base Steppable Functions
=======================================================

In this appendix, we present an alphabetical list of member functions and
objects of the SteppableBasePy class from which all steppables should
inherit:

``add_antimony_to_cell`` - translates Antimony model to SBML and forwards it
to ``add_sbml_to_cell``

``add_antimony_to_cell_ids`` - translates Antimony model to SBML and forwards it
to ``add_sbml_to_cell_ids``

``add_antimony_to_cell_types`` - translates Antimony model to SBML and forwards it
to ``add_sbml_to_cell_types``

``add_cellml_to_cell`` - translates CellML model to SBML and forwards it
to ``add_sbml_to_cell``

``add_cellml_to_cell_ids`` - translates CellML model to SBML and forwards it
to ``add_sbml_to_cell_ids``

``add_cellml_to_cell_types`` - translates CellML model to SBML and forwards it
to ``add_sbml_to_cell_types``

``add_free_floating_antimony`` - translates Antimony model to SBML and forwards it
to ``add_free_floating_sbml``

``add_free_floating_cellml`` - translates CellML model to SBML and forwards it
to ``add_free_floating_sbml``

``add_free_floating_sbml`` - adds free floating SBML solver object to the
simulation

``add_new_plot_window`` - adds new plot windows to the Player display

``add_sbml_to_cell`` - attaches SBML solver object to individual cell

``add_sbml_to_cell_ids`` - attaches SBML solver object to individual cells with
specified ids

``add_sbml_to_cell_types`` - attaches SBML solver object to cells with specified
types

``adhesionFlexPlugin`` - a reference to C++ AdhesionFlexPlugin object. None
if plugin not used.

``are_cells_different`` - function determining if two cell objects are indeed
different objects

``boundaryMonitorPlugin`` - a reference to C++ BoundaryMonitorPlugin object.
None if plugin not used

``boundaryPixelTrackerPlugin`` - a reference to C++
BoundaryPixelTrackerPlugin object. None if plugin not used

``build_wall`` - builds wall of cells (They have to be of cell type which has
Freeze attribute set in the Cell Type Plugin) around the lattice

``cell_field`` - reference to cell field.

``cell_list`` - cell list. Allows iteration over all cells in the simulation

``cell_list_by_type`` - function that creates on the fly a list of cells of
given cell types.

``cellOrientationPlugin`` - a reference to C++ CellOrientationPlugin object.
None if plugin not used

``cellTypeMonitorPlugin`` - a reference to C++ CellTypeMonitorPlugin object.
None if plugin not used

``centerOfMassPlugin`` - a reference to C++ CenterOfMassPlugin object. None
if plugin not used

``change_number_of_work_nodes`` - function that allows changing number of
worknodes use dby the simulation

``check_if_in_the_lattice`` - convenience function that determines if 3D point
is within lattice boundaries

``chemotaxisPlugin`` - a reference to C++ ChemotaxisPlugin object. None if
plugin not used

``cleanDeadCells`` - function that calls step function from
VolumetrackerPlugin to remove dead cell. Advanced use only. Deprecated in CC3D 4.x

``cleaverMeshDumper`` - a reference to C++ CleaverMeshDumper object. None if
module not used. Experimental. Deprecated in CC3D 4.0.0

``clone_attributes`` - copies all attributes from source cell to target cell.
Typically used in mitosis. Allows specification of attributes that
should not be copied.

``clone_parent_2_child`` - used in mitosis plugin. Copies all parent cell
attributes to the child cell.

``clone_cluster_attributes`` - typically used in mitosis with
compartmentalized cells. Copies attributes from cell in a source cluster
to corresponging cell in the target cluster. Allows specification of
attributes that should not be copied

``clone_parent_cluster_2_child_cluster`` - used in mitosis with compartmentalized
cells. Copies all attributes from cell in a parent cluster to
corresponding cell in the child cluster

``cluster_list`` - Python-iterable list of clusters. Obsolete

``clusterSurfacePlugin`` - a reference to C++ ClusterSurfacePlugin object.
None if module not used.

``clusterSurfaceTrackerPlugin`` - a reference to C++
ClusterSurfaceTrackerPlugin object. None if module not used.

``clusters`` - Python-iterable list of clusters.

``connectivityGlobalPlugin`` - a reference to C++ ConnectivityGlobalPlugin
object. None if module not used.

``connectivityLocalFlexPlugin`` - a reference to C++
ConnectivityLocalFlexPlugin object. None if module not used.

``contactLocalFlexPlugin`` - a reference to C++ ContactLocalFlexPlugin
object. None if module not used.

``contactLocalProductPlugin`` - a reference to C++ ContactLocalProductPlugin
object. None if module not used.

``contactMultiCadPlugin`` - a reference to C++ ContactMultiCadPlugin object.
None if module not used.

``contactOrientationPlugin`` - a reference to C++ ContactOrientationPlugin
object. None if module not used.

``copy_sbml_simulators`` - function that copies SBML Solver objects from one cell to
another

``create_scalar_field_cell_level_py`` - function creating cell-level scalar field
for Player visualization.

``create_scalar_field_py`` - function creating pixel-based scalar field for
Player visualization.

``create_vector_field_cell_level_py`` - function creating cell-level vector field
for Player visualization.

``create_vector_field_py`` -- function creating pixel-based vector field for
Player visualization.

``delete_cell`` - function deleting cell.

``delete_free_floating_sbml`` - function deleting free floarting SBML Solver
object with a given name.

``delete_sbml_from_cell`` - function deleting SBML Solver object with a given
name from individual cell.

``delete_sbml_from_cell_ids`` - function deleting SBML Solver object with a
given name from individual cells with specified ids.

``delete_sbml_from_cell_types`` - function deleting SBML Solver object with a
given name from individual cells of specified types.

``destroy_wall`` - function destroying wall of frozen cells around the
lattice (if the wall exists)

``dim`` - dimension of the lattice

``distance`` - convenience function calculating distance between two 3D
points

``distance_between_cells`` - convenience function calculating distance between
COMs of two cells.

``distance_vector`` - convenience function calculating distance vector beween
two 3D points

``distance_vector_between_cells`` - convenience function calculating distance
vector beween COMs of two cells

``elasticityTrackerPlugin`` - a reference to C++ ElasticityTrackerPlugin
object. None if module not used.

``every_pixel`` - Python-iterable object returning tuples (x,y,z) for every
pixel in the simulation. Allows iteration with user-defined steps
between pixels.

``every_pixel_with_steps`` - internal function used by everyPixel.

``fetch_cell_by_id`` - fetches cell from cell inventory with
specified id. Returns None if cell cannot be found.

``finish`` - core function of each CC3D steppable. Called at the end of the
simulation. User provide implementation of this function.

``focalPointPlasticityPlugin`` - a reference to C++
FocalPointPlasticityPlugin object. None if module not used.

``frequency`` - steppable call frequency.

``get_anchor_focal_point_plasticity_data_list`` -  returns a list anchored links

``get_box_coordinates`` - returns the two points defining the smallest box containing
all cells in simulation.

``get_cell_boundary_pixel_list`` - function returning list of boundary pixels

``get_cell_neighbor_data_list`` - function returning Python-iterable list of
tuples (neighbor, common surface area) that allows iteration over cell
neighbors

``get_cell_pixel_list`` - function returning Python-iterable list of pixels
belonging to a given cell

``get_cluster_cells`` - function returning Python iterable list of cells in a
cluster with a given cluster id.

``get_copy_of_cell_boundary_pixels`` - function creating and returning new
Python-iterable list of cell pixels of all pixels belonging to a
boundary of a given cell.

``get_copy_of_cell_pixels`` - function creating and returning new
Python-iterable list of cell pixels of all pixels belonging to a given
cell.

``get_elasticity_data_list`` - function returning Python-iterable list of C++
ElasticityData objects. Used in conjunction with ElasticityPlugin

``get_energy_calculations`` - function returning iterator of flip result
and dictionary of effective energies by energy function for all flip attempts
of the most recent Monte Carlo step. Requires ``EnergyFunctionCalculator`` with
Type "Statistics".

``get_field_secretor`` - function returning Secretor object that allows
implementation of secretion in a cell-by-cell fashion.

``get_focal_point_plasticity_data_list`` - function returning Python-iterable
list of C++ FocalPointPlasticityData objects. Used in conjunction with
FocalPointPlasticityPlugin.

``get_focal_point_plasticity_neighbor_list`` - function returning a
Python-iterable list of all cell objects linked to a cell. Used in conjunction
with FocalPointPlasticityPlugin.

``get_focal_point_plasticity_num_neighbors`` - function returning the
number of links attached to a cell. Used in conjunction with
FocalPointPlasticityPlugin.

``get_focal_point_plasticity_is_linked`` - function returning a Boolean
signifying whether two cells are linked. Used in conjunction with
FocalPointPlasticityPlugin.

``get_focal_point_plasticity_initiator`` - function returning which of
two linked cells initiated the link, or None if two cells are not linked.
Used in conjunction with FocalPointPlasticityPlugin.

``get_internal_focal_point_plasticity_data_list`` - function returning
Python-iterable list of C++ InternalFocalPointPlasticityData objects.
Used in conjunction with FocalPointPlasticityPlugin.

``get_pixel_neighbors_based_on_neighbor_order`` - function returning
Python-iterable list of pixels which are withing given neighbor order of
the specified pixel

``get_plasticity_data_list`` - function returning Python-iterable list of C++
tPlasticityData objects. Used in conjunction with PlasticityPlugin.
Deprecated

``get_sbml_simulator`` - gets RoadRunner object for a given cell

``get_sbml_state`` - gets Python-dictionary describing state of the SBML
model.

``get_sbml_value`` - gets numerical value of the SBML model parameter

``get_type_name_by_cell`` - gets string name of cell type

``init`` - internal use only

``invariant_distance`` - calculates invariant distance between two 3D points

``invariant_distance_between_cells`` - calculates invariant distance between
COMs of two cells.

``invariant_distance_vector`` - calculates invariant distance vector between
two 3D points

``invariant_distance_vector_between_cells`` - calculates invariant distance
vector between COMs of two cells.

``invariant_distance_vector_integer`` - calculates invariant distance vector
between two 3D points. Keeps vector components as integer numbers

``inventory`` - inventory of cells. C++ object

``lengthConstraintPlugin`` - a reference to C++ LengthConstraintPlugin
object. None if module not used.

``momentOfInertiaPlugin`` - a reference to C++ MomentOfInertiaPlugin object.
None if module not used.

``move_cell`` - moves cell by a specified shift vector

``neighborTrackerPlugin`` - a reference to C++ NeighborTrackerPlugin object.
None if module not used.

``new_cell`` - creates new cell of the user specified type

``normalize_path`` - ensures that file path obeys rules of current operating
system

``numpy_to_point_3d`` - converts numpy vector to Point3D object

``open_file_in_simulation_output_folder`` - function returning the file
handle and output path of a file in the simulation output folder. Returns
None, None if the file cannot be opened.

``output_dir`` - simulation output directory

``pixelTrackerPlugin`` - a reference to C++ PixelTrackerPlugin object. None
if module not used.

``plasticityTrackerPlugin`` - a reference to C++ PlasticityTrackerPlugin
object. None if module not used.

``point_3d_to_numpy`` - converts Point3D to numpy vector

``polarization23Plugin`` - a reference to C++ Polarization23Plugin object.
None if module not used.

``polarizationVectorPlugin`` - a reference to C++ PolarizationVectorPlugin
object. None if module not used.

``potts`` - reference to C++ Potts object

``reassign_cluster_id`` - reassignes cluster id. **Notice:** you cannot type
cell.clusterId=20. This will corrupt cell inventory. Use
reassignClusterId instead

``remove_attribute`` - internal use

``resize_and_shift_lattice`` - resizes lattice and shifts its content by a
specified vector. Throws an exception if operation cannot be safely
performed.

``runBeforeMCS`` - flag determining if steppable gets called before
(runBeforeMCS=1) Monte Carlo Step of after (runBeforeMCS=1). Default
value is 0.

``secretionPlugin`` - a reference to C++ SecretionPlugin object. None if
module not used.

``set_focal_point_plasticity_parameters`` - convenience function for setting
various focal point plasticity parameters for a cell. Used in conjunction with
FocalPointPlasticityPlugin.

``set_max_mcs`` - sets maximum MCS. Used to increase or decrease number of MCS
that simulation shuold complete.

``set_sbml_state`` - used to pass dictionary of values of SBML variables

``set_sbml_value`` - sets single SBML variable with a given name

``set_step_size_for_cell`` - sets integration step for a given SBML Solver
object in a specified cell

``set_step_size_for_cell_ids`` - sets integration step for a given SBML Solver
object in cells of specified ids

``set_step_size_for_cell_types`` - sets integration step for a given SBML Solver
object in cells of specified types

``set_step_size_for_free_floating_sbml`` - sets integration step for a given free
floating SBML Solver object

``shared_steppable_vars`` - reference to a global dictionary shared by all
steppables.

``simulator`` - a reference to C++ Simulator object

``start`` - core function of the steppable. Users provide implementation of
this function

``step`` - core function of the steppable. Users provide implementation of
this function

``stop_simulation`` - function used to stop simulation immediately

``timestep_cell_sbml`` - function carrying out integration of all SBML models
in the SBML Solver objects belonging to cells.

``timestep_free_floating_sbml`` - function carrying out integration of all SBML
models in the free floating SBML Solver objects

``timestep_sbml`` - function carrying out integration of all SBML models in
all SBML Solver objects

``translate_to_sbml_string`` - function returning a string of SBML model specification
translated from Antimony or CellML model specification file or string

``typeIdTypeNameDict`` - internal use only - translates type id to type name

``vector_norm`` - function calculating norm of a vector

``volumeTrackerPlugin`` - a reference to C++ VolumeTrackerPlugin object.
None if module not used.

Additionally MitosisPlugin base has these functions:

``child_Cell`` - a reference to a cell object that has jus been created as a
result of mitosis

``parent_cell`` - a reference to a cell object that underwent mitisos. After
mitosis this cell object will have smalle volume

``set_parent_child_position_flag`` - function which sets flag determining
relative positions of child and parent cells after mitosis. Value 0
means that parent child position will be randomized between mitosis
event. Negative integer value means parent appears on the 'left' of the
child and positive integer values mean that parent appears on the
'right' of the child.

``get_parent_child_position_flag`` - returns current value of
parentChildPositionFlag.

``divide_cell_random_orientation`` - divides parent cell using randomly chosen
cleavage plane.

``divide_cell_orientation_vector_based`` - divides parent cell using cleavage
plane perpendicular to a given vector.

``divide_cell_along_major_axis`` - divides parent cell using cleavage plane
along major axis

``divide_cell_along_minor_axis`` - divides parent cell using cleavage plane
along minor axis

``update_attributes`` - function called immediately after each mitosis
event.Users provide implementation of this function.
