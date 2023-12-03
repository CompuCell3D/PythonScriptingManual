Global Volume and Surface Constraints
-------------------------------------

One of the most commonly used energy term in the GGH Hamiltonian is a
term that restricts variation of single cell volume. Its simplest form
can be coded as show below:

.. code-block:: xml

    <Plugin Name="Volume">
        <TargetVolume>25</TargetVolume>
        <LambdaVolume>2.0</LambdaVolume>
    </Plugin>


By analogy we may define a term which will put similar constraint
regarding the surface of the cell:

.. code-block:: xml

    <Plugin Name="Surface">
        <TargetSurface>20</TargetSurface>
        <LambdaSurface>1.5</LambdaSurface>
    </Plugin>


These two plugins inform CompuCell that the Hamiltonian will have two
additional terms associated with volume and surface conservation. That
is when pixel copy is attempted one cell will increase its volume and
another cell will decrease. Thus overall energy of the system changes.
Volume constraint essentially ensures that cells maintain
the volume which close (this depends on thermal fluctuations) to target
volume. The role of surface plugin is analogous to volume, that is to
"preserve" surface. Note that surface plugin is commented out in the
example above.

The examples shown below apply volume and surface constraints to all cells in the simulation.
you can however apply volume and surface constraints to individual cell types or individual cells

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
    in more that two cells – this is especially true in 3D.
