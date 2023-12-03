Instabilities of the Forward Euler Method
------------------------------------------

Most of the PDE solvers in CC3D use Forward Euler explicit numerical
scheme. This method is unstable for large diffusion constant. As a
matter of fact using D=0.25 with pulse initial condition will lead to
instabilities in 2D. To deal with this you would normally use implicit
solvers however due to moving boundary conditions that we have to deal
with in CC3D simulations, memory requirements, performance and the fact
that most diffusion constants encountered in biology are quite low
(unfortunately this is not for all chemicals e.g. oxygen ) we decided to
use explicit scheme. If you have to use large diffusion constants with
explicit solvers you need to do rescaling:

1) Set D, Δt, Δx according to your model

2) If

.. math::
   :nowrap:

   \begin{eqnarray}
        D\frac{\Delta t}{\Delta x^2}>0.16 {\text     in 3D}
   \end{eqnarray}

you will need to to call solver multiple times per MCS.

3) Set ``<ExtraTimesPerMCS>`` to N-1 where:

.. math::
   :nowrap:

   \begin{eqnarray}
        ND' = D
   \end{eqnarray}

and

.. math::
   :nowrap:

   \begin{eqnarray}
        D\frac{\Delta t/N}{\Delta x^2} < 0.16 {\text     in 3D}
   \end{eqnarray}

Initial Conditions
-------------------

We can specify initial concentration as a function of ``x``, ``y``, ``z``
coordinates using ``<InitialConcentrationExpression>`` tag we use ``muParser``
syntax to type the expression. Alternatively we may use
``ConcentrationFileName`` tag to specify a text file that contains values of
concentration for every pixel:

.. code-block:: xml

    <ConcentrationFileName>initialConcentration2D.txt</ConcentrationFileName>

The value of concentration of the last pixel read for a given cell
becomes an overall value of concentration for a cell. That is if cell
has, say ``8`` pixels, and you specify different concentration at every
pixel, then cell concentration will be the last one read from the file.

**Concentration file format** is as follows:

.. code-block:: xml

    *x y z c*

where ``x`` , ``y`` , ``z`` , denote coordinate of the pixel. ``c`` is the value of the
concentration.

**Example:**

.. code-block:: xml

    0 0 0 1.2

    0 0 1 1.4

    ...

The initial concentration can also be input from the Python script
(typically in the start function of the steppable) but often it is more
convenient to type one line of the CC3DML script than few lines in
Python.

Boundary Conditions
-------------------

All standard solvers (``Flexible``, ``Fast``, and ``ReactionDiffusion``) by default
use the same boundary conditions as the GGH simulation (and those are
specified in the Potts section of the CC3DML script). Users can,
however, override those defaults and use customized boundary conditions
for each field individually. Currently CompuCell3D supports the
following boundary conditions for the diffusing fields: periodic,
constant value (Dirichlet) and constant derivative (von Neumann). To
specify custom boundary condition we include <BoundaryCondition> section
inside ``<DiffusionField>`` tags.

The ``<BoundaryCondition>`` section describes boundary conditions along
particular axes. For example:

.. code-block:: xml

    <Plane Axis="X">
        <ConstantValue PlanePosition="Min" Value="10.0"/>
        <ConstantValue PlanePosition="Max"  Value="10.0"/>
    </Plane>

specifies boundary conditions along the ``x`` axis. They are Dirichlet-type
boundary conditions. ``PlanePosition='Min"`` denotes plane parallel to ``yz``
plane passing through ``x=0``. Similarly ``PlanePosition="Min"`` denotes plane
parallel to ``yz`` plane passing through ``x=fieldDimX-1`` where ``fieldDimX`` is ``x``
dimension of the lattice.

By analogy we specify constant derivative boundary conditions:

.. code-block:: xml

    <Plane Axis="Y">
        <ConstantDerivative PlanePosition="Min" Value="10.0"/>
        <ConstantDerivative PlanePosition="Max" Value="10.0"/>
    </Plane>

We can also mix types of boundary conditions along single axis:

.. code-block:: xml

    <Plane Axis="Y">
        <ConstantDerivative PlanePosition="Min" Value="10.0"/>
        <ConstantValue PlanePosition="Max" Value="0.0"/>
    </Plane>

Here in the ``xz`` plane at ``y=0`` we have von Neumann boundary conditions but
at ``y=fieldFimY-1`` we have dirichlet boundary condition.

To specify periodic boundary conditions along, say, ``x`` axis we use the
following syntax:

.. code-block:: xml

    <Plane Axis="X">
        <Periodic/>
    </Plane>

Notice, that ``<Periodic>`` boundary condition specification applies to both
"ends" of the axis *i.e.* we cannot have periodic boundary conditions at
``x=0`` and constant derivative at ``x=fieldDimX-1``.

