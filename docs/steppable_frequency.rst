How to Stop Steppables or Adjust Frequency
===========================================================================================================


Adjust Steppable Frequency
--------------------------------------

When you create a steppable using Twedit++, the editor will write template
steppable code and register it in the main Python
script. By default, the steppable will run every Monte Carlo Step (MCS) 
as shown by ``frequency=1``.
You can increase the frequency of nonessential code like a chart update steppable or cell death handler to improve performance since that code could be called less often.

.. code-block:: python

    from cellsortingSteppables import cellsortingSteppable

    CompuCellSetup.register_steppable(steppable=cellsortingSteppable(frequency=1))

We can change ``frequency`` argument to any non-negative value ``N`` to ensure
that our steppable gets called every ``N`` MCS.

Adjust Steppable Frequency During Simulation
-----------------------------------------------------

For some projects, it may happen that you initially want to
call a steppable, say, every 50 MCS but later slow it down to every 500 MCS or not call it at all. 
In such a case, all you need to do is to put the following code in the step
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

How to Stop a Simulation On Demand
---------------------------------------

Place the following code using Twedit++'s helper menu ``CC3D Python->Simulation->Stop Simulation`` anywhere in the steppable.

.. code-block:: python

    self.stop_simulation()

The inverse situation may also occur – you want to run a simulation for more
MCS than originally planned.

In this case you use (``CC3D Python->Simulation->SetMaxMCS``)

.. code-block:: python

    self.set_max_mcs(100000)

to extend simulation to 100000 MCS.
