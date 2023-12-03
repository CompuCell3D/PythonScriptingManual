DiffusionSolverFE
-----------------

DiffusionSolverFE is new solver in 3.6.2 and is intended to fully
replace ``FlexibleDiffusionSolverFE``. It eliminates several limitations
and inconveniences of ``FlexibleDiffusionSolverFE`` and provides new
features such as GPU implementation or cell type dependent
diffusion/decay coefficients. In addition it also eliminates the need
to rescale diffusion/decay/secretion constants. It checks stability
condition of the PDE and then rescales appropriately all coefficients
and computes how many extra times per MCS the solver has to be called. It
makes those extra calls automatically.

.. warning::

    One of the key differences between ``FlexibleDiffusionSolverFE`` and
    ``DiffusionSolverFE`` is the way in which secretion is treated. In
    ``FlexibleDiffusionSolverFE`` all secretion amount is done once followed by
    possibly multiple diffusion calls to diffusion (to avoid numerical
    instabilities). In ``DiffusionSolverFE`` the default mode of operation is
    such that multiple secretion and diffusion calls are interleaved.
    This means that instead of secreting full amount for a given MCS and
    diffusing it, the ``DiffusionSolverFE`` secretes substance gradually so that
    there is equal amount of secretion before each call of the diffusion.
    One can change this behavior by adding ``<DoNotScaleSecretion/>`` to
    definition of the diffusion solver e.g.

    .. code-block::

            <Steppable Type="DiffusionSolverFE">
                <DoNotScaleSecretion/>
                <DiffusionField Name="ATTR">
                    <DiffusionData>

                …

    With such definition the ``DiffusionSolverFE`` will behave like
    ``FlexibleDiffusionSolverFE`` as far as computation.

.. note::

    ``DiffusionSolverFE`` autoscales diffusion discretization
    depending on the lattice so that ``<AutoscaleDiffusion/>`` we used in
    ``FlexibleDiffusionSolverFE`` is unnecessary.
    This may result in slow performance so users have to be aware that those
    extra calls to the solver may be the cause.

Typical syntax for the ``DiffusionSolverFE`` may look like example below:

.. code-block:: xml

    <Steppable Type="DiffusionSolverFE">
        <DiffusionField Name="ATTR">
            <DiffusionData>
                <FieldName>ATTR</FieldName>
                <GlobalDiffusionConstant>0.1</GlobalDiffusionConstant>
                <GlobalDecayConstant>5e-05</GlobalDecayConstant>
                <DiffusionCoefficient CellType="Red">0.0</DiffusionCoefficient>
            </DiffusionData>
            <SecretionData>
                <Secretion Type="Bacterium">100</Secretion>
            </SecretionData>
            <BoundaryConditions>
                <Plane Axis="X">
                    <Periodic/>
                </Plane>
                <Plane Axis="Y">
                    <Periodic/>
                </Plane>
                </BoundaryConditions>
        </DiffusionField>
    </Steppable>


The syntax resembles the syntax for ``FlexibleDiffusionSolverFE``. We
specify global diffusion constant by using ``<GlobalDiffusionConstant>``
tag. This specifies diffusion coefficient which applies to entire region
of the simulation. We can override this specification for regions
occupied by certain cell types by using the following syntax:

.. code-block:: xml

    <DiffusionCoefficient CellType="Red">0.0</DiffusionCoefficient>

Similar principles apply to decay constant and we use
``<GlobalDecayConstant>`` tag to specify global decay coefficient and

.. code-block:: xml

    <DecayCoefficient CellType="Red">0.0</DecayCoefficient>

to override global definition for regions occupied by Red cells.

We do not support ``<DeltaX>``, ``<DeltaT>`` or ``<ExtraTimesPerMCS>`` tags.

.. note::

    ``DiffusionSolverFE`` autoscales diffusion discretization
    depending on the lattice so that ``<AutoscaleDiffusion/>`` we used in
    ``FlexibleDiffusionSolverFE`` is unnecessary.

Running DiffusionSolver on GPU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run ``DiffusionSolverFE`` on GPU all we have to do (besides having OpenCL
compatible GPU and correct drives installed) to replace first line of
solver specification:

.. code-block:: xml

    <Steppable Type="DiffusionSolverFE">

with

.. code-block:: xml

    <Steppable Type="DiffusionSolverFE_OpenCL">


.. note::

    Depending on your computer hardware you may or may not be able to take advantage of
    GPU capabilities.

