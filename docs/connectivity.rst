Connectivity Plugins
--------------------

The "basic" ``Connectivity`` plugin works **only in 2D and only on square
lattice** and is used to ensure that cells are connected or in other
words to prevent separation of the cell into pieces. The detailed
algorithm for this plugin is described in Roeland Merks' paper “Cell
elongation is a key to *in-silico* replication of in vitro
vasculogenesis and subsequent remodeling” Developmental Biology **289**
(2006) 44-54). There was one modification of the algorithm as compared
to the paper. Namely, to ensure proper connectivity we had to reject all
pixel copies that resulted in more that two collisions. (see the paper
for detailed explanation what this means).

The syntax of the plugin is straightforward:

.. code-block::

    <Plugin Name="Connectivity">
        <Penalty>100000</Penalty>
    </Plugin>

.. note::

    The value of ``Penalty`` is irrelevant because all ``Connectivity`` plugins
    have a special status. Namely, CC3D will call connectivity plugin to check if the a given pixel copy would
    lead to cell fragmentation and if so it will reject the pixel copy without computing
    energy-based pixel-copy acceptance function. thus the only thing that matters here is that
    penalty parameter is a positive number. Any number


As we mentioned, earlier 2D connectivity algorithm is particularly fast but works only
on Cartesian lattice nad in 2D only. If you are on hex lattice or are working with 3 dimensions
You should use ``ConnectivityGlobal`` plugin and there specify so called ``FastAlgorithm`` to get
decent performance.

For example (see *Demos/PluginDemos/connectivity_global_fast*):

.. code-block:: xml

    <Plugin Name="ConnectivityGlobal">
        <FastAlgorithm/>
        <ConnectivityOn Type="NonCondensing"/>
        <ConnectivityOn Type="Condensing"/>
    </Plugin>

will enforce connectivity of cells of type ``Condensing`` and ``NonCondensing`` and will use "fast algorithm".

If  you want to enforce connectivity for individual cells cells (see *Demos/PluginDemos/connectivity_elongation_fast*)
you would use the following CC3DML code:


.. code-block:: xml

    <Plugin Name="ConnectivityGlobal">
        <FastAlgorithm/>
    </Plugin>


and couple it with the following Python steppable:

.. code-block:: python

    class ConnectivityElongationSteppable(SteppableBasePy):
        def __init__(self,_simulator,_frequency=10):
            SteppableBasePy.__init__(self,_simulator,_frequency)

        def start(self):
            for cell in self.cellList:
                if cell.type==1:
                    cell.connectivityOn = True

                elif cell.type==2:
                    cell.connectivityOn = True

Below we describe a slower version of ConnectivityGlobal plugin that is still supported but
has much slower performance and for that reason we encourage you to try faster implementation described above

 .. note::

    **DEPRECATED**

    A more general type of connectivity constraint is implemented in
    ``ConnectivityGlobal`` plugin. In this case we calculate volume of a cell
    using breadth first search algorithm and compare it with actual volume
    of the cell. If they agree we conclude that cell connectivity is
    preserved. This plugin works both in 2D and 3D and on either type of
    lattice. However, the computational cost of running such algorithm can
    be quite high so it is best to limit this plugin to cell types for which
    connectivity of cell is really essential:

    .. code-block:: xml

        <Plugin Name="ConnectivityGlobal">
            <Penalty Type="Body1">1000000000</Penalty>
        </Plugin>

    As we mentioned before the actual value of ``Penalty`` parameter does not matter as long it is a positive number

    In certain types of simulation it may happen that at some point cells
    change cell types. If a cell that was not subject to connectivity
    constraint, changes type to the cell that is constrained by global
    connectivity and this cell is fragmented before type change this
    situation normally would result in simulation freeze. However,
    CompuCell3D, first before applying constraint it will check if the cell
    is fragmented. If it is, there is no constraint. Global connectivity
    constraint is only applied when cell is non-fragmented.

    Quite often in the simulation we don't need to impose connectivity
    constraint on all cells or on all cells of given type. Usually only
    select cell types or select cells are elongated and therefore need
    connectivity constraint. In such a case we simply declare ``ConnectivityGlobal`` with no further specifications
    taking place in CC3DML
    The actual connectivity assignments to particular cells take place in Python

    In CC3DML we only declare:

    .. code-block:: xml

        <Plugin Name="ConnectivityGlobal"/>

    In Python we manipulate/access connectivity parameters for individual
    cells using the following syntax:

    .. code-block:: python

        class ElongationFlexSteppable(SteppableBasePy):
            def __init__(self,_simulator,_frequency=10):
                SteppableBasePy.__init__(self, _simulator, _frequency)
                # self.lengthConstraintPlugin=CompuCell.getLengthConstraintPlugin()


            def start(self):
                pass

            def step(self,mcs):
                for cell in self.cellList:
                    if cell.type==1:
                        self.lengthConstraintPlugin.setLengthConstraintData(cell,20,20) # cell , lambdaLength, targetLength
                        self.connectivityGlobalPlugin.setConnectivityStrength(cell,10000000) #cell, strength

                    elif cell.type==2:
                        self.lengthConstraintPlugin.setLengthConstraintData(cell,20,30)  # cell , lambdaLength, targetLength
                        self.connectivityGlobalPlugin.setConnectivityStrength(cell,10000000) #cell, strength

    See also example in *Demos/PluginDemos/elongationFlexTest.*

    If you are in 2D and on Cartesian lattice you may instead use ``ConnectivityLocalFlex``

    In this case

    In CC3DML we only declare:

    .. code-block:: xml

        <Plugin Name="ConnectivityLocalFlex"/>

    and in Python:

    .. code-block:: python

        self.connectivityLocalFlexPlugin.setConnectivityStrength(cell,20.7)
        self.connectivityLocalFlexPlugin.getConnectivityStrength(cell)

