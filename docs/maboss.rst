Building and Using MaBoSS Models
================================

As of v4.2.5., CC3D supports simulating boolean models using MaBoSS (Markovian Boolean Stochastic Simulator)
[1]_ and attaching them to cells.
MaBoSS enables representing intracellular mechanisms like gene regulatory networks and
chemical kinetics as Boolean networks, on which MaBoSS simulates continuous or discrete time
Markov processes.
CC3D provides an interactive version of MaBoSS simulations with select MaBoSS simulation capabilities,
so that individual networks can be selectively integrated in time, modified, and reconfigured according
to an overall CC3D simulation.
With combined capabilities, MaBoSS models in CC3D can be interconnected and coupled with cellular
properties, local conditions, and ODE models.
For a detailed description of MaBoSS capabilities, examples of MaBoSS simulations and downloading the
full, standalone MaBoSS simulation package, visit the `MaBoSS homepage <https://maboss.curie.fr/>`_.

.. note::

    To cite MaBoSS usage in CC3D, use the following,

    Stoll, Gautier, et al. "MaBoSS 2.0: an environment for stochastic Boolean modeling." Bioinformatics 33.14 (2017): 2226-2228.

Building a MaBoSS Model in CC3D
-------------------------------

MaBoSS simulation specification is divided into two components: a network description, and a simulation
configuration.
A MaBoSS network description describes a network on the basis of nodes, including the name, logic, and
transition rates of each node of the network.
A MaBoSS simulation configuration describes the network parameters and initial conditions.
Typical MaBoSS usage includes creating a network description file with the extension ``.bnd`` and a
configuration file with the extension ``.cfg``, which are both passed to MaBoSS using a terminal.
In CC3D, MaBoSS simulations can be created using any combination of network and configuration files `or`
multiline strings.

A very simple network description of two nodes ``A`` and ``B`` in a multiline string could look like
the following,

.. code-block:: python

    """
    node A {
        logic = $B_ext && !B;
        rate_up = @logic ? $node_rate : 0.0;
        rate_down = @logic ? 0.0 : $node_rate;
    }
    node B {
        logic = A;
        rate_up = @logic ? $node_rate : 0.0;
        rate_down = $node_rate / 10;
    }
    """

The network description describes the logic of each node (`i.e.`, ``logic``), and an expression for
the rate of each node going from 0 to 1 (`i.e.`, ``rate_up``) and going from 1 to 0 (`i.e.`, ``rate_down``).
Rate expressions can be constant (`e.g.`, ``rate_down`` for node ``B``), or conditional
(`e.g.`, ``rate_down`` for node ``B``).
For conditional expressions, the syntax ``X ? Y : Z`` reads ``Y`` if ``X`` is true, otherwise ``Z``.
The network also uses two external variables ``$B_ext`` and ``$node_rate``, the values of which are
specified in the configuration file and, along with everything else described in this network except the
network itself, can be accessed and modified in CC3D for individual simulation instances of this network.

A corresponding configuration for this network in a multiline string could look like the following,

.. code-block:: python

    """
    A.istate = FALSE;
    $B_ext = FALSE;
    $node_rate = 10.0;
    """

The configuration declares the initial state of node ``A``, and declares values for the external
variables ``$B_ext`` and ``$node_rate``.
Note that, since the configuration does not declare the initial state of node ``B``, each network
instance will initialize node ``B`` with a randomly selected state.

.. note::

    MaBoSS provides additional specification capabilities for the configuration file
    (`e.g.`, declaring a random generator seed).
    The network and configuration specification relevant to MaBoSS simulations in CC3D are described
    in the previous example.
    The remaining inputs relevant to specifying a MaBoSS simulation in CC3D are described in
    subsequent text, and are declared through an interface provided by CC3D.

A MaBoSS simulation can be created and attached to a cell in CC3D using MaBoSS network description and
configuration files from within a steppable,

.. code-block:: python

    self.add_maboss_to_cell(cell=cell,
                            model_name=model_name,
                            bnd_file=bnd_file,
                            cfg_file=cfg_file,
                            time_step=time_step,
                            time_tick=time_tick)

Here ``cell`` is the CC3D cell to which the MaBoSS simulation should be attached,
``model_name`` is a string that declares an alias name by which the MaBoSS simulation can be
accessed after the call,
``bnd_file`` and ``cfg_file`` are the absolute path to the location of a network description and
configuration file, respectively,
``time_step`` is a ``float`` equal to the MaBoSS simulation time that corresponds to one simulation step in CC3D,
and ``time_tick`` is the MaBoSS simulation time that corresponds to considering the transition of every
node in the network one time (`i.e.`, the MaBoSS `time window`).

MaBoSS model and simulation specification declared in Python multiline strings can also be used to
create a MaBoSS simulation and attach it to a cell,

