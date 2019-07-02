Changing number of Worknodes
============================

CompuCell3D allows multi-core executions of simulations. We use
checker-board algorithm to deal with the CPM part of the simulation.
This algorithm restricts minimum partition size. As a rule of thumb, if
you have cells that are large or are fragmented and spread out
throughout the lattice, you should not use multiple cores. If your cells
are relatively small using multiple cores can give you substantial boost
in terms of simulation run times. But what does a small cell mean? If we
are on a ``100 x 100`` lattice and cells have approx. 5-7 pixels in “diameter”
then if we use 4 cores then each core will be responsible for ``50 x 50``
piece of the lattice. This is much bigger than our cell. However as we
increase number of cores it may happen that lattice area processed by a
single core is comparable in size to a single cell. This is a recipe for
disaster. In such a case two (or more) CPUs may modify attributes of the
same cell at the same time. This is known as race condition and CC3D
does not provide any protection against such situation. The reason CC3D
leaves it up to the user to ensure that race conditions do not occur is
performance – protecting against race conditions would lead to slower
code putting in question the whole effort to parallelize CC3D.

PDE solvers used in CC3D don’t exhibit any side effects associated with
increasing number of cores. As a matter of fact parallelizing PDE
solvers provides the biggest boost to the simulation. We estimate that
with 3-4 diffusing fields in the simulation, CC3D spends 80-90% of its
runtime solving PDEs.

An example, ``DynamicNumberOfProcessors`` in ``Demos/SimulationSettings``
demonstrates how to change number of CPUs used by the simulation:

.. code-block:: python

    from cc3d.core.PySteppables import *


    class DynamicNumberOfProcessorsSteppable(SteppableBasePy):

        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):
            if mcs == 10:
                self.resize_and_shift_lattice(new_size=(400, 400, 1), shift_vec=(100, 100, 0))

            if mcs == 100:
                self.change_number_of_work_nodes(8)


At ``MCS = 10`` we resize the lattice and shift its content and at ``MCS = 100`` we
change number of CPU’s to 8. Actually what we do here is we chane number
of computational threads to 8 and it is up to operating system to
assign those threads to different processors. When we have 8 processors
usually operating system will try to use all 8 CPU’s In case our CPU
count is lower some CPU’s will execute more than one computational CC3D
thread and this will give lower performance compared to the case when
each CPU handles one CC3D thread.

As usual Twedit++ offers help in pasting template code ,simply go to
``CC3D Python->Simulation`` menu and choose appropriate option.
