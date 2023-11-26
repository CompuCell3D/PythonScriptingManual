Contact Plugin
--------------

Contact plugin implements computations of adhesion energy between neighboring cells.


Together with volume constraint contact energy is one of the most
commonly used energy terms in the GGH Hamiltonian. In essence it
describes how cells "stick" to each other.

The explicit formula for the energy is:

.. math::
    :nowrap:

    \begin{eqnarray}
        E_{adhesion} = \sum_{i,j,neighbors} J\left ( \tau_{\sigma(i)},\tau_{\sigma(j)} \right )\left ( 1-\delta_{\sigma(i), \sigma(j)} \right )
    \end{eqnarray}

where ``i`` and ``j`` label two neighboring lattice sites :math:`\sigma`'s denote cell
Ids, :math:`\tau`'s denote cell types .


In the above formula, we need to differentiate between cell types and
cell Ids. This formula shows that cell types and cell Ids **are not the
same**. The ``Contact`` plugin in the ``.xml`` file, defines the energy per unit
area of contact between cells of different types (:math:`J\left ( \tau_{\sigma(i)},\tau_{\sigma(j)} \right )`) and the interaction
range ``NeighborOrder`` of the contact:

.. code-block:: xml

    <Plugin Name="Contact">
        <Energy Type1="Foam" Type2="Foam">3</Energy>
        <Energy Type1="Medium" Type2="Medium">0</Energy>
        <Energy Type1="Medium" Type2="Foam">0</Energy>
        <NeighborOrder>2</NeighborOrder>
    </Plugin>


In this case, the interaction range is ``2``, thus only up to second nearest
neighbor pixels of a pixel undergoing a change or closer will be used to calculate
contact energy change. ``Foam`` cells have contact energy per unit area of ``3``
and ``Foam`` and ``Medium`` as well as Medium and Medium have contact energy of
``0`` per unit area. For more information about contact energy calculations
see “Introduction to CompuCell3D”