.. code-block:: python

    self.add_maboss_to_cell(cell=cell,
                            model_name=model_name,
                            bnd_str=bnd_str,
                            cfg_str=cfg_str,
                            time_step=time_step,
                            time_tick=time_tick)

Here ``bnd_str`` and ``cfg_str`` are network description and configuration multiline strings, respectively
(`i.e.`, the contents of a file, but as a multiline string).
Any combination of file path and string inputs can be used for passing the network description and configuration,
so long as each is passed.

MaBoSS simulations can also be created from within a steppable without being attached to a cell,

.. code-block:: python

    mm = self.maboss_model(model_name=model_name,
                           bnd_file=bnd_file,
                           cfg_file=cfg_file,
                           time_step=time_step,
                           time_tick=time_tick)

The same can be accomplished from outside a steppable using a function of the same name and arguments
from the ``cc3d.core.MaBoSSCC3D`` module,

.. code-block:: python

    from cc3d.core import MaBoSSCC3D
    mm = MaBoSSCC3D.maboss_model(model_name=model_name,
                                 bnd_file=bnd_file,
                                 cfg_file=cfg_file,
                                 time_step=time_step,
                                 time_tick=time_tick)

Both implementations of ``maboss_model`` take the same optional arguments as the steppable method
``add_maboss_to_cell`` (`e.g.`, the keyword arguments ``bnd_str`` and ``seed``).

MaBoSS simulations are automatically destroyed when a cell is destroyed unless the MaBoSS simulation is
also stored elsewhere (`e.g.`, as an attribute on a steppable).
MaBoSS simulations can also be manually removed from a cell,

.. code-block:: python

    self.delete_maboss_from_cell(cell=cell, model_name=model_name)

All provided functions to create MaBoSS simulations in CC3D can also take optional keyword arguments,

-   ``discrete_time`` takes a Boolean value (default is ``False``). When passing ``discrete_time=True``,
    a MaBoSS simulation will perform time integration with fixed time intervals equal to ``time_tick``
    until an amount of time equal to ``time_step`` has elapsed for one integration step.
    By default, a MaBoSS simulation will integrate using the Gillespie algorithm.

-   ``seed`` takes an integer value (default is 0) as the seed for the random generator of the MaBoSS
    simulation.

-   ``istate`` a dictionary of string names and corresponding initial state values.

.. note::

    A ``time_step`` value less than a ``time_tick`` value is only valid when using the default Gillespie
    algorithm.
    Otherwise, the ``time_step`` value must be greater than the ``time_tick`` value for anything to occur.

Interacting with a MaBoSS Model
-------------------------------

All MaBoSS simulations attached to each cell can be accessed using the cell property ``maboss`` and referring
to the alias of the model as passed to the keyword argument ``model_name`` when the simulation was created,

.. code-block:: python

    self.add_maboss_to_cell(cell=cell, model_name='MyMaBoSSModel', ...)
    ...
    mm = cell.maboss.MyMaBoSSModel

Every MaBoSS simulation attached to every cell in simulation can be integrated one step in time
from a steppable,

.. code-block:: python

    self.timestep_maboss()

Likewise, a MaBoSS simulation instance can be individually integrated one step in time,

.. code-block:: python

    cell.maboss.MyMaBoSSModel.step()

The values passed to the keyword arguments ``time_step``, ``time_tick``, ``discrete_time`` and ``seed``
when creating a MaBoSS simulation can all be overwritten at any time by interacting with the
MaBoSS simulation instance and its attached ``CC3DRunConfig`` object,

.. code-block:: python

    mm = cell.maboss.MyMaBoSSModel
    mm.step_size *= 2.0  # Double value passed to time_step
    mm.run_config.time_tick /= 2.0  # Half value passed to time_tick
    mm.run_config.discrete_time = False  # Enable Gillespie algorithm
    mm.run_config.seed - mm.run_config.seed + 1  # Increment value passed to seed

Each node of a MaBoSS simulation network can be accessed as if interacting with a Python dictionary.
For example, to get node ``A`` in a network attached to a cell with alias ``MyMaBoSSModel``,

.. code-block:: python

    node_a = cell.maboss.MyMaBoSSModel['A']

Data about a node can be accessed and, where appropriate, set using properties and functions of a node.
For example, the state of a node can be accessed and set using the property ``state`` such that
networks of individual cells and/or multiple networks in the same cell can be coupled,

.. code-block:: python

    node_1a = cell1.maboss.MyMaBoSSModel['A']
    node_1ao = cell1.maboss.MyOtherMaBoSSModel['A']
    node_2b = cell2.maboss.MyMaBoSSModel['B']
    node_1a.state = node_2b.state or node_1ao.state

