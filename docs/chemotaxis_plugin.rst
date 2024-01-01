Chemotaxis
----------

``Chemotaxis`` plugin, is used to simulate the chemotaxis
of cells. Put simply, a cell will follow the highest concentration of a chemical field. 
Note that a cell can only move towards or away from a 
chemical field if it can detect any concentration above 0 at its surface. 
The cell cannot "see" far away to know where to move. 

Related: `Chemotaxis Examples in Python <chemotaxis_on_a_cell-by-cell_basis.html>`_.

Properties
****************************

Assume ``self`` is an instance of SteppableBasePy.

**self.chemotaxisPlugin.addChemotaxisData(cell, fieldName: string)**: adds a chemotaxis behavior that will cause the given ``cell`` 
to respond to the chemical field specified by ``fieldName``. 
``fieldName`` must match the name of the chemical field exactly.  
Returns a chemotaxis data object, which has the following methods: 

    - **chemotaxisData.setLambda(lambda: float)**: assigns the lambda of the given chemotaxis behavior, which controls the intensity of the chemotaxis 
    (see definition below).

    - **chemotaxisData.assignChemotactTowardsVectorTypes([cellType1, cellType2, ...])**: causes chemotaxis to trigger when the cell touches
    one or more of the other cell types in the provided list.

    - **chemotaxisData.setLogScaledCoef(coef: float)**: assign the log-scaled
    coefficient of the given chemotaxis behavior, which helps to mitigate 
    excessive orders of magnitude in chemotaxis decisions (see definition below).

**self.chemotaxisPlugin.getChemotaxisData(cell, fieldName: string)**: finds a chemotaxis behavior that is already assigned to the ``cell`` and returns it. 
``fieldName`` must match the name of the chemical field exactly. 

****************************


How It Works
***************************

For every pixel copy, this plugin calculates the change of energy
associated with the pixel move. There are several methods to define a change
in energy due to chemotaxis. By default, we define a chemotaxis using the
following formula:

.. math::
   :nowrap:

   \begin{eqnarray}
        \Delta E_{chem} = -\lambda\left ( c(x_{destination}) - c(x_{source}) \right )
   \end{eqnarray}


where :math:`c(x_{source})` and :math:`c(x_{destination})` denote chemical concentration at
the pixel-copy-source and pixel-copy-destination pixel, respectively.

The body of the ``Chemotaxis`` plugin description contains sections called
``ChemicalField``. In this section, we tell CompuCell3D which module contains
a chemical field that we wish to use for chemotaxis. In our case it is
``FlexibleDiffusionSolverFE``. Next, we specify the name of the field - ``FGF``.
Subsequently, we specify ``lambda`` for each cell type so that cells of
different types may respond differently to a given chemical. In
particular, types not listed will not respond to chemotaxis at all.

**Lambda**: Controls how quickly a cell will move in response to a chemical field. 
More precisely, it affects the *decision* of whether or not a cell's pixel will be copied so that the cell can move.
If a cell has multiple chemicals that it is exposed to, it is more inclined to move towards the field that its lambda is higher for. 
If lambda is positive, the cell will move toward the field. 
Conversely, if it is negative, the cell will move away.
Note that the *absolute value* controls the intensity, 
so -100 and +100 will each have a similar effect on the cell.

****************************

Occasionally, we may want to use a different formula for the chemotaxis
than the one presented above. The current version of CompCell3D supports the
following definitions of change in chemotaxis energy (``Saturation`` and
``SaturationLinear`` respectively ):

.. math::
   :nowrap:

   \begin{eqnarray}
       \Delta E_{chem} = -\lambda \left [ \frac{c(x_{destination})}{s+c(x_{destination})} - \frac{c(x_{source})}{s+c(x_{source})} \right ]
   \end{eqnarray}

or

.. math::
   :nowrap:

   \begin{eqnarray}
       \Delta E_{chem} = -\lambda \left [ \frac{c(x_{destination})}{sc(x_{destination})+1} - \frac{c(x_{source})}{sc(x_{source})+1} \right ]
   \end{eqnarray}


