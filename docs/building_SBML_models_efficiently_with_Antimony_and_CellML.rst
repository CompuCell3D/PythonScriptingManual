Building SBML models efficiently with Antimony and CellML
=========================================================

Now that we know how to write an Antimony model in Tellurium and use it with SBML solver,
let's explore some built-in functionality to efficiently write and use reaction-kinetics
models in Antimony and CellML [1]_ model definition languages. Antimony and CellML models can be
be attached to simulation objects exactly like SBML models, using variations in function naming
conventions corresponding to the choice in model specification (*e.g.*, for SBML model functions
``add_sbml_to_cell`` and ``add_sbml_to_link`` there are corresponding functions ``add_antimony_to_cell``,
``add_cellml_to_cell``, ``add_antimony_to_link`` and ``add_cellml_to_link``).
For Antimony and CellML model specification, models are translated to SBML using the libAntimony
library developed by Lucian Smith and Herbert Sauro. Furthermore, models can be specified in
external files and imported by CC3D steppables *or* within CC3D steppables as Python
multi-line strings.

Say we want to implement our previous Antimony model definition of an RK model:

.. code-block:: c++

    $X0 -> S1 ; k1*X0;
    S1 -> S2 ; k2*S1*S2^h/(10 + S2^h) + k3*S1;
    S2 -> $X3 ; k4*S2;

    h=2;
    k1 = 1.0;
    k2 = 2.0;
    k3 = 0.02;
    k4 = 1.0;
    X0 = 1;

Now say we want to attach the Antimony model definition to a cell *without* leaving
Twedit++, but rather all within a steppable ``AntimonySolverSteppable``. This can be
accomplished using a multi-line string using proper Antimony syntax:

.. code-block:: python

    class AntimonySolverSteppable(SteppableBasePy):

        def __init__(self,frequency=1):
            SteppableBasePy.__init__(self,frequency)

        def start(self):

            antimony_model_string = """model rkModel()
            $X0 -> S1 ; k1*X0;
            S1  -> S2 ; k2*S1*S2^h/(10 + S2^h) + k3*S1;
            S2  -> $X3 ; k4*S2;

            h  = 2;
            k1 = 1.0;
            k2 = 2.0;
            k3 = 0.02;
            k4 = 1.0;
            X0 = 1;
            end"""

            options = {'relative': 1e-10, 'absolute': 1e-12}
            self.set_sbml_global_options(options)
            step_size = 1e-2

            for cell in self.cell_list:
                self.add_antimony_to_cell(model_string=antimony_model_string,
                                          model_name='dp',
                                          cell=cell,
                                          step_size=step_size)

        def step(self):
            self.timestep_sbml()

Compared to attaching a SBML model to cells, we see that not much has changed
procedurally: we define a model (in this case, using Antimony instead of SBML), set the
requisite settings for SBML Solver, and attach our model to CC3D objects using built-in
functions (in this case, using ``add_antimony_to_cell`` instead of ``add_sbml_to_cell``). The
major differences here are that we have defined our model using Antimony model specification
within the steppable using built-in functions, and also that we defined our model initial
conditions with Antimony. In this case, SBML Solver retrieved our initial conditions from the
translation of our Antimony model, rather than from explicit arguments. Were we to also pass
initial conditions to SBML Solver as an argument through ``add_antimony_to_cell``, the
explicit calls would take precedence over those declared in the Antimony model string.

Now say that we've obtained a shared CellML model that we'd like to use in CC3D. We can
load the model specification from file:

.. code-block:: python

    class CellMLSolverSteppable(SteppableBasePy):

        def __init__(self,frequency=1):
            SteppableBasePy.__init__(self,frequency)

        def start(self):

            cellml_model_file = 'Simulation/shared_cellml_model.txt'

            options = {'relative': 1e-10, 'absolute': 1e-12}
            self.set_sbml_global_options(options)
            step_size = 1e-2

            self.add_cellml_to_cell_ids(model_file=cellml_model_file,
                                        model_name='dp',
                                        cell_ids=list(range(1,11)),
                                        step_size=step_size)

        def step(self):
            self.timestep_sbml()

Here the shared CellML model is stored in the same Simulation directory as the CC3D project
steppables, in the file ``shared_cellml_model.txt``. We pass the path of the model file to
``add_cellml_to_cell_ids`` to attach the shared CellML model to all cells with ids in the
list ``list(range(1,11))``, just like passing a SBML model file to ``add_sbml_to_cell_ids``.
Note that if the CellML model does not specify initial conditions, then we must explicitly
pass them to ``add_cellml_to_cell_ids``.

We see that there are two ways of passing an Antimony or CellML model to SBML Solver, either
as a Python multi-line string, or as a path to a file containing the model. One of these
must be accomplished, where a multi-line string is passed to the keyword argument
``model_string``, or a path to a file is passed to the keyword argument ``model_file``. These
are true for SBML, Antimony, and CellML built-in functions.

For attaching Antimony and CellML models to links, steppables have the functions ``add_antimony_to_link`` and
``add_cellml_to_link``. Their usage is the exact same as their cell-based counterparts, with the exception that
a link is passed to the keyword argument ``link``, rather than passing a cell to the keyword argument ``cell``,

.. code-block:: python

    self.add_antimony_to_link(link=link, ...)
    self.add_cellml_to_link(link=link, ...)

.. [1]
   Cuellar, A.A., Lloyd, C.M., Nielsen, P.F., Bullivant, D.P., Nickerson, D.P. and Hunter, P.J. An overview of CellML 1.1, a biological model description language. SIMULATION: Transactions of The Society for Modeling and Simulation International. 2003 Dec;79(12):740-747.