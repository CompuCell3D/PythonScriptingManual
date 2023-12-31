CellType Plugin
---------------

An example of the plugin that stores user assigned data that is used to
configure simulation before it is run is a ``CellType Plugin``. This plugin
is responsible for defining cell types and storing cell type
information. It is a basic plugin used by virtually every CompuCell
simulation. The syntax is straight forward as can be seen in the example
below:

.. code-block:: xml

    <Plugin Name="CellType">
      <CellType TypeName="Medium" TypeId="0"/>
      <CellType TypeName="Fluid" TypeId="1"/>
      <CellType TypeName="Wall" TypeId="2" Freeze=""/>
    </Plugin>


Here we have defined three cell types that will be present in the
simulation: ``Medium``, ``Fluid``, ``Wall``. Notice that we assign a number – ``TypeId``
– to every cell type. It is strongly recommended that ``TypeId``’s are
consecutive positive integers (e.g. ``0,1,2,3...``). ``Medium`` is traditionally
given ``TypeId=0`` and we recommend that you keep this convention.

.. note::

    **Important:** Every CC3D simulation must define ``CellType Plugin`` and
    include at least ``Medium`` specification.

Notice that in the example above cell type ``Wall`` has extra attribute
``Freeze=""``. This attribute tells CompuCell that cells of **frozen** type
will not be altered by pixel copies. Freezing certain cell types is a
very useful technique in constructing different geometries for
simulations or for restricting ways in which cells can move.