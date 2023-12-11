FlexibleDiffusionSolver
-----------------------

This steppable is one of the basic and most important modules in
CompuCell3D simulations.


.. tip::

    Starting from version ``3.6.2`` we developed ``DiffusionSolverFE``
    which eliminates several inconveniences of ``FlexibleDiffusionSolver``.

As the name suggests it is responsible for solving diffusion equation
but in addition to this it also handles chemical secretion which maybe
thought of as being part of general diffusion equation:

.. math::
    :nowrap:

    \begin{eqnarray}
        \frac{\partial c}{\partial t} = D \nabla^2c-kc+\text{secretion}
    \end{eqnarray}


where ``k`` is a decay constant of concentration ``c`` and ``D`` is the
diffusion constant. The term called ``secretion`` has the meaning as
described below.

Example syntax for FlexibleDiffusionSolverFE looks as follows:

.. code-block:: xml

    <Steppable Type="FlexibleDiffusionSolverFE">
        <AutoscaleDiffusion/>
        <DiffusionField Name="FGF8">
            <DiffusionData>
                <FieldName>FGF8</FieldName>
                <DiffusionConstant>0.1</DiffusionConstant>
                <DecayConstant>0.002</DecayConstant>
                <ExtraTimesPerMCS>5</ExtraTimesPerMCS>
                <DeltaT>0.1</DeltaT>
                <DeltaX>1.0</DeltaX>
                <DoNotDiffuseTo>Bacteria</DoNotDiffuseTo>
                <InitialConcentrationExpression>x*y
                </InitialConcentrationExpression>
            </DiffusionData>

            <SecretionData>
                <Secretion Type="Amoeba">0.1</Secretion>
            </SecretionData>

            <BoundaryConditions>
                <Plane Axis="X">
                    <ConstantValue PlanePosition="Min" Value="10.0"/>
                    <ConstantValue PlanePosition="Max"  Value="10.0"/>
                </Plane>

                <Plane Axis="Y">
                    <ConstantDerivative PlanePosition="Min" Value="10.0"/>
                    <ConstantDerivative PlanePosition="Max"  Value="10.0"/>
                </Plane>
            </BoundaryConditions>

        </DiffusionField>

        <DiffusionField Name="FGF">
            <DiffusionData>
                <FieldName>FGF</FieldName>
                <DiffusionConstant>0.02</DiffusionConstant>
                <DecayConstant>0.001</DecayConstant>
                <DeltaT>0.01</DeltaT>
                <DeltaX>0.1</DeltaX>
                <DoNotDiffuseTo>Bacteria</DoNotDiffuseTo>
            </DiffusionData>
            <SecretionData>
                <SecretionOnContact Type="Medium"
                 SecreteOnContactWith="Amoeba">0.1</SecretionOnContact>
                <Secretion Type="Amoeba">0.1</Secretion>
            </SecretionData>
        </DiffusionField>
    </Steppable>


We define sections that describe a field on which the steppable is to
operate. In our case we declare just two diffusion fields - ``FGF8`` and ``FGF``.

.. warning::

    When you want to solve more than one diffusive field using given diffusion
    you should declare those multiple fiuelds within a single definition of the diffusion solver. You cannot
    include two diffusion solver definitions - one with e.g. ``FGF8`` and another with ``FGF``.
    In other words you can only define e.g. ``FlexibleDiffusionSolverFE`` once per simulation.
    You can however use FlexibleDiffusionSolverFE for e.g. ``FGF`` and ``DiffusionSolverFE`` for e.g. ``FGF8``

Inside the diffusion field we specify sections describing diffusion and
secretion. Let's take a look at ``DiffusionData`` section first:

.. code-block:: xml

    <DiffusionField Name="FGF8">
    <DiffusionData>
        <FieldName>FGF8</FieldName>
        <DiffusionConstant>0.1</DiffusionConstant>
        <DecayConstant>0.002</DecayConstant>
        <ExtraTimesPerMCS>5</ExtraTimesPerMCS>
        <DeltaT>0.1</DeltaT>
        <DeltaX>1.0</DeltaX>
        <DoNotDiffuseTo>Bacteria</DoNotDiffuseTo>

        <InitialConcentrationExpression>x*y
        </InitialConcentrationExpression>

    </DiffusionData>