where ``s`` denotes saturation constant. To use the first of the above
formulas, we set the value of the saturation coefficient:

.. code-block:: xml

    <Plugin Name="Chemotaxis">
       <ChemicalField Source="FlexibleDiffusionSolverFE" Name="FGF">
            <ChemotaxisByType Type="Amoeba" Lambda="0"/>
            <ChemotaxisByType Type="Bacteria" Lambda="2000000" SaturationCoef="1"/>
       </ChemicalField>
    </Plugin>


Notice that this only requires a small change in line where you previously
specified only lambda.

.. code-block:: xml

    <ChemotaxisByType Type="Bacteria" Lambda="2000000" SaturationCoef="1"/>


To use the second of the above formulas use ``SaturationLinearCoef`` instead of
``SaturationCoef``:

.. code-block:: xml

    <Plugin Name="Chemotaxis">
       <ChemicalField Source="FlexibleDiffusionSolverFE" Name="FGF">
          <ChemotaxisByType Type="Amoeba" Lambda="0"/>
         <ChemotaxisByType Type="Bacteria" Lambda="2000000" SaturationLinearCoef="1"/>
       </ChemicalField>
    </Plugin>

The ``lambda`` value specified for each cell type can also be scaled using the
``LogScaled`` formula according to the concentration of the field at the center of mass of the
chemotaxing cell :math:`c_{CM}`,

.. math::
    :nowrap:

    \begin{eqnarray}
        \Delta E_{chem} = -\frac{\lambda}{s + c_{CM}} \left ( c(x_{destination}) - c(x_{source}) \right )
    \end{eqnarray}

The ``LogScaled`` formula is commonly used to mitigate excessive forces on cells
in fields that vary over several orders of magnitude, and can be selected
by setting the value of :math:`s` with the attribute `LogScaledCoef` like as follows,

.. code-block:: xml

    <ChemotaxisByType Type="Amoeba" Lambda="100" LogScaledCoef="1"/>

Sometimes it is desirable to have chemotaxis **at the interface
between** only certain types of cells **and not between** other
cell-type-pairs. In such a case we augment ``ChemotaxisByType`` element with
the following attribute:

.. code-block:: xml

    <ChemotaxisByType Type="Amoeba" Lambda="100 "ChemotactTowards="Medium"/>


This will cause the change in chemotaxis energy to be non-zero
only for those pixel copy attempts that happen between pixels belonging
to ``Amoeba`` and ``Medium``. 
Essentially, the amoeba will follow the highest concentration of the medium it can find.

.. note::

    The term ``ChemotactTowards`` means "chemotax at the interface between"

CC3D supports slight modifications of the above formulas in the
``Chemotaxis`` plugin where :math:`\Delta E` is non-zero only if the cell located at :math:`x_{source}` *after*
the pixel copy is non-medium. To enable this mode users need to include

.. code-block:: XML

    <Algorithm="Regular"/>

tag in the body of CC3DML plugin.
Additionally, ``Chemotaxis`` plugin can apply the above formulas using the parameters
and formulas of both the cell located at :math:`x_{source}` (if any) `and` the cell located
at :math:`x_{destination}` (if any). To enable this mode users need to include

.. code-block:: xml

    <Algorithm="Reciprocated"/>


Let's look at the syntax by studying the example usage of the Chemotaxis
plugin:

.. code-block:: xml

    <Plugin Name="Chemotaxis">
       <ChemicalField Source="FlexibleDiffusionSolverFE" Name="FGF">
            <ChemotaxisByType Type="Amoeba" Lambda="300"/>
            <ChemotaxisByType Type="Bacteria" Lambda="200"/>
       </ChemicalField>
    </Plugin>

The definitions of chemotaxis presented so far do not allow
specification of chemotaxis parameters individually for each cell. To do
this we will use Python scripting. We still need to specify in the
CC3DML which fields are important from chamotaxis stand point. Only
fields listed in the CC3DML will be used to calculate chemotaxis energy:

.. code-block:: xml

    …

    <Plugin Name="CellType">
        <CellType TypeName="Medium" TypeId="0"/>
        <CellType TypeName="Bacterium" TypeId="1" />
        <CellType TypeName="Macrophage" TypeId="2"/>
        <CellType TypeName="Wall" TypeId="3" Freeze=""/>
    </Plugin>

    …

    <Plugin Name="Chemotaxis">
        <ChemicalField Source="FlexibleDiffusionSolverFE" Name="ATTR">
        <ChemotaxisByType Type="Macrophage" Lambda="20"/>
        </ChemicalField>
    </Plugin>

    …


In the above excerpt from the CC3DML configuration file, we see that
cells of type ``Macrophage`` will chemotax in response to ``ATTR`` gradient.

Using Python scripting we can modify the chemotaxis properties of individual
cells as follows:


.. code-block:: python

   class ChemotaxisSteering(SteppableBasePy):
           def __init__(self, _simulator, _frequency=100):
               SteppableBasePy.__init__(self, _simulator, _frequency)

           def start(self):

               for cell in self.cellList:
                   if cell.type == self.cell_type.Macrophage:
                       cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ATTR")
                       cd.setLambda(20.0)
                       cd.assignChemotactTowardsVectorTypes([self.cell_type.Medium, self.cell_type.Bacterium])
                       break

           def step(self, mcs):
               for cell in self.cellList:
                   if cell.type == self.cell_type.Macrophage:
                       cd = self.chemotaxisPlugin.getChemotaxisData(cell, "ATTR")
                       if cd:
                           lam = cd.getLambda() - 3
                           cd.setLambda(lam)
                       break

In the ``start`` function for the first encountered cell of type ``Macrophage``
(``type==self.cell_type.Macrophage``), we insert a ``ChemotaxisData`` object (it determines chemotaxing
properties) and initialize ``λ`` parameter to ``20``. 
We also initialize a vector of cell types towards which Macrophage cells will chemotax 
(it will chemotax towards Medium and Bacterium cells). Notice the break statement inside the if statement, inside the loop. It ensures that only first
encountered Macrophage cell will have chemotaxing properties altered.

In the step function we decrease lambda chemotaxis by ``3`` units every ``100``
MCS. In effect we turn a cell from chemotaxing up ``ATTR`` gradient to being
chemorepelled.

In the above example we have more than one macrophage but only one of
them has altered chemotaxing properties. The other macrophages have
chemotaxing properties set in the CC3DML section. CompuCell3D first
checks if local definitions of chemotaxis are available (i.e. for
individual cells) and if so it uses those. Otherwise it will use
definitions from from the CC3DML.

The ``ChemotaxisData`` structure has additional functions which allow to set
chemotaxis formula used. For example we may type:

.. code-block:: python

    def start(self):
        for cell in self.cellList:
            if cell.type == self.cell_type.Macrophage:
                cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ATTR")
                cd.setLambda(20.0)
                cd.setSaturationCoef(200.0)
                cd.assignChemotactTowardsVectorTypes([self.cell_type.Medium, self.cell_type.Bacterium])
                break


to activate ``Saturation`` formula. To activate ``SaturationLinear`` formula we
would use:

.. code-block:: python

    cd.setSaturationLinearCoef(2.0)

To activate the ``LogScaled`` formula for a cell, we would use:

.. code-block:: python

    cd.setLogScaledCoef(3.0)

.. warning::

    When you use chemotaxis plugin you have to make sure that
    fields that you refer to and module that contains this fields are
    declared in the CC3DML file. Otherwise you will most likely cause either
    program crash (which is not as bad as it sounds) or unpredicted behavior
    (much worse scenario, although unlikely as we made sure that in the case
    of undefined symbols, CompuCell3D exits)
