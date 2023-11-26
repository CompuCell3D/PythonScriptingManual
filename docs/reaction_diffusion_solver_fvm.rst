ReactionDiffusionSolverFVM
---------------------------

The reaction diffusion finite volume (RDFVM) solver uses the finite volume method to
solve the following system of :math:`N` reaction diffusion equations:

.. math::
    :nowrap:

    \begin{align*}
        \int \iiint \frac{\partial c_1}{\partial t} dV dt &= \int \iiint \left( \nabla \left(D_1 \nabla c_1 \right) + A_1 \left(c_1, c_2, ..., c_N \right) c_1 + B_1 \left(c_1, c_2, ..., c_N \right) \right) dV dt \\
        \int \iiint \frac{\partial c_2}{\partial t} dV dt &= \int \iiint \left( \nabla \left(D_2 \nabla c_2 \right) + A_2 \left(c_1, c_2, ..., c_N \right) c_2 + B_2 \left(c_1, c_2, ..., c_N \right) \right) dV dt \\
        {\text ...} \\
        \int \iiint \frac{\partial c_N}{\partial t} dV dt &= \int \iiint \left( \nabla \left(D_N \nabla c_N \right) + A_N \left(c_1, c_2, ..., c_N \right) c_N + B_N \left(c_1, c_2, ..., c_N \right) \right) dV dt
    \end{align*}

The RDFVM solver provides a broad range of basic and detailed modeling and simulation capability,
including the following,

* Explicit surface transport modeling and boundary conditions on the basis of location
* Dynamic diffusivity on the basis of cells and location
* Maintenance of numerical stability through adaptive time-stepping
* String-based field reaction model specification
* Secretion and uptake on the basis of cells
* Settable discretization length along each spatial direction

At its most basic level, the RDFVM solver calculates the flux across the implicit surfaces of the lattice.
RDVM differs from other CC3D solvers in that it provides the ability to choose a model of the flux
across each surface in the lattice. Consider a point :math:`\mathbf{x}` in the lattice, and suppose
:math:`\mathbf{x}_k` is the coordinate of a :math:`k\mathrm{th}` neighboring site in the lattice.
For each :math:`j\mathrm{th}` concentration field :math:`c_j \left( \mathbf{x}, t \right)` at time :math:`t`,
the RDFVM solver calculates the flux :math:`F_{j, k}` of material over the surface shared by the volume
element at :math:`\mathbf{x}` and its :math:`k\mathrm{th}` neighbor. Using the finite volume method, this formalism
produces the discretized form for calculating each concentration field at time :math:`t + \Delta t`,

.. math::

    c_j \left( \mathbf{x}, t + \Delta t \right) = c_j \left( \mathbf{x}, t \right) + \Delta t \left( \sum_k F_{j, k} \left( c_j \left( \mathbf{x}, t \right), c_j \left( \mathbf{x}_k, t \right) \right) + s_j \left( \mathbf{x}, t \right)  \right)

Transport via diffusion occurs according to the diffusivity :math:`D_j \left( \mathbf{x}, t \right)` on
either side of a surface and distance :math:`\Delta x_k` separating :math:`\mathbf{x}` and :math:`\mathbf{x}_k`,

.. math::

    F_{j, k} \left( \mathbf{x}, t \right) = \frac{1}{\left( \Delta x_k \right)^2} D_{j, k} \left( \mathbf{x}, t \right) \left( c_j \left( \mathbf{x}_k, t \right) - c_j \left( \mathbf{x}, t \right) \right),

where :math:`D_{j, k} \left( \mathbf{x}, t \right)` is the diffusivity of the surface shared by the volumes at
:math:`\mathbf{x}` and :math:`\mathbf{x}_k`,

.. math::

    D_{j, k} \left( \mathbf{x}, t \right) = \frac{2 D_j \left( \mathbf{x}, t \right) D_j \left( \mathbf{x}_k, t \right)}{D_j \left( \mathbf{x}, t \right) + D_j \left( \mathbf{x}_k, t \right)}