We give a name (``FGF8``) to the diffusion field – this is required as we
will refer to this field in other modules.

.. note::::

    Field name is repeated twice once in the ``<DiffusionField Name="FGF8">``
    element and in the ``<FieldName>FGF8</FieldName>``
    element. The rule is that the name defined in the ``<DiffusionField Name="FIELD_NAME">``
     element trumps the latter definition. The latter
    definition was used for all versions of CC3D until ``3.7.2`` therefore to
    keep old code compatible we still maintain possibility that field name
    will be defined using ``<FieldName>FIELD_NAME</FieldName>`` only.

Next we specify diffusion constant and decay constant.

.. warning::

    We use Forward Euler Method to solve these equations.
    This is not a stable method for solving diffusion equation and we do not
    perform stability checks. If you enter too high diffusion constant for
    example you may end up with unstable (wrong) solution. Always test your
    parameters to make sure you are not in the unstable region.

We may also specify cells that will not participate in the diffusion.
You do it using ``<DoNotDiffuseTo>`` tag. In this example we do not let any ``FGF`` diffuse
into ``Bacteria`` cells. You may of course use as many as necessary
``<DoNotDiffuseTo>`` tags. To prevent decay of a chemical in certain cells
we use syntax:

.. code-block:: xml

    <DoNotDecayIn>Medium</DoNotDecayIn>

In addition to diffusion parameters we may specify how secretion should
proceed. ``SecretionData`` section contains all the necessary information to
tell CompuCell how to handle secretion. Let's study the example:

.. code-block:: xml

    <SecretionData>
        <SecretionOnContact Type="Medium" SecreteOnContactWith="Amoeba">0.1</SecretionOnContact>
        <Secretion Type="Amoeba">0.1</Secretion>
    </SecretionData>


Here we have a definition two major secretion modes. Line:

.. code-block:: xml

    <Secretion Type="Amoeba">0.1</Secretion>

ensures that every cell of type ``Amoeba`` will get ``0.1`` increase in
concentration every MCS. Line:

.. code-block:: xml

    <SecretionOnContact Type="Medium" SecreteOnContactWith="Amoeba">0.1</SecretionOnContact>

means that cells of type ``Medium`` will get additional ``0.1`` increase in
concentration **but only when** they touch cell of type ``Amoeba``. This mode of
`secretion <secretion.html>`_ is called ``SecretionOnContact``.

We can also see new CC3DML tags ``<DeltaT>`` and ``<DeltaX>``. Their values
determine the correspondence between MCS and actual time and between
lattice spacing and actual spacing size. In this example for the first
diffusion field one MCS corresponds to ``0.``1 units of actual time and
lattice spacing is equal ``1`` unit of actual length. What is happening here
is that the diffusion constant gets multiplied by:

.. code-block:: python

    DeltaT/(DeltaX * DeltaX)

provided the decay constant is set to 0. If the decay constant is not
zero DeltaT appears additionally in the term (in the explicit numerical
approximation of the diffusion equation solution) containing decay
constant so in this case it is more than simple diffusion constant
rescaling.

``DeltaT`` and ``DeltaX`` settings are closely related to ``ExtraTimesPerMCS``
setting which allows calling of diffusion (and only diffusion) more than
once per MCS. The number of extra calls per MCS is specified by the user
on a per-field basis using ``ExtraTimesPerMCS`` tag.

.. warning::
    When using ``ExtraTimesPerMCS``, secretion functions will
    called only once per MCS. This is different than using ``PDESolverCaller``,
    where the entire module is called multiple times (this includes diffusion and
    secretion for all fields).

.. tip::

    We recommend that you stay away from redefining ``DeltaX`` and
    ``DeltaT`` and assume that your diffusion/decay coefficients are expressed
    in units of pixel (distance) and MCS (time). This way when you assign
    physical time and distance units to MCS and pixels you can easily
    obtain diffusion and decay constants. ``DeltaX`` and ``DeltaT`` introduce
    unnecessary complications.

