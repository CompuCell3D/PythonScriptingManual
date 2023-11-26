Volume and Cell Growth
============================

Properties
****************************

**cell.targetVolume**: the "goal" volume that a cell tries to shrink or grow to whenever possible

**cell.lambdaVolume**: the strength of the volume constraint; that is, how fast a cell will shrink/grow towards its targetVolume

****************************

**How to Add the Volume Plugin in XML**

* As you create your simulation, check the box for either **VolumeFlex** or **VolumeLocalFlex**.
* Otherwise, add in the XML manually with this button in **Twedit++**:


.. image:: images/CC3DML_volume_dialog.PNG
   :height: 450px


Your complete ``.xml`` file should look like this. Yours may have extra code, but that's fine. 

.. code-block:: xml

    <CompuCell3D Revision="3" Version="4.4.1">    
        <Metadata>
            <!-- Basic properties simulation -->
            <NumberOfProcessors>1</NumberOfProcessors>
            <DebugOutputFrequency>10</DebugOutputFrequency>
        </Metadata>
        
        <Potts>
            <!-- Basic properties of CPM (GGH) algorithm -->
            <Dimensions x="256" y="256" z="1"/>
            <Steps>100000</Steps>
            <Temperature>10.0</Temperature>
            <NeighborOrder>1</NeighborOrder>
        </Potts>
        
        <Plugin Name="CellType">
            <!-- Listing all cell types in the simulation -->
            <CellType TypeId="0" TypeName="Medium"/>
            <CellType TypeId="1" TypeName="CellA"/>
            <CellType TypeId="2" TypeName="CellB"/>
        </Plugin>
        
        <!-- VOLUME PLUGIN -->
        <Plugin Name="Volume">
            <VolumeEnergyParameters CellType="CellA" LambdaVolume="2.0" TargetVolume="50"/>
            <VolumeEnergyParameters CellType="CellB" LambdaVolume="2.0" TargetVolume="50"/>
        </Plugin>
        
        <Plugin Name="NeighborTracker">
            <!-- Module tracking neighboring cells of each cell -->
        </Plugin>
        
        <Plugin Name="Contact">
            <!-- Specification of adhesion energies goes here -->
        </Plugin>
        
        <Steppable Type="BlobInitializer">            
            <!-- Initial layout of cells in the form of spherical (circular in 2D) blob -->
            <Region>
                <Center x="128" y="128" z="0"/>
                <Radius>51</Radius>
                <Gap>0</Gap>
                <Width>7</Width>
                <Types>CellA,CellB</Types>
            </Region>
        </Steppable>
    </CompuCell3D>



VolumeFlex vs VolumeLocalFlex
**********************************************

VolumeFlex is designed so that lambda volume and target volume are defined in XML. 
When using VolumeLocalFlex, the lambda volume and target volume must be defined in Python.
(The same is true for SurfaceLocalFlex, lambda surface, and target surface). 

**Example 1:** VolumeFlex

XML

.. code-block:: xml

    <Plugin Name="Volume">
      <VolumeEnergyParameters CellType="Somatic" LambdaVolume="2.0" TargetVolume="50"/>
      <VolumeEnergyParameters CellType="Necrotic" LambdaVolume="2.0" TargetVolume="50"/>
   </Plugin>

   
**Example 2:** (a separate project) VolumeLocalFlex

XML

.. code-block:: xml

   <Plugin Name="Volume"/>
   
Python Steppable

.. code-block:: python

    def start(self):
        for cell in self.cell_list:
            cell.targetVolume = 25
            cell.lambdaVolume = 5.0


Complete Example: Contact-Inhibited Cell Growth
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cell-cell contact generally inhibits proliferation (contact inhibition).

`Download the sample code here <https://drive.google.com/file/d/1GIk6VyTcZnwZ8_LgCClAxUYzb-clhbTY/view?usp=drive_link>`_, 
then watch the video from the latest workshop to follow along:

`Get the slides here <https://docs.google.com/presentation/d/1KNnXN1p7J81UrFxDw6c6yc0o0NmDl3sa/edit#slide=id.p24>`_.

.. image:: https://img.youtube.com/vi/x0FG5LRf1U8/maxresdefault.jpg
    :alt: Workshop Tutorial Video
    :target: https://www.youtube.com/watch?v=x0FG5LRf1U8&list=PLiEtieOeWbMKTIF2mekBc9cABFPEDwCdj&index=19&t=4030
    :width: 80%

..
    [Last Updated] November 2023