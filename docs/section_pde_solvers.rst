PDESolvers in CompuCell3D
=========================

One of the most important and time-consuming parts of the CC3D
simulation is to solve all sorts of Partial Differential Equations which
describe behavior of certain simulation objects (usually chemical
fields). Most of the CC3D PDE solvers solve PDE with diffusive terms.
Because we are dealing with moving boundary condition problems it was
easiest and probably most practical to use explicit scheme of Finite
Difference method. Most of CC3D PDE solvers run on multi core
architectures and we also have GPU solvers which run and high
performance GPU’s and they also provide biggest speedups in terms of
performance. Because CC3D solvers were implemented at different CC3D
life cycle and often in response to particular user requests, CC3DML
specification may differ from solver to solver. However, the basic
structure of CC3DML PDE solver code follows similar pattern .

.. toctree::
    :maxdepth: 1

    accessing_concentration_fields_managed_of_pde_solvers
    flexible_diffusion_solver
    diffusion_solver_settings
    diffusion_solver
    advection_diffusion_solver
    fast_diffusion_solver_2D
    kernel_diffusion_solver
    reaction_diffusion_solver
    reaction_diffusion_solver_fvm
    steady_state_diffusion_solver
    fluctuation_compensator_addon