Direct Call to CompuCell3D from Python
=======================================

In a typical situation, you will most often run CC3D using GUI. You create simulation, run it, look at the results,
modify parameters, run again and the process continues. But what if you would like to be more "methodical" in
finding optimal parameters? The new CC3D comes with a convenience module that allows you to directly call CC3D as
a Python function and get return value(s) from your simulations. As you can tell already, functionality like this
allows you to use various optimization packages and be able to find desired set of parameters for your simulation
- assuming you know how to define a proper metrics.

How does it work?
-----------------

.. note::

    All examples from this section can be found in ``Demos/CallableCC3D``

Step 1
~~~~~~

If you want to call CC3D engine from a Python function and get return value you need to modify your existing
simulation to return such value. This is a very easy step - take a look at he code below:

.. code-block:: python

    from cc3d.core.PySteppables import *
    from cc3d import CompuCellSetup
    from random import random


    class CellsortSteppable(SteppableBasePy):
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)

        def start(self):
            pass

        def step(self, mcs):
            if mcs == 100:
                pg = CompuCellSetup.persistent_globals
                pg.return_object = 200.0 + random()


This is a "regular" steppable. The only new part is the line where we modify
``CompuCellSetup.persistent_globals.return_object``. This variable that will persist even after simulation is finished
is the way we pass simulation return value to the caller. Here, our return value is set to be a sum of number ``200.0``
and a random number between 0 and 1. This return value can be set at any point in the simulation.
In particular it often makes sense to set it in the ``finish`` function, but for illustration purposes we set it in
``step`` function. When accessing persistent_globals object , do not forget to include necessary import:
``from cc3d import CompuCellSetup``

Step 2
~~~~~~

Once we have a simulation we need to write a Python script from which we will call our value-returning simulations.
We will first show a minimal example where we call CC3D from Python script few times and store return values of each
simulation in a list. Here is the code:

.. code-block:: python
    :linenos:

    from os.path import dirname, join, expanduser
    from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller


    def main():

        number_of_runs = 4

        # You may put a direct path to a simulation of your choice here and comment out simulation_fname line below
        # simulation_fname = <direct path your simulation>
        simulation_fname = join(dirname(dirname(__file__)), 'cellsort_2D', 'cellsort_2D.cc3d')
        root_output_folder = join(expanduser('~'), 'CC3DCallerOutput')

        # this creates a list of simulation file names where simulation_fname is repeated number_of_runs times
        # you can create a list of different simulations if you want.
        sim_fnames = [simulation_fname] * number_of_runs

        ret_values = []
        for i, sim_fname in enumerate(sim_fnames):
            cc3d_caller = CC3DCaller(
                cc3d_sim_fname=sim_fname,
                screenshot_output_frequency=10,
                output_dir=join(root_output_folder,f'cellsort_{i}'),
                result_identifier_tag=i
            )

            ret_value = cc3d_caller.run()
            ret_values.append(ret_value)

        print('return values', ret_values)


    if __name__ == '__main__':
        main()

In the first