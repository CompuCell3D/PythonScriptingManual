VolumeFlex Plugin
-----------------

``VolumeFlex`` plugin is more sophisticated version of ``Volume`` Plugin. While
``Volume`` Plugin treats all cell types the same i.e. they all have the same
target volume and lambda coefficient, ``VolumeFlex`` plugin allows you to
assign different lambda and different target volume to different cell
types. The syntax for this plugin is straightforward and essentially
mimics the example below.

.. code-block:: xml

    <Plugin Name="Volume">
        <VolumeEnergyParameters CellType="Prestalk" TargetVolume="68" LambdaVolume="15"/>
        <VolumeEnergyParameters CellType="Prespore" TargetVolume="69" LambdaVolume="12"/>
        <VolumeEnergyParameters CellType="Autocycling" TargetVolume="80" LambdaVolume="10"/>
        <VolumeEnergyParameters CellType="Ground" TargetVolume="0" LambdaVolume="0"/>
        <VolumeEnergyParameters CellType="Wall" TargetVolume="0" LambdaVolume="0"/>
    </Plugin>

.. note::

    Almost all CompuCell3D modules which have options ``Flex`` or
    ``LocalFlex`` are implemented as a single C++ module and CC3D, based on
    CC3DML syntax used, figures out which functionality to load at the run
    time. As a result for the reminder of this reference manual we will
    stick to the convention that all ``Flex`` and ``LocalFlex`` modules will be
    invoked using core name of the module only.

Notice that in the example above cell types ``Wall`` and ``Ground`` have target
volume and coefficient lambda set to 0 – very unusual. That's because in
this particular case those cells are frozen so the parameters specified
for these cells do not matter. In fact it is safe to remove
specifications for these cell types, but just for the illustration
purposes we left them here.

Using ``VolumeFlex`` Plugin you can effectively freeze certain cell types.
All you need to do is to put very high lambda coefficient for the cell
type you wish to freeze. You have to be careful though , because if
initial volume of the cell of a given type is different from target
volume for this cell type the cells will either shrink or expand to
match target volume and only after this initial volume adjustment will
they remain frozen provided ``LambdaVolume`` is high enough. Since rapid
changes in the cell volume are uncontrolled (e.g. they can destroy many
neighboring cells) you should opt for more gradual changes. In any case,
we do not recommend this way of freezing cells because it is difficult
to use, and also not efficient in terms of speed of simulation run.

SurfaceFlex Plugin
------------------

``SurfaceFlex`` plugin is more sophisticated version of ``Surface`` Plugin.
Everything that was said with respect to ``VolumeFlex`` plugin applies to
``SurfaceFlex``. For syntax see example below:

.. code-block:: xml

    <Plugin Name="Surface">
        <SurfaceEnergyParameters CellType="Prestalk" TargetSurface="90" LambdaSurface="0.15"/>
        <SurfaceEnergyParameters CellType="Prespore" TargetSurface="98" LambdaSurface="0.15"/>
        <SurfaceEnergyParameters CellType="Autocycling" TargetSurface="92" LambdaSurface="0.1"/>
        <SurfaceEnergyParameters CellType="Ground" TargetSurface="0" LambdaSurface="0"/>
        <SurfaceEnergyParameters CellType="Wall" TargetSurface="0" LambdaSurface="0"/>
    </Plugin>

VolumeLocalFlex Plugin
----------------------

``VolumeLocalFlex`` Plugin is very similar to ``Volume`` plugin. however this time
you specify lambda coefficient and target volume, individually for each cell.
In the course of
simulation you can change this target volume depending on e.g.
concentration of *e.g.* ``FGF``in the particular cell. This way you can specify
which cells grow faster, which slower based on a state of the
simulation. This plugin requires you to develop a module (plugin or
steppable) which will alter target volume for each cell. You can do it
either in C++ or even better in Python.

Example syntax:

.. code-block:: xml

    <Plugin Name="Volume"/>

SurfaceLocalFlex Plugin
-----------------------

This plugin is analogous to ``VolumeLocalFlex`` but operates on cell
surface.

Example syntax:

.. code-block:: xml

    <Plugin Name="Surface"/>