The ``AutoscaleDiffusion`` tag tells CC3D to automatically rescale diffusion
constant when switching between square and hex lattices. In previous
versions of CC3D such scaling had to be done manually to ensure that
solutions diffusion of equation on different lattices match. Here we
introduced for user convenience a simple tag that does rescaling
automatically. The rescaling factor comes from the fact that the
discretization of the divergence term in the diffusion equation has
factors such as unit lengths, using surface are and pixel/voxel volume
in it. On a square lattice all those values have numerical value of ``1.0`` .
On hex lattice, and for that matter of non-square latticeses, only
pixel/voxel volume has numerical value of ``1`` . All other quantities have
values different than ``1.0`` which causes the necessity to rescale
diffusion constant. The detail of the hex lattice derivation will be
presented in the "Introduction to Hexagonal Lattices in CompuCell3D" -
http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf .


The ``FlexibleDiffusionSolver`` is also capable of solving simple coupled
diffusion type PDE of the form:

.. math::
    :nowrap:

    \begin{align*}
     \frac{\partial c}{\partial t} = D \nabla^2c-kc+\text{secretion} + m_dcd + m_fcf \\
     \frac{\partial d}{\partial t} = D \nabla^2d-kd+\text{secretion} + n_cdc + n_fdf \\
     \frac{\partial f}{\partial t} = D \nabla^2f-kf+\text{secretion} + p_cfc + p_dfd
    \end{align*}

where :math:`m_c`, :math:`m_f`, :math:`n_c` , :math:`n_f`, :math:`p_c`, :math:`p_d` are coupling coefficients.
To code the above equations in CC3DML syntax you need to use the following syntax:

.. code-block:: xml

    <Steppable Type="FlexibleDiffusionSolverFE">
        <DiffusionField>
            <DiffusionData>
                <FieldName>c</FieldName>
                <DiffusionConstant>0.1</DiffusionConstant>
                <DecayConstant>0.002</DecayConstant>
                <CouplingTerm InteractingFieldName=”d” CouplingCoefficent=”0.1”/>
                <CouplingTerm InteractingFieldName=”f” CouplingCoefficent=”0.2”/>
                <DeltaT>0.1</DeltaT>
                <DeltaX>1.0</DeltaX>
                <DoNotDiffuseTo>Bacteria</DoNotDiffuseTo>
            </DiffusionData>
            <SecretionData>
                <Secretion Type="Amoeba">0.1</Secretion>
            </SecretionData>
        </DiffusionField>

        <DiffusionField>
            <DiffusionData>
                <FieldName>d</FieldName>
                <DiffusionConstant>0.02</DiffusionConstant>
                <DecayConstant>0.001</DecayConstant>
                <CouplingTerm InteractingFieldName=”c” CouplingCoefficent=”-0.1”/>
                <CouplingTerm InteractingFieldName=”f” CouplingCoefficent=”-0.2”/>
                <DeltaT>0.01</DeltaT>
                <DeltaX>0.1</DeltaX>
                <DoNotDiffuseTo>Bacteria</DoNotDiffuseTo>
                </DiffusionData>
            <SecretionData>
                <Secretion Type="Amoeba">0.1</Secretion>
            </SecretionData>
        </DiffusionField>

        <DiffusionField>
            <DiffusionData>
                <FieldName>f</FieldName>
                <DiffusionConstant>0.02</DiffusionConstant>
                <DecayConstant>0.001</DecayConstant>
                <CouplingTerm InteractingFieldName=”c” CouplingCoefficent=”-0.2”/>
                <CouplingTerm InteractingFieldName=”d” CouplingCoefficent=”0.2”/>
                <DeltaT>0.01</DeltaT>
                <DeltaX>0.1</DeltaX>
                <DoNotDiffuseTo>Bacteria</DoNotDiffuseTo>
            </DiffusionData>
            <SecretionData>
                <Secretion Type="Amoeba">0.1</Secretion>
            </SecretionData>
        </DiffusionField>
    </Steppable>



As one can see the only addition that is required to couple diffusion
equations has simple syntax:

.. code-block:: xml

    <CouplingTerm InteractingFieldName=”c” CouplingCoefficent=”-0.1”/>
    <CouplingTerm InteractingFieldName=”f” CouplingCoefficent=”-0.2”/>
