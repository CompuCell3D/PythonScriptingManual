Fluctuation Compensator Solver Add-On
-------------------------------------

Fluctuation Compensator is an optional PDE solver add-on introduced in v4.1.2
to account for Metropolis surface fluctuations in field solutions in both a
feasible and sensible way. The algorithm is based on that which is described
by Marée et. al [1]_ and imposes total mass conservation in all cellular domains
and the medium over the spin flips of a Monte Carlo step. The algorithm does not
impose advection by domain deformation, but rather homogeneously applies a
correction factor in each subdomain to all field solutions of a solver such that
the total amount of each simulated species in each subdomain is unchanged over all
spin flips.

The Fluctuation Compensator algorithm consists of the following three rules.

1. **Rule 1 (mass conservation)**: In each subdomain, the total amount of each
   species is unchanged over an arbitrary number of spin flips.

2. **Rule 2 (uniform correction)**: Corrections applied to values in each subdomain so to
   impose mass conservation are uniformly applied.

3. **Rule 3 (Neumann condition)**: The amount of species in the copying site of a spin
   flip are exactly copied to the site of the flip.

.. note::

   Fluctuation Compensator is supported in DiffusionSolverFE, ReactionDiffusionSolverFE and ReactionDiffusionSolverFVM.

Exactly one Fluctuation Compensator can be attached to each supported solver instance.
An attached Fluctuation Compensator performs corrections on *all* fields of the solver
to which it is attached. A Fluctuation Compensator can be attached to a solver in
CC3DML using the tag ``<FluctuationCompensator/>`` at the level of field specification.
For example, to attach a Fluctuation Compensator to a simple use-case with
DiffusionSolverFE might look like the following.

.. code-block:: xml

    <Steppable Type="DiffusionSolverFE">
        <FluctuationCompensator/>
        <DiffusionField Name="ATTR"/>
    </Steppable>


Demos showing basic usage and comparison are available in
``Demos/SteppableDemos/FluctuationCompensator``.

.. Note::

   PDE solution field values can be modified outside of the solver routines without
   invalidating the correction factors of Fluctuation Compensators *so long as*
   they are notified that field values have been modified. The CompuCell3D library has
   a convenience method to do exactly this: ``updateFluctuationCompensators``. Call this
   method after modifying field values and before the next PDE solution step to refresh
   Fluctuation Compensators according to your changes.

.. [1]
   Marée, Athanasius FM, Verônica A. Grieneisen, and Leah Edelstein-Keshet.
   "How cells integrate complex stimuli: the effect of feedback from phosphoinositides
   and cell shape on cell polarization and motility." PLoS Computational Biology 8.3 (2012).
