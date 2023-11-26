PIFDumper Steppable
-------------------

This steppable does the opposite to ``PIFIitialize``r – it writes PIF file
of current lattice configuration. The syntax similar to the syntax of
``PIFInitializer``:

.. code-block:: xml

    <Steppable Type="PIFDumper" Frequency=”100”>
        <PIFName>line</PIFName>
    </Steppable>

Notice that we used ``Frequency`` attribute of steppable to ensure that PIF
files are written every ``100`` MCS. Without it they would be written every
MCS. The file names will have the following format: ``PIFName.MCS.pif``

In our case they would be ``line.0.pif``, ``line.100.pif``, ``line.200.pif``, etc...

This module is actually quite useful. For example, if we want to start
simulation from a more configuration of cells (not rectangular cells as
this is the case when we use ``Uniform`` or ``Blob`` initializers). In such a
case we would run a simulation with a ``PIFDumper`` included and once the
cell configuration reaches desired shape we would stop and use PIF file
corresponding to this state. Once we have PIF initial configuration we
may run many simulation starting from the same, realistic initial
condition.

.. tip::

    Restarting simulation from a given configuration is actually even easier in the recent
    versions of CC3D. All you have to do is to create .``cc3d`` project where you add serialization optyion
    CC3D will be savbing complete snapshots of the simulation (including PIF files) and you can easily restart
    the simulation from a given end-point of the previous run. For more details see "Python Scripting Manual"
    https://pythonscriptingmanual.readthedocs.io/en/latest/restarting_simulations.html?highlight=restart


.. tip::

    You can also generate PIF file from the current simulation
    snapshot by using Player tool: Tools->Generate PIF file from current
    snapshot…