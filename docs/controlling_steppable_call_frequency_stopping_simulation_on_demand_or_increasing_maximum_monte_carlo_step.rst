Controling steppable call frequency. Stopping simulation on demand or increasing maximum Monte Carlo Step.
===========================================================================================================

When you create steppable using Twedit++, the editor will plunk template
steppable code and will register this steppable in the main Python
script. By default such steppable will be called after each completed
MCS – as code snippet below shows:

.. code-block:: python

    from cellsortingSteppables import cellsortingSteppable

    steppableInstance = cellsortingSteppable(sim, _frequency=1)
    steppableRegistry.registerSteppable(steppableInstance)

We can change ``_frequency`` argument to any non-negative value ``N`` to ensure
that our steppable gets called every ``N`` MCS.

Sometimes in the simulation it may happen that initially you want to
call steppable, say, every 50 MCS but later as the simulation goes on
you may want to call it every 500 MCS or not call it at all. In such a
case all you need to to is to put the following code in the step
function:

.. code-block:: python

    def step(self,mcs):
        ...
        if mcs > 10000:
            self.frequency = 500

This will ensure that after ``MCS = 10000`` the steppable will be called every
500 MCS. If you want to disable steppable completely, you can always set
frequency to a number that is greater than MCS and this would do the
trick.

On few occasions instead of waiting for a simulation to go through all
MCS’s you may have a metric determining if it is sensible to continue
simulation or not. In case you want to stop simulation on demand. CC3D
has useful function call that does exactly that. Place the following
code (``CC3D Python->Simulation->Stop Simulation``)

.. code-block:: python

    self.stopSimulation()

anywhere in the steppable and after this call simulation will get
stopped.

Inverse situation may also occur – you want to run simulation for more
MCS than originally planned.

In this case you use (``CC3D Python->Simulation->SetMaxMCS``)

.. code-block:: python

    self.setMaxMCS(100000)

to extend simulation to 100000 MCS.
