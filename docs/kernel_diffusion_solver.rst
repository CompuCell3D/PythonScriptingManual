KernelDiffusionSolver
---------------------

This diffusion solver has the advantage over previous solvers that it
can handle large diffusion constants. It is also stable. However, it
does not accept options like ``<DoNotDiffuseTo>`` or ``<DoNotDecayIn>``. It also
requires periodic boundary conditions.

Simply put KernelDiffusionSolver solves diffusion equation:

.. math::
    :nowrap:

    \begin{eqnarray}
        \frac{\partial c}{\partial t} = D \nabla^2c-kc+\text{secretion}
    \end{eqnarray}

with fixed, periodic boundary conditions on the edges of the lattice.
This is different from ``FlexibleDiffusionSolverFE`` where the boundary
conditions evolve. You also need to choose a proper ``Kernel range (K)``
according to the value of diffusion constant. Usually when :math:`K^2e^{-K^2/{4D}}`
is small (this is the main part of the
integrand), the approximation converges to the exact value.

The syntax for this solver is as follows:

.. code-block:: xml

    <Steppable Type="KernelDiffusionSolver">
      <DiffusionField Name="FGF">
        <Kernel>4</Kernel>
        <DiffusionData>
          <FieldName>FGF</FieldName>
          <DiffusionConstant>1.0</DiffusionConstant>
          <DecayConstant>0.000</DecayConstant>
        <ConcentrationFileName>
          Demos/diffusion/diffusion_2D.pulse.txt
          </ConcentrationFileName>
        </DiffusionData>
      </DiffusionField>
    </Steppable>



Inside ``<DiffusionField>`` tag one may also use option ``<CoarseGrainFactor>``. For example:

.. code-block:: xml

    <Steppable Type="KernelDiffusionSolver">
      <DiffusionField Name="FGF">
        <Kernel>4</Kernel>
        <CoarseGrainFactor>2</CoarseGrainFactor>
        <DiffusionData>
          <FieldName>FGF</FieldName>
          <DiffusionConstant>1.0</DiffusionConstant>
          <DecayConstant>0.000</DecayConstant>
          <ConcentrationFileName>
          Demos/diffusion/diffusion_2D.pulse.txt
          </ConcentrationFileName>
        </DiffusionData>
      </DiffusionField>
    </Steppable>