Transport via a simple biased permeability occurs according to the permeation coefficient
:math:`P_j \left( \mathbf{x}, t \right)`, bias coefficients :math:`a_j \left( \tau \right)` and
:math:`b_j \left( \tau \right)` according to cell type :math:`\tau`, and area :math:`A_k` of the
surface shared by the volumes at :math:`\mathbf{x}` and :math:`\mathbf{x}_k`,

.. math::

    F_{j, k} \left( \mathbf{x}, t \right) = \frac{1}{\Delta x_k} \left(b_j \left( \tau \left( \mathbf{x}_k, t \right) \right) c_j \left( \mathbf{x}_k, t \right) - a_j \left( \mathbf{x}, t \right) c_j \left( \mathbf{x}, t \right) \right)

where :math:`P_{j, k} \left( \mathbf{x}, t \right)` is the permeationg coefficient of the
surface shared by the volumes at :math:`\mathbf{x}` and :math:`\mathbf{x}_k`,

.. math::

    P_{j, k} \left( \mathbf{x}, t \right) = \frac{2 P_j \left( \mathbf{x}, t \right) P_j \left( \mathbf{x}_k, t \right)}{P_j \left( \mathbf{x}, t \right) + P_j \left( \mathbf{x}_k, t \right)}

The following is a representative example of a specification for the RDFVM solver using two fields
*U* and *V* and two cell types *CellType1* and *CellType2*,

.. code-block:: xml

    <Steppable Type=”ReactionDiffusionSolverFVM”>
        <DeltaX>1.0</DeltaX>
        <DeltaY>1.0</DeltaY>
        <DeltaZ>1.0</DeltaZ>
        <AutoTimeSubStep/>
        <FluctuationCompensator/>
        <DiffusionField Name=”U”>
            <DiffusionData>
                <DiffusionConstant>0.1</DiffusionConstant>
                <DiffusionCoefficient CellType=”CellType1”>0.1</DiffusionCoefficient>
                <DiffusionCoefficient CellType=”CellType2”>0.1</DiffusionCoefficient>
                <DiffusivityByType/>
                <DiffusivityFieldInMedium/>
                <InitialConcentrationExpression>x</InitialConcentrationExpression>
            </DiffusionData>
            <SecretionData>
                ...
            </SecretionData>
            <ReactionData>
                <ExpressionSymbol>u</ExpressionSymbol>
                <ExpressionMult>(-1.0+u*v)</ExpressionMult>
                <ExpressionIndep>0.1</ExpressionIndep>
            </ReactionData>
            <BoundaryConditions>
                ...
            </BoundaryConditions>
        </DiffusionField>
        <DiffusionField Name=”V”>
            <DiffusionData>
                <DiffusionConstant>0.1</DiffusionConstant>
                <DiffusionCoefficient CellType=”CellType1”>0.1</DiffusionCoefficient>
                <DiffusionCoefficient CellType=”CellType2”>0.1</DiffusionCoefficient>
                <DiffusivityByType/>
                <DiffusivityFieldEverywhere/>
                <PermIntCoefficient Type1=”CellType1”, Type2=”CellType1”>0.1</PermIntCoefficient>
                <PermIntCoefficient Type1=”CellType1”, Type2=”CellType2”>0.1</PermIntCoefficient>
                <PermIntCoefficient Type1=”CellType2”, Type2=”CellType2”>0.1</PermIntCoefficient>
                <PermIntBias Type1=”CellType1”, Type2=”CellType2”>0.01</PermIntBias>
                <SimplePermInt/>
            </DiffusionData>
            <SecretionData>
                ...
            </SecretionData>
            <ReactionData>
                <ExpressionSymbol>v</ExpressionSymbol>
                <ExpressionMult>(-u^2)</ExpressionMult>
                <ExpressionIndep>0.9</ExpressionIndep>
            </ReactionData>
            <BoundaryConditions>
                ...
            </BoundaryConditions>
        </DiffusionField>
    </Steppable>

This specification implements a number of features while implementing the Schnakenberg model of
the form,

.. math::
    :nowrap:

    \begin{align*}
        \frac{\partial U}{\partial t} &= \nabla \left(D_U \nabla U \right) + \left( U V - 1 \right) U + 0.1 \\
        \frac{\partial V}{\partial t} &= \nabla \left(D_V \nabla V \right) - U^2 V + 0.9
    \end{align*}

