PDESolverCaller Plugin
-----------------------

.. warning::

    In most cases you can specify extra calls to PDE solvers in
    the solver itself. Thus this plugin is being deprecated. We mention
    it here for backward compatibility reasons as some of the older CC3D simulations
    may still be using this plugin.

PDE solvers in CompuCell3D are implemented as steppables . This means
that by default they are called every MCS. In many cases this is
insufficient. For example if diffusion constant is large, then explicit
finite difference method will become unstable and the numerical solution
will have no sense. To fix this problem one could call PDE solver many
times during single MCS. This is precisely the task taken care of by
``PDESolverCaller plugin``. The syntax is straightforward:

.. code-block:: xml

    <Plugin Name="PDESolverCaller">
        <CallPDE PDESolverName="FlexibleDiffusionSolverFE"ExtraTimesPerMC="8"/>
    </Plugin>

All you need to do is to give the name of the steppable that implements
a given PDE solver and pass let CompCell3D know how many extra times per
MCS this solver is to be called (here ``FlexibleDiffusionSolverFE`` was ``8``
extra times per MCS).
