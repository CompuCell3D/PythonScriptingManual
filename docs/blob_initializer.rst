BlobInitializer Steppable
-------------------------

``BlobInitializer`` steppable is used to lay out circular blob of cells on the lattice.

An example syntax where we create one circular region of cells in the lattice is presented below:

.. code-block:: xml

    <Steppable Type="BlobInitializer">
       <Region>
         <Gap>0</Gap>
         <Width>5</Width>
         <Radius>40</Radius>
         <Center x="100" y="100" z="0"/>
         <Types>Condensing,NonCondensing</Types>
       </Region>
    </Steppable>

Similarly as for the ``UniformFieldInitializer`` users can define many
regions each of which is a blob of a particular center point, radius and
list of cell types that will be assigned to cells forming the blob.
Listing types in the ``<Types>`` tag follows same rules as in the
UniformInitializer.

.. note::

    Original (**and deprecated**) syntax of this plugin looks as follows:

    .. code-block:: xml

        <Steppable Type="BlobInitializer">
            <Gap>0</Gap>
            <Width>5</Width>
            <CellSortInit>yes</CellSortInit>
            <Radius>40</Radius>
        </Steppable>


    The blob is centered in the middle of th lattice and has radius given by
    ``<Radius>`` parameter. All cells are initially squares (or cubes in 3D) where
    ``<Width>`` determines the length of the cube or square side and ``<Gap>``
    determines space between squares or cubes. ``<CellSortInit>`` tag and value
    ``yes`` is used to initialize cells randomly with type id being either ``1`` or
    ``2`` . Otherwise all cells will have type id ``1``. This can be easily modified
    in Python .