The complete CC3DML interface for the RDFVM solver is as follows,

* **Element** ``<DeltaX>`` (optional)
    * Specifies discretization along the *x* dimension.
    * If only ``<DeltaX>`` is specified, then a uniform discretization is applied along all directions.
* **Element** ``<DeltaY>`` (optional)
    * Specifies discretization along the *y* dimension.
* **Element** ``<DeltaZ>`` (optional)
    * Specifies discretization along the *z* dimension.
* **Element** ``<AutoTimeSubStep>`` (optional)
    * Enables time sub-stepping to optimize solver performance.
    * Only reliable when all reaction expressions of a field are independent of the field.
    * When enabled, simulation steps are explicitly integrated using maximum stable sub-steps.
    * Note that the derived stability condition (Scarborough) is sufficient but not necessary, so greater time steps than those calculated may be stable, but are not guaranteed to be stable.
* **Element** ``<FluctuationCompensator>`` (optional)
    * Enables deployment of the CC3D FluctuationCompensator.
* **Element** ``<DiffusionField>``
    * Defines a diffusion field
    * **Attribute** ``Name``: the name of the field
    * **Element** ``<DiffusionData>``
        * **Element** ``<DiffusionConstant>`` (optional)
            * Specifies a constant diffusion coefficient for the medium.
            * **Value**: value of the diffusion coefficient
        * **Element** ``<DiffusionCoefficient>`` (optional)
            * Specifies a constant diffusion coefficient for a cell type.
            * Can be set per cell during simulation execution
            * **Attribute** ``CellType``: name of the cell type
            * **Value**: value of the diffusion coefficient
        * **Element** ``<DiffusivityByType>`` (optional)
            * Imposes diffusion coefficients according to occupying ID label
            * Each cell and the medium is initialized with a diffusivity specified by ``<DiffusionCoefficient>`` and ``<DiffusionConstant>``, respectively.
            * Without any other diffusion mode specification, ``<DiffusionConstant>`` is everywhere applied.
        * **Element** ``<DiffusivityFieldInMedium>`` (optional)
            * Activates editable field diffusivity in the medium.
        * **Element** ``<DiffusivityFieldEverywhere>`` (optional)
            * Activates editable field diffusivity in the simulation domain.
            * The diffusivity field of a field with name “Field” can be accessed in Python as a concentration field with the name “FieldDiff”.
            * Diffusion mode precedence is ``<DiffusivityFieldEverywhere>`` over ``<DiffusivityFieldInMedium>`` over ``<DiffusivityByType>`` over constant diffusion.
        * **Element** ``<SimplePermInt>`` (optional)
            * Activates simple interface transport flux at cell-cell and cell-medium interfaces.
        * **Element** ``<PermIntCoefficient>`` (optional)
            * Specifies a permeation coefficient for the interface of two cell types (denoted :math:`P_j`).
            * Can be accessed per cell and modified during simulation execution.
            * Value defaults to zero.
            * **Attribute** ``Type1``: name of the first cell type, or Medium
            * **Attribute** ``Type2``: name of the second cell type, or Medium
            * **Value**: value of the coefficient
        * **Element** ``<PermIntBias>`` (optional)
            * Specifies a permeability bias coefficient for the interface of two types (denoted :math:`b_j`).
            * Can be accessed per cell and modified during simulation execution.
            * Value defaults to one.
            * **Attribute** ``Type1``: name of the first cell type, or Medium
            * **Attribute** ``Type2``: name of the second cell type, or Medium
            * **Value**: value of the coefficient
        * **Element** ``<InitialConcentrationExpression>`` (optional)
            * String expression for the initial concentration
            * **Value**: initial concentration expression (*e.g.*, ``x*y+10*z``)
    * **Element** ``<SecretionData>`` (optional)
            * Secretion data elements, defined in the same way as for DiffusionSolverFE
    * **Element** ``<ReactionData>`` (optional)
        * **Element** ``<ExpressionSymbol>`` (optional)
            * Declares a custom symbol for the field in reaction expressions.
            * Can be used to refer to a field in reactions defined for other fields.
            * Value defaults to the field name + “ExpSym” (*e.g.*, ``MyFieldExpSym``).
            * Only one can be defined per field.
            * **Value**: expression symbol (*e.g.*, ``MyField``)
        * **Element** ``<ExpressionMult>`` (optional)
            * Defines an expression for the field-dependent reaction (denoted :math:`A_j`).
            * **Value**: reaction expression (*e.g.*, ``10*MyOtherField``)
        * **Element** ``<ExpressionIndep>`` (optional)
            * Defines an expression for the field-independent reaction (denoted :math:`B_j`).
            * **Value**: reaction expression (*e.g.*, ``MyOtherField-20``)
    * **Element** ``<BoundaryConditions>`` (optional)
        * Boundary condition elements, defined in the same as for DiffusionSolverFE.
        * Boundary conditions are applied at surfaces and can be manipulated at each site during simulation execution.
        * If a condition is not specified for a boundary, then it is assumed to be zero flux.

