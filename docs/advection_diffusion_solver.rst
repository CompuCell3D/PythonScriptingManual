AdvectionDiffusionSolver.
-------------------------

.. note::

    This is an experimental module and was not fully curated.

``AdvectionDiffusionSolver`` solves advection diffusion equation on a cell field as
opposed to grid. Of course, the inaccuracies are bigger than in the case
of PDE being solved on the grid but on the other hand solving the PDE on
a cell field means that we associate concentration with a given cell (not
just with a lattice point). This means that as cells move so does the
concentration. In other words we get advection for free. The
mathematical treatment of this kind of approximation was described in
Phys. Rev. E 72, 041909 (2005) paper by D.Dan et al.

The equation solved by this steppable is of the type:

.. math::
    :nowrap:

    \begin{eqnarray}
       \frac{\partial c}{\partial t} = D \nabla^2c-kc+\vec{\nu} \cdot \vec{\nabla} c + \text{secretion}
    \end{eqnarray}

where :math:`c` denotes concentration , :math:`D` is diffusion constant, :math:`k` decay constant, :math:`\vec{\nu}` is
velocity field.

In addition to just solving advection-diffusion equation this module
allows users to specify secretion rates of the cells as well as
different secretion modes. The syntax for this module follows same
pattern as ``FlexibleDiffusionSolverFE``.

Example syntax:

.. code-block:: XML

    <Steppable Type="AdvectionDiffusionSolverFE">
        <DiffusionField Name="FGF">
            <DiffusionData>
                <FieldName>FGF</FieldName>
                <DiffusionConstant>0.05</DiffusionConstant>
                <DecayConstant>0.003</DecayConstant>
                <ConcentrationFileName>flowFieldConcentration2D.txt</ConcentrationFileName>
                <DoNotDiffuseTo>Wall</DoNotDiffuseTo>
            </DiffusionData>
            <SecretionData>
                <Secretion Type="Fluid">0.5</Secretion>
                <SecretionOnContact Type="Fluid"
                <SecreteOnContactWith="Wall">0.3</SecretionOnContact>
            </SecretionData>
        </DiffusionField>
    </Steppable>

