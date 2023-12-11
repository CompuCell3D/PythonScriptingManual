Cell Death
==============================

This guide covers suggested apoptosis, necrosis, and phagocytosis. 


Death by Apoptosis
************************************************

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
                b_cell.lambdaVolume = 1000 #Optional: make the shrinkage happen very fast

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
************************************************

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
************************************************

This time, another cell will absorb the ``volume`` of the cell that dies.
Think of a macrophage eating a bacterium and becoming slightly larger. 
This code checks every bacteria cell to see if its only neighbors are macrophage(s).

.. code-block:: python
    
    def step(self, mcs):
        cells_to_delete = []
        for i, bacteria in enumerate(self.cell_list_by_type(self.BACTERIA)):
            is_only_touching_macrophage = True
            macrophage = None
            for neighbor, common_surface_area in self.get_cell_neighbor_data_list(bacteria):
                if neighbor:
                    if neighbor.type == self.MACROPHAGE:
                        macrophage = neighbor
                    else:
                       is_only_touching_macrophage = False
            
            if is_only_touching_macrophage and macrophage != None:
                #Now, the macrophage eats the bacteria.
                macrophage.targetVolume += bacteria.volume
                macrophage.targetSurface += 2 * sqrt(bacteria.volume) #Try to retain volume-to-surface ratio
                cells_to_delete.append(bacteria)
                    
        for cell in cells_to_delete:
            self.delete_cell(cell)


Alternative Approach 1: You could also check the length of ``cell_list_by_type`` to see if it is 1,
but that would prevent phagocytosis from happening if the cell is touching any of the Medium.

Alternative Approach 2: Since ``common_surface_area`` is not used in this example, CC3D has no way
to know if one cell is inside of another. You could check the shared surface area against each cell's current surface.

.. note::

    As in apoptosis, it's important to use move all cells to delete to a new list, ``cells_to_delete``,
    so that a separate Python loop will make the calls to ``self.delete_cell(cell)``.
    This ensures that the first loop does not lose its place as it searches for dying cells.

************************************************

How to Turn off Mitosis for Dying Cells
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have a separate cell type for dying cells, then just add a line
like ``if cell.type != self.NECROTIC``.

.. code-block:: python

    class MitosisSteppable(MitosisSteppableBase):
        def __init__(self,frequency=1):
            MitosisSteppableBase.__init__(self,frequency)

        def step(self, mcs):

            cells_to_divide=[]
            
            for cell in self.cell_list:
                if cell.type != self.NECROTIC:
                    cells_to_divide.append(cell)
                        
            for cell in cells_to_divide:
                self.divide_cell_random_orientation(cell)
        

        def update_attributes(self):
            # ...

Otherwise, for apoptosis, you could check the targetVolume:

.. code-block:: python

    for cell in self.cell_list_by_type(self.CENTROBLAST):
        if cell.targetVolume > 0:
            cells_to_divide.append(cell)


How to Control Division Time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to divide every cell every 70 MCS, for instance, you should 
track each cell's last division time independently using ``cell.dict``.


.. code-block:: python

    DIVISION_TIME = 70 #mcs

    class MitosisSteppable(MitosisSteppableBase):
        def __init__(self,frequency=1):
            MitosisSteppableBase.__init__(self,frequency)

        def step(self, mcs):

            cells_to_divide=[]
            
            for cell in self.cell_list:
                last_div_time = cell.dict["last division time"]
                if mcs - last_div_time >= DIVISION_TIME:
                    cell.dict["last division time"] = mcs
                    cells_to_divide.append(cell)
            
            for cell in cells_to_divide:
                self.divide_cell_random_orientation(cell)
        

        def update_attributes(self):
            # ...

.. note::

    You may like to implement some rules to reduce crowding, such as contact-inhibited growth
    or a very simple if-statement that prevents cells with too many neighbors from dividing. 
    Using pressure tends to be more realistic. 