The RDFVM solver provides a runtime interface for manipulating various model features during a simulation
from a steppable. In general, the RDFVM solver is accessible during simulations that use it in Python from
any steppable using the attribute ``reaction_diffusion_solver_fvm``,

.. code-block:: python

    from cc3d.core.PySteppables import *
    from cc3d.cpp import CompuCell

    class MySteppable(SteppableBasePy):

        def start(self):
            # Reference to the reaction diffusion finite volume solver, or None if the solver is not loaded
            rd_fvm = self.reaction_diffusion_solver_fvm
            # Get the diffusivity field for field with name "MyField" and set some values
            my_field_diff = self.field.MyFieldDiff
            for x in range(self.dim.x):
                my_field_diff[x, 0, 0] *= 2.0
            # Make the bottom boundary concentration of the field a linear function
            for x in range(self.dim.x):
                rd_fvm.useFixedConcentration("MyField", "MinY", x / (self.dim.x - 1), CompuCell.Point3D(x, 0, 0))
            # Use permeable membrane transport at the left boundary volume elements
            for y in range(self.dim.y):
                rd_fvm.usePermeableSurface("MyField", "MaxX", CompuCell.Point3D(0, y, 0))
            # Increase the diffusivity in cell 1
            cell_1 = self.fetch_cell_by_id(1)
            cell_diff = rd_fvm.getCellDiffusivityCoefficient(cell_1, "MyField")
            rd_fvm.setCellDiffusivityCoefficient(cell_1, "MyField", 2 * cell_diff)
            # Increase the permeation coefficient between cell 1 and cells of type "Type2"
            perm_cf, cell_type1_bias, cell_type2_bias = rd_fvm.getPermeableCoefficients(cell_1,
                                                                                        self.cell_type.Type2,
                                                                                        "MyField")
            rd_fvm.setCellPermeationCoefficient(cell_1, self.cell_type.Type2, "MyField", 2 * perm_cf)

The boundary conditions of each volume element can be set, modified and unset during simulation.
In general, a volume element can be selected by location using a CC3D ``Point3D``, and a surface of
a volume can be selected using the following names,

* ``MinX``: surface with outward-facing normal pointing towards the negative *x* direction.
* ``MaxX``: surface with outward-facing normal pointing towards the positive *x* direction.
* ``MinY``: surface with outward-facing normal pointing towards the negative *y* direction.
* ``MaxY``: surface with outward-facing normal pointing towards the positive *y* direction.
* ``MinZ``: surface with outward-facing normal pointing towards the negative *z* direction.
* ``MaxZ``: surface with outward-facing normal pointing towards the positive *z* direction.

The RDFVM solver provides methods for setting the following mass transport laws and
conditions on the basis of individual volume element surface during simulation execution,

* useDiffusiveSurface(field_name: string, surface_name: string, pt: CompuCell.Point3D)
    * Use diffusive transport on a surface of a volume
    * ``field_name``: name of the field
    * ``surface_name``: name of the surface
    * ``pt``: location of the volume
