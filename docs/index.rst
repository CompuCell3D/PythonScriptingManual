.. python_scripting_manual documentation master file, created by


Python Scripting Manual for CompuCell3D - version 4.4.1
=======================================================

This manual teaches how to leverage Python for complex CompuCell3D simulations.
You do not need to be an expert in Python, but you should know how to write simple Python scripts
that use functions, classes, dictionaries, and lists.
You can find decent tutorials online (e.g.
`Instant Python Hacking <http://hetland.org/writing/instant-hacking.html>`__)
or watch the `CompuCell3D Workshop Python tutorial videos <https://www.youtube.com/watch?v=f_PJOGoCoEw&list=PLiEtieOeWbMKTIF2mekBc9cABFPEDwCdj>`__.

..
    [Last Updated] 2023


.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Introduction

    introduction
    section_python_tutorials


.. toctree::
    :caption: Textbook and Guides

    section_steppable
    section_plugins
    section_potts_and_lattice
    section_initializers
    section_algorithms
    
    iterating_over_cell_neighbors
    field_secretion
    chemotaxis_on_a_cell-by-cell_basis
    steering_changing_cc3dml_parameters_on-the-fly
    steering_changing_python_parameters_using_UI
    replacing_cc3dml_with_equivalent_python_syntax
    cell_motility_applying_force_to_cells
    setting_cell_membrane_fluctuation_ona_cell-by-cell_basis
    modifying_attributes_of_cellg_object
    steppable_frequency
    resizing_the_lattice
    changing_number_of_worknodes
    dividing_clusters
    changing_cluster_id_of_a_cell
    sbml_solver
    building_sbml_models_using_tellurium
    building_SBML_models_efficiently_with_Antimony_and_CellML
    maboss
    configuring_multiple_screenshots
    parameter_scans
    restarting_simulations
    implementing_energy_functions_in_python
    recording_screenshots


.. toctree::
    :caption: Reference

    volume_and_growth
    surface
    mitosis
    cell_death
    reference_field_secretor
    section_pde_solvers
    section_tutorials
    

.. toctree::
    :caption: Examples

    building_a_wall
    checking_if_two_cell_objects_point_to_different_cells
    chemotaxis_on_a_cell-by-cell_basis
    example_mitosis
    example_contact_inhibited_cell_growth


.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Legacy Content

    transition_to_cc3d_4
    legacy_secretion


.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Appendix

    appendix_a
    appendix_b
    cc3d_python
    calling_cc3d_directly_from_python
    authors
    funding
    references
