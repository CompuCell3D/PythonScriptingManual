AdhesionFlex Plugin
-------------------

``AdhesionFlex`` offers a very flexible way to define adhesion between cells. It
allows setting individual adhesivity properties for each cell. Users can
use either CC3DML syntax or Python scripting to initialize adhesion
molecule density for each cell. In addition, ``Medium`` can also carry its
own adhesion molecules. We use the following formula to calculate
adhesion energy in ``AdhesionFlex`` plugin:

.. math::
    :nowrap:

    \begin{eqnarray}
        E_{adhesion} = \sum_{i,j,neighbors} \left ( - \sum_{m,n}k_{mn}F\left ( N_{m}\left (i \right ), N_{n} \left( j \right ) \right ) \right )\left ( 1-\delta_{\sigma(i), \sigma(j)} \right )
    \end{eqnarray}


where indexes ``i``, ``j`` label pixels, :math:`- \sum_{m,n}k_{mn}F\left ( N_{m}\left (i \right ), N_{n} \left( j \right ) \right )`
denotes contact energy between cell types :math:`\sigma(i)` and :math:`\sigma(j)` and indexes ``m`` , ``n``
label adhesion molecules in cells composed of pixels ``i`` and ``j`` respectively. ``F``
denotes user-defined function of :math:`N_m` and :math:`N_n`.
Although this may look a bit complex, the basic idea is simple: each
cell has certain number of adhesion molecules on its surface. When cells touch
each other the resultant energy is simply a "product of interactions" of
adhesion molecules from one cell with adhesion molecules from another cell. The CC3DML
syntax for this plugin is given below:

.. code-block:: xml

    <Plugin Name="AdhesionFlex">
        <AdhesionMolecule Molecule="NCad"/>
        <AdhesionMolecule Molecule="NCam"/>
        <AdhesionMolecule Molecule="Int"/>
        <AdhesionMoleculeDensity CellType="Cell1" Molecule="NCad" Density="6.1"/>
        <AdhesionMoleculeDensity CellType="Cell1" Molecule="NCam" Density="4.1"/>
        <AdhesionMoleculeDensity CellType="Cell1" Molecule="Int" Density="8.1"/>
        <AdhesionMoleculeDensity CellType="Medium" Molecule="Int" Density="3.1"/>
        <AdhesionMoleculeDensity CellType="Cell2" Molecule="NCad" Density="2.1"/>
        <AdhesionMoleculeDensity CellType="Cell2" Molecule="NCam" Density="3.1"/>

        <BindingFormula Name="Binary">
            <Formula> min(Molecule1,Molecule2)</Formula>
            <Variables>
                <AdhesionInteractionMatrix>
                 <BindingParameter Molecule1="NCad" Molecule2="NCad">-1.0</BindingParameter>
                 <BindingParameter Molecule1="NCam" Molecule2="NCam">2.0</BindingParameter>
                 <BindingParameter Molecule1="NCad" Molecule2="NCam">-10.0</BindingParameter>
                 <BindingParameter Molecule1="Int" Molecule2="Int">-10.0</BindingParameter>
                </AdhesionInteractionMatrix>
            </Variables>
        </BindingFormula>

        <NeighborOrder>2</NeighborOrder>
    </Plugin>


:math:`k_{mn}` matrix is specified within the ``AdhesionInteractionMatrix``
tag – the elements are listed using ``BindingParameter`` tags. The
``AdhesionMoleculeDensity`` tag specifies initial concentration of adhesion
molecules. Even if you are going to modify those from Python you are still required to specify the
names of adhesion molecules and associate them with appropriate cell
types. Failure to do so may result in simulation crash or undefined
behaviors. The user-defined function ``*F*`` is specified using ``Formula`` tag
where the arguments of the function are called ``Molecule1`` and ``Molecule2`` .
The syntax has to follow syntax of the muParser -
https://beltoforion.de/en/muparser/features.php#idDef1 .

.. note::

    Using more complex formulas with muParser requires special ``CDATA`` syntax. Please check :doc:`mu_parser` for more details.

CompuCell3D example – *Demos/AdhesionFlex* - demonstrates how to
manipulate concentration of adhesion molecules. For example:

.. code-block:: python

    self.adhesionFlexPlugin.getAdhesionMoleculeDensity(cell,"NCad")

allows to access adhesion molecule concentration using its name (as
given in the CC3DML above using ``AdhesionMoleculeDensity`` tag).


.. code-block:: python

    self.adhesionFlexPlugin.getAdhesionMoleculeDensityByIndex(cell,1)

allows to access adhesion molecule concentration using its index in the
adhesion molecule density vector. The order of the adhesion molecule
densities in the vector is the same as the order in which they were
declared in the CC3DML above - AdhesionMoleculeDensity tags.

.. code-block:: python

    self.adhesionFlexPlugin.getAdhesionMoleculeDensityVector(cell)

allows access to entire adhesion molecule density vector. Each of these functions has
its corresponding function which operates on
``Medium`` .  In this case we do not give cell as first argument:

.. code-block:: python

    self.adhesionFlexPlugin.getMediumAdhesionMoleculeDensity('Int')

    self.adhesionFlexPlugin.getMediumAdhesionMoleculeDensityByIndex (0)

    self.adhesionFlexPlugin.getMediumAdhesionMoleculeDensityVector(cell)

To change the value of the adhesion molecule density we use set
functions:

.. code-block:: python

    self.adhesionFlexPlugin.setAdhesionMoleculeDensity(cell,'NCad',0.1)

    self.adhesionFlexPlugin.setAdhesionMoleculeDensityByIndex(cell,1,1.02)

    self.adhesionFlexPlugin.setAdhesionMoleculeDensityVector(cell,[3.4,2.1,12.1])

Notice that in this last function we passed entire Python list as the
argument. CC3D will check if the number of entries in this vector is the
same as the number of entries in the currently used vector. If so the
values from the passed vector will be copied, otherwise they will be
**ignored**.

.. note::

    During mitosis we create new cell (``childCell``) and the
    adhesion molecule vector of this cell will have no components. However
    in order for simulation to continue we have to initialize this vector
    with number of adhesion molecules appropriate to ``childCell`` type. We know that
    ``setAdhesionMoleculeDensityVector`` is not appropriate for this task so we
    have to use:

    .. code-block:: python

        self.adhesionFlexPlugin.assignNewAdhesionMoleculeDensityVector(cell,[3.4,2.1,12.1])

    which will ensure that the content of passed vector is copied entirely
    into cell’s vector (making size adjustments as necessary).

.. note::

    You have to make sure that the number of newly assigned
    adhesion molecules is exactly the same as the number of adhesion
    molecules declared for the cell of this particular type.

All of the ``get`` functions has corresponding set function which operates on
``Medium``:

.. code-block:: python

    self.adhesionFlexPlugin.setMediumAdhesionMoleculeDensity("NCam",2.8)

    self.adhesionFlexPlugin.setMediumAdhesionMoleculeDensityByIndex(2,16.8)

    self.adhesionFlexPlugin.setMediumAdhesionMoleculeDensityVector([1.4,3.1,18.1])

    self.adhesionFlexPlugin.assignNewMediumAdhesionMoleculeDensityVector([1.4,3.1,18.1])
