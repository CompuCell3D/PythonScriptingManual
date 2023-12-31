.. foldable table of content can be implemented by making sure that the headers
   follow proper hierarchy  - see http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html
    and making sure that the document that is at the "top of" of toc has subdocs listed as in this exa  mple

Plugins Section
================

In this section we overview CC3DML syntax for all the plugins available
in CompuCell3D. Plugins are either energy functions, lattice monitors or
store user assigned data that CompuCell3D uses internally to configure
simulation before it is run.

.. toctree::
    :maxdepth: 1

    cell_type_plugin
    global_volume_and_surface_plugins
    volume_and_surface_tracker_plugins
    volume_and_surface_flex_plugins
    neighbor_tracker
    chemotaxis_plugin
    external_potential_plugin
    center_of_mass_plugin
    contact_plugin
    adhesion_flex_plugin
    compartments
    length_constraint
    connectivity
    secretion
    pde_solver_caller
    focal_point_plasticity
    curvature
    pixel_tracking_plugins
    moment_of_inertia
    convergent_extension