.. python_scripting_manual documentation master file, created by


CompuCell3D Manual - version 4.5.0
=======================================================

This manual teaches how to leverage Python for complex CompuCell3D simulations.
You do not need to be an expert in Python, but you should know how to write simple Python scripts
that use functions, classes, dictionaries, and lists.
You can find decent tutorials online (e.g.
`Instant Python Hacking <http://hetland.org/writing/instant-hacking.html>`__)
or watch the `CompuCell3D Workshop Python tutorial videos <https://www.youtube.com/watch?v=f_PJOGoCoEw&list=PLiEtieOeWbMKTIF2mekBc9cABFPEDwCdj>`__.

..
    [Link Last Updated] 2023


.. toctree::
    :caption: Introduction
    :maxdepth: 1
    :hidden:

    introduction

.. toctree::
    :caption: Intro to CC3D Python Programming
    :maxdepth: 1
    :hidden:

    section_python_tutorials


.. toctree::
    :caption: Writing Simulations in Pure Python
    :maxdepth: 1
    :hidden:

    cc3d_python


.. toctree::
    :caption: CC3D - How To
    :maxdepth: 1
    :hidden:

    section_how_to
    building_a_wall
    checking_if_two_cell_objects_point_to_different_cells
    example_mitosis
    example_contact_inhibited_cell_growth
    volume_and_growth
    surface
    mitosis
    cell_death
    reference_field_secretor
    field_secretion
    chemotaxis_on_a_cell-by-cell_basis
    steering_changing_cc3dml_parameters_on-the-fly
    steering_changing_python_parameters_using_UI
    replacing_cc3dml_with_equivalent_python_syntax
    cell_motility_applying_force_to_cells
    setting_cell_membrane_fluctuation_ona_cell-by-cell_basis
    dividing_clusters
    changing_cluster_id_of_a_cell

.. toctree::
    :caption: Network Solvers
    :hidden:

    sbml_solver
    building_sbml_models_using_tellurium
    building_SBML_models_efficiently_with_Antimony_and_CellML
    maboss


.. toctree::
    :caption: Screenshots, Restarts, Parameter Scans
    :hidden:

    configuring_multiple_screenshots
    parameter_scans
    restarting_simulations


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: XML Steppables

   section_steppable


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: XML Plugins

   section_plugins



.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: XML Expression Evaluator

   mu_parser


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: PDESolvers in CompuCell3D

   section_pde_solvers


.. toctree::
    :caption: Intro to Cellular Potts Model
    :maxdepth: 1
    :hidden:

    section_potts_and_lattice
    section_algorithms


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Real-world Examples

    section_real_world_examples


.. toctree::
    :caption: Legacy Content
    :hidden:

    transition_to_cc3d_4
    legacy_secretion


.. toctree::
    :maxdepth: 1
    :caption: Appendix
    :hidden:

    appendix_a
    appendix_b
    calling_cc3d_directly_from_python
    changing_number_of_worknodes
    authors
    funding
    references