Likewise, the value of external variables can be accessed and set using the MaBoSS ``Network`` attached to a
MaBoSS simulation.
The network of a MaBoSS simulation can be accessed with the property ``network``, and the external variables
of a network can be accessed and set using the property ``symbol_table`` of the network.
For example, an external variable declared in a MaBoSS simulation specification as ``$cellVolume`` can be
coupled to the current volume of a cell (`e.g.`, to use the cell volume as a MaBoSS model parameter),

.. code-block:: python

    cell.maboss.MyMaBoSSModel.network.symbol_table['cellVolume'] = cell.volume

CC3D MaBoSS API
---------------

For brevity and generality, the following APIs are presented as relevant to modeling and simulation using
CC3D and MaBoSS.

The module ``cc3d.cpp.MaBoSSCC3DPy`` contains the following relevant API,

.. code-block:: python

    # Network node
    class CC3DMaBoSSNode:
        # Description; read-only
        description: str
        # Input node flag; read-only
        is_input: bool
        # Internal node flag
        is_internal: bool
        # Reference node flag
        is_reference: bool
        # Initial state
        istate: bool
        # Current rate down; read-only
        rate_down: float
        # Current rate up; read-only
        rate_up: float
        # Reference state
        ref_state: bool
        # Current state
        state: bool
        # MaBoSS Node "mutate" method
        def mutate(self, value: float) -> None

    # External variable value container
    class SymbolTable:
        # List of symbol names; read-only
        names: List[str]
        # Gets a symbol value by name
        def __getitem__(self, item: str) -> Union[bool, int, float]
        # Sets a symbol value by name
        def __setitem__(self, item: str, value: Union[bool, int, float]) -> None

    # Simulation network
    class Network:
        # List of nodes; read-only
        nodes: List[CC3DMaBoSSNode]
        # Symbol table; read-only
        symbol_table: SymbolTable

    # Simulation configuration
    class CC3DRunConfig:
        # Current random generator seed
        seed: int
        # Simulation time tick
        time_tick: float
        # Discrete time flag
        discrete_time: bool

    # The main MaBoSS simulation class in CC3D
    class CC3DMaBoSSEngine:
        # Network of the simulation; read-only
        network: Network
        # Configuration of the simulation; read-only
        run_config: CC3DRunConfig
        # Current simulation time; read-only
        time: float
        # Current default step size
        step_size: float
        # Integrates the simulation one step; passing no argument integrates over current value of step_size
        def step(self, _stepSize=-1.0) -> None
        # Gets the network state
        def getNetworkState(self) -> NetworkState
        # Loads an existing network state
        def loadNetworkState(self, _networkState: NetworkState) -> None
        # Get a node by node name
        def __getitem__(self, key: str) -> CC3DMaBoSSNode
        # Set a node state by node name
        def __setitem__(self, key: str, value: bool) -> None

The module ``cc3d.core.MaBoSSCC3D`` contains the following relevant API,

.. code-block:: python

    # Instantiates and returns a MaBoSS simulation instance from files and/or strings.
    def maboss_model(bnd_file: str = None,
                     bnd_str: str = None,
                     cfg_file: str = None,
                     cfg_str: str = None,
                     time_step: float = 1.0,
                     time_tick: float = 1.0,
                     discrete_time: bool = False,
                     seed: int = None,
                     istate: Dict[str, bool] = None) -> MaBoSSCC3DPy.CC3DMaBoSSEngine

The ``SteppableBasePy`` class contains the following relevant API,

.. code-block:: python

    class SteppableBasePy:
        # Adds a MaBoSS simulation instance to a cell
        @staticmethod
        def add_maboss_to_cell(cell: CellG,
                               model_name: str,
                               bnd_file: str = None,
                               bnd_str: str = None,
                               cfg_file: str = None,
                               cfg_str: str = None,
                               time_step: float = 1.0,
                               time_tick: float = 1.0,
                               discrete_time: bool = False,
                               seed: int = 0,
                               istate: Dict[str, bool] = None) -> None
        # Removes a MaBoSS simulation instance from a cell
        @staticmethod
        def delete_maboss_from_cell(cell: CellG, model_name: str) -> None
        # Instantiates and returns a MaBoSS simulation instance from files and/or strings.
        @staticmethod
        def maboss_model(bnd_file: str = None,
                         bnd_str: str = None,
                         cfg_file: str = None,
                         cfg_str: str = None,
                         time_step: float = 1.0,
                         time_tick: float = 1.0,
                         discrete_time: bool = False,
                         seed: int = 0,
                         istate: Dict[str, bool] = None) -> MaBoSSCC3DPy.CC3DMaBoSSEngine
        # Steps all existing MaBoSS simulations
        def timestep_maboss(self) -> None:
        # Returns a dictionary with summary statistics of a node of a model
        def maboss_stats(self, model_name: str, node_name: str) -> dict:

.. [1]
    Stoll, Gautier, et al. "MaBoSS 2.0: an environment for stochastic Boolean modeling." Bioinformatics 33.14 (2017): 2226-2228.
