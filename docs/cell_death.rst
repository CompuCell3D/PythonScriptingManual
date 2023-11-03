Cell Death
==============================

This guide covers apoptosis, necrosis, and phagocytosis. 


Death by Apoptosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each cell you want to kill, set its ``targetVolume`` to 0.
The cell will begin to shrink over time. 
You can make this happen faster by increasing ``lambdaVolume``.
Once the cell's volume is small enough, you should delete it with ``self.delete_cell(cell)``.


**Example step 1:** This example simulates apoptosis for B cells. In your main Steppable, write:

.. code-block:: python

    def step(self, mcs):
        for b_cell, common_surface_area in self.get_cell_neighbor_data_list(tfh_cell):
            if b_cell and b_cell.type == self.CENTROCYTE:
                b_cell.targetVolume = 0 #Starts apoptosis

**Example step 2:** Add this to your Main Python Script file. 
We use a separate Steppable to check for cell death only periodically (that is, every 100 MCS instead of every 1 step). 
This is __optional__, but it may provide a slight boost to performance.

.. code-block:: python

    from GerminalCenterMigrationSteppables import DeathSteppable

    CompuCellSetup.register_steppable(steppable=DeathSteppable(frequency=100))

**Example step 3:** Add a new Steppable to your Main Python Script file. 

.. code-block:: python

    class DeathSteppable(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):
            cells_to_delete = []        
            for cell in self.cell_list:
                if cell.volume < 2: #Replace '2' with any arbitrary small number
                    cells_to_delete.append(cell)
            
            for cell in cells_to_delete:
                self.delete_cell(cell)

.. note::

    It's important to use move all cells to delete to a new list, ``cells_to_delete``,
    so that a separate Python loop will make the calls to ``self.delete_cell(cell)``.
    This ensures that the first loop does not lose its place as it searches for dying cells.

Death by Necrosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many ways to achieve this, but one is to create a separate cell type, ``Necrotic``,
that has a very high target surface and lamda surface. Its volume can remain the same as before. 
This simulates the cell tearing apart, which, in real cells, 
creates a toxic environment for surviving neighobrs.
This time, there is no call to ``self.delete_cell(cell)`` so that the cell's detritus will remain there.

.. code-block:: xml

    <Plugin Name="Volume">
      <VolumeEnergyParameters CellType="Somatic" LambdaVolume="2.0" TargetVolume="50"/>
      <VolumeEnergyParameters CellType="Necrotic" LambdaVolume="2.0" TargetVolume="50"/>
   </Plugin>
   
   <Plugin Name="Surface">
      <SurfaceEnergyParameters CellType="Somatic" LambdaSurface="2.0" TargetSurface="50"/>
      <SurfaceEnergyParameters CellType="Necrotic" LambdaSurface="2.0" TargetSurface="200"/>
   </Plugin>

When you are ready to kill a cell, just change its type to ``NECROTIC``. In this example,
all cells die at Monte Carlo Step 100.

.. code-block:: python
    
    def step(self, mcs):
        if mcs == 100:
            for cell in self.cell_list:      
                cell.type = self.NECROTIC

Death by Phagocytosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This time, another cell will absorb the ``volume`` of the cell that dies.
Think of a macrophage eating a bacterium and becoming slightly larger. 

.. code-block:: python
    
    cells_to_delete = []
    for i, cell in enumerate(self.cell_list_by_type(self.MACROPHAGE)):
        for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):
            if neighbor and neighbor.type == self.BACTERIA:
                cell.targetVolume += neighbor.volume
                cell.targetSurface += 2 * sqrt(neighbor.volume) #Try to retain volume-to-surface ratio
                cells_to_delete.append(neighbor)
                
    for cell in cells_to_delete:
        self.delete_cell(cell)

.. note::

    As in apoptosis, it's important to use move all cells to delete to a new list, ``cells_to_delete``,
    so that a separate Python loop will make the calls to ``self.delete_cell(cell)``.
    This ensures that the first loop does not lose its place as it searches for dying cells.