* useDiffusiveSurfaces(field_name: string, pt: CompuCell.Point3D)
    * Use diffusive transport on all surfaces of a volume
    * ``field_name``: name of the field
    * ``pt``: location of the volume
* usePermeableSurface(field_name: string, surface_name: string, pt: CompuCell.Point3D)
    * Use permeable membrane transport on a surface of a volume
    * ``field_name``: name of the field
    * ``surface_name``: name of the surface
    * ``pt``: location of the volume
* usePermeableSurfaces(field_name: string, pt: CompuCell.Point3D)
    * Use permeable membrane transport on all surfaces of a volume
    * ``field_name``: name of the field
    * ``pt``: location of the volume
* useFixedFluxSurface(field_name: string, surface_name: string, outward_val: float, pt: CompuCell.Point3D)
    * Use a fixed flux condition on a surface of a volume
    * ``field_name``: name of the field
    * ``surface_name``: name of the surface
    * ``outward_val``: value of the flux, oriented outward from the volume
    * ``pt``: location of the volume
* useFixedConcentration(field_name: string, surface_name: string, conc_val: float, pt: CompuCell.Point3D)
    * Use a fixed concentration condition on a surface of a volume
    * ``field_name``: name of the field
    * ``surface_name``: name of the surface
    * ``conc_val``: value of the concentration on the surface
    * ``pt``: location of the volume
* useFixedFVConcentration(field_name: string, conc_val: float, pt: CompuCell.Point3D)
    * Use a fixed concentration condition in a volume
    * ``field_name``: name of the field
    * ``surface_name``: name of the surface
    * ``conc_val``: value of the concentration in the volume
    * ``pt``: location of the volume

The RDFVM solver also provides methods for setting cell-based model parameters for transport laws,
which are applied according to the transport laws and boundary conditions of each volume occupied
by a cell,

* getCellDiffusivityCoefficient(cell: CompuCell.CellG, field_name: string)
    * Get the diffusion coefficient of a cell for a field
    * ``cell``: a cell
    * ``field_name``: name of the field
    * Returns (``float``): value of diffusion coefficient
* setCellDiffusivityCoefficient(cell: CompuCell.CellG, field_name: string, diffusion_coefficient: float)
    * Set the diffusion coefficient of a cell for a field
    * ``cell``: a cell
    * ``field_name``: name of the field
    * ``diffusion_coefficient``: value of the diffusion coefficient
* getPermeableCoefficients(cell: CompuCell.CellG, ncell_type: int, field_name: string)
    * Get the permeation coefficient and bias coefficient of a cell for permeable membrane transport with neighbor cells of a type
    * ``cell``: a cell
    * ``ncell_type``: type ID of the type of neighbor cells
    * ``field_name``: name of the field
    * Returns (``float``, ``float``): permeation and bias coefficients
* getPermeableCoefficients(cell: CompuCell.CellG, ncell: CompuCell.CellG, field_name: string)
    * Get the permeation coefficient of a cell and bias coefficients of a cell and a neighboring cell for permeable membrane transport with a neighboring cell
    * ``cell``: a cell
    * ``ncell``: a neighbor cell
    * ``field_name``: name of the field
    * Returns (``float``, ``float``, ``float``): permeation coefficient and bias coefficients of a cell, and bias coefficient of a neighboring cell
* setCellPermeationCoefficient(cell: CompuCell.CellG, ncell_type: int, field_name: string, permeation_coefficient: float)
    * Set the permeation coefficient of a cell for permeable membrane transport with neighbor cells of a type
    * ``cell``: a cell
    * ``ncell_type`` type ID of the type of neighbor cells
    * ``field_name``: name of the field
    * ``permeation_coefficient``: value of the permeation coefficient
* setCellPermeableBiasCoefficient(cell: CompuCell.CellG, ncell_type: int, field_name: string, bias_val: float)
    * Set the bias coefficient of a cell for permeable membrane transport with neighbor cells of a type
    * ``cell``: a cell
    * ``ncell_type``: type ID of the type of neighbor cells
    * ``field_name``: name of the field
    * ``bias_val``: value of the bias coefficient
