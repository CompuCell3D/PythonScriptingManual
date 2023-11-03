Cell
============================

TODO: move this content into Appendix A and B.














Properties
****************************

*Tip:* You can insert code snippets to get or set these attributes in Twedit++ 
by clicking **CC3D Python -> Cell Attributes** or **CC3D Python -> Cell Constraints**.

**cell.id**: the unique identifier of the cell

**cell.type**: the phenotype that the cell belongs to

**cell.dict**: stores custom attributes for the cell. 

Example:

.. code-block:: python

    cell.dict['ATTR_NAME'] = VALUE_OR_OBJECT #This can be any Python data: integer, string, object, etc.
    print(cell.dict['ATTR_NAME'])

**cell.volume**: [Read Only Access] the *current* number of voxels the cell occupies

**cell.targetVolume**: the "goal" volume that a cell tries to shrink or grow to whenever possible

**cell.lambdaVolume**: the strength of the volume constraint; that is, how fast a cell will shrink/grow towards its targetVolume

**cell.pressure**: the pressure from the volume constraint if present

**cell.surface**: [Read Only Access] the *current* surface of the cell measured in voxel perimeter

**cell.targetSurface**: the strength of the surface constraint; that is, how fast a cell will flex towards its targetSurface

**cell.surfaceTension**: the surface tension from the Surface area constraint if present

**cell.xCOM**, **cell.yCOM**, **cell.zCOM**: [Read Only Access] the center of mass for a given cell. 
You must add the CenterOfMass plugin to your XML to use these attributes. 

**cell.clusterId**: [Read Only Access]  the ID of the cluster that the cell belongs to. This is separate from the ``cell.id``.
Can be modified using ``reassignClusterId(…)`` function.

TODO: **cell.clusterSurfaceTension**: the surface tension exerted upon the cell

TODO: **cell.ecc**: the eccentricity of the cell

TODO: **cell.lX**, **cell.lY**, **cell.lZ**:  [Read Only Access] the minor axes of the cell: x-axis, y-axis, and z-axis

TODO: **cell.fluctAmpl**: the fuctuation amplitude of the cell 

TODO: **cell.iXX**, **cell.iYY**, **cell.iZZ**, **cell.iXY**, **cell.iXZ**, **cell.iYZ**: the inertia tensor represented as 6 values



Relevant Functions
**************************************

**SteppableBasePy.fetch_cell_by_id(CELL_ID)**: finds one cell by ID

**SteppableBasePy.reassign_cluster_id(cell, newClusterId)**: assigns the cluster ID, ``newClusterId``, to the given ``cell``

TODO: **SteppableBasePy.are_cells_different(cell1, cell2)**: returns true if ``cell1`` and ``cell2`` are different

Functions to Iterate through Cells
**************************************

*Tip:* You can insert these code snippets in Twedit++ by clicking **CC3D Python -> Visit**.

**SteppableBasePy.cell_list**: returns every cell in the simulation

Example:

.. code-block:: python

        for cell in self.cell_list:
            # you can access/manipulate cell properties here
            print("id=", cell.id, " type=", cell.type, " volume=", cell.volume)
        
**SteppableBasePy.cell_list_by_type(TYPENAME_1, ...)**: returns every cell belonging to a particular type. 
If more than one type is passed, every cell belonging to any one of the given types will be included. 

.. note::
    The arugments, self.TYPENAME_1 and self.TYPENAME_2, **must** use capital letters. 
    For example, if your cell's type was called Bacteria, then it must be spelled self.BACTERIA. 

Example:

.. code-block:: python

        for cell in self.cell_list_by_type(self.TYPENAME_1, self.TYPENAME_2, ...):
            # you can access/manipulate cell properties here
            print ("id=", cell.id, " type=", cell.type)
        
**SteppableBasePy.clusters**: returns every cluster of cell compartments

Example:

.. code-block:: python
        
        for compartments in self.clusters:
            for cell in compartments:
                print(cell.id)

**SteppableBasePy.get_cluster_cells(clusterId)**: returns all cells in the same cluster as the cell specified by ``clusterId``

Example:

.. code-block:: python
        
        for cell in self.cell_list:
            cluster_cell_list = self.get_cluster_cells(cell.clusterId)
            for cell_cmpt in cluster_cell_list:
                print('compartmental cell id=', cell_cmpt)
        
            