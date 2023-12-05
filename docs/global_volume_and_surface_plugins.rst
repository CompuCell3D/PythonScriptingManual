Global Volume and Surface Constraints
-------------------------------------

Related: `Volume and Cell Growth [Reference] <volume_and_growth.html>`_ and 
`Surface and Cell Contact [Reference] <surface.html>`_

One of the most commonly used energy terms in the GGH Hamiltonian is a
term that restricts variation of single cell volume. Its simplest form
can be coded like this:

.. code-block:: xml

    <Plugin Name="Volume">
        <VolumeEnergyParameters CellType="CellA" LambdaVolume="2.0" TargetVolume="25"/>
    </Plugin>


By analogy, we may define a term which will put a similar constraint
regarding the surface of the cell:

.. code-block:: xml

    <Plugin Name="Surface">
        <SurfaceEnergyParameters CellType="CellA" LambdaSurface="1.5" TargetSurface="20.0"/>
    </Plugin>


These two plugins inform CompuCell that the Hamiltonian will have two
additional terms associated with volume and surface conservation. That is, when a pixel copy is attempted, one cell will increase its volume and
another cell will decrease. Thus, the overall energy of the system changes.
Volume constraint essentially ensures that cells maintain
the volume which close to (this depends on thermal fluctuations) its target
volume. The role of the surface plugin is analogous to volume; it
"preserves" the total length of the cell's surface. 

The examples shown below apply volume and surface constraints to all cells in the simulation.
You can, however, apply volume and surface constraints to individual cell types or individual cells.

Energy terms for volume and surface constraints have the form:

.. math::

   \begin{eqnarray}
        E_{volume} = \lambda_{volume} \left ( V_{cell} - V_{target} \right )^2
   \end{eqnarray}

.. math::

   \begin{eqnarray}
        E_{surface} = \lambda_{surface} \left ( S_{cell} - S_{target} \right )^2
   \end{eqnarray}


.. note::

    Copying a single pixel may cause surface change
    in more than two cells – this is especially true in 3D.


.. note:: 

    The Volume and Surface plugins handle their respective behaviors automatically as long as they are added to the XML. 
    However, if your particular use case needs to avoid the built-in constraints brought by these plugins,
    you can still `track the volume and surface manually <volume_and_surface_tracker_plugins.html>`_.