Chemotaxis on a cell-by-cell basis
==================================

Just like the secretion is typically defined for cell types the same
applies to chemotaxis. And similarly as in the case of the secretion
there is an easy way to implement chemotaxis on a cell-by-cell basis.
You can find relevant example in ``Demos/PluginDemos/chemotaxis_by_cell_id``.
 Let us look at the code:

.. code-block:: python

    class ChemotaxisSteering(SteppableBasePy):
        def __init__(self, _simulator, _frequency=100):
            SteppableBasePy.__init__(self, _simulator, _frequency)

        def start(self):

            for cell in self.cellList:
                if cell.type == self.MACROPHAGE:
                    cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ATTR")
                    cd.setLambda(30.0)
                    cd.assignChemotactTowardsVectorTypes([self.MEDIUM, self.BACTERIUM])
                    break

        def step(self, mcs):
            if mcs > 100 and not mcs % 100:
                for cell in self.cellList:
                    if cell.type == self.MACROPHAGE:

                        cd = self.chemotaxisPlugin.getChemotaxisData(cell, "ATTR")
                        if cd:
                            lm = cd.getLambda() - 3
                            cd.setLambda(lm)
                        break

Before we start analyzing this code let’s look at CC3DML declaration of
the chemotaxis plugin:

.. code-block:: xml

    <Plugin Name="Chemotaxis">
       <ChemicalField Source="FlexibleDiffusionSolverFE" Name="ATTR">
    <!--     <ChemotaxisByType Type="Macrophage" Lambda="20"/>   	 -->
       </ChemicalField>
     </Plugin>


As you can see we have commented out ``ChemotaxisByType`` but leaving
information about fields so that chemotaxis plugin can fetch pointers to
the fields. Clearly leaving such definition of chemotaxis in the CC3DML
would have no effect on the simulation. However, as you can see in the
Python steppable code we define chemotaxis on a cell-by-cell basis.We
loop over all cells and when we encounter cell of type Macrophage we
assign to it object called ``ChemotaxisData`` (we use
``self.chemotaxisPlugin.addChemotaxisData`` function to do that).
ChemotaxisData object allows definition of all chemotaxis properties
available via CC3DML but here we apply them to single cells. In our
example code we set lambda describing chemotaxis strength and cells
types that don’t inhibit chemotaxis by touching our cell (in other
words, cell experiences chemotaxis when it touches cell types listed in
assignChemotactTowardsVectorTypes function).

Notice ``break`` instruction at the end of the loop. It ensures that the for
loop that iterates over all cells stops after it encounters first cell
of type ``Macrophage``.

In the step function iterate through all cells and search for first
occurrence of Macrophage cell (``break`` instruction at the end of this
function will ensure it). This time however, instead of adding
chemotaxis data we fetch ``ChemotaxisData`` object associated with a cell.
We extract lambda and decrease it by 3 units. The net result of several
operations like that is that lambda chemotaxis will go from positive
number to negative number and cell that initially chemotaxed up the
concentration gradient, now will start moving away from the source of
the chemical.

When you want to implement chemotaxis using alternative calculations
with saturation terms all you need to do is to add cd.setSaturationCoef
function call to enable type of chemotaxis that corresponds in the
CC3DML to the following call:

.. code-block:: xml

    <ChemotaxisByType ChemotactTowards="CELL_TYPES" Lambda="1.0" SaturationCoef="100.0" Type="CHEMOTAXING_TYPE"/>

The Python code would look like:

.. code-block:: python

    for cell in self.cellList:
        if cell.type == self.MACROPHAGE:
            cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ATTR")
            cd.setLambda(30.0)
            cd.setSaturationCoef(100)
            cd.assignChemotactTowardsVectorTypes([self.MEDIUM, self.BACTERIUM])

If we want to replicate the following CC3DML version of chemotaxis for a
single cell:

.. code-block:: xml

    <ChemotaxisByType ChemotactTowards="CELL_TYPES" Lambda="1.0" SaturationLinearCoef="10.1" Type="CHEMOTAXING_TYPE"/>

we would use the following Python snippet:

.. code-block:: python

    for cell in self.cellList:
        if cell.type == self.MACROPHAGE:
            cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ATTR")
            cd.setLambda(30.0)
            cd.setSaturationLinearCoef(100)
            cd.assignChemotactTowardsVectorTypes([self.MEDIUM, self.BACTERIUM])

