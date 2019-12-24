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

In line 1 we import functions from ``os.path`` package that will be used to create paths to files. In line 2 we
import ``CC3DCaller`` class. ``CC3DCaller`` object runs single simulation and returns simulation return value.

.. note::

    Simulation return value is a dictionary. This allows for quite a lot of flexibility. In particular, you are not limited to a single return value but can use multiple return values.

in line 11 we construct a path to to a simulation that returns value This is a simulation that is bundled with CC3D. If
you want to run different simulation you would replace code in line 11 with a direct path to your simulation.
Line 12 defines location where we will write simulation output files (think of it as custom version of
``CC3DWorkspace`` folder that CC3D normally uses for simulation output)

.. note::

    When you rerun your multiple simulations using script above you may want to make sure that simulation output folders are empty to avoid overwriting output from previous runs

In line 16 we construct a lit of simulations we want to run. Notice that we use Pythonic syntax to create a list with
multiple copies of the same element. ``[simulation_fname] * number_of_runs`` constructs a list where ``simulation_fname``
is repeated ``number_of_runs`` times.

in line 18 we create a list that will hold results. Line 19 starts a loop where we iterate over simulation paths we
stored in ``sim_fnames`` list.

In line 20 we create ``CC3DCaller`` object where we pass simulation name, screenshot output frequency, output directory
for this specific simulation and a tag (identifier) that is used to identify return results. In our case we we use
integer number ``i`` as identifier but you can be more creative. Finally in line 27 we execute simulation and get
return value of the simulation and in line 28 is appended to ``ret_values``.
Line 30 prints return values.

If we run this script the output of print statement in line 30 will look something like (because we use ``random()``
function we do not know exact outputs):

.. code-block:: console

    return values [{'tag': 0, 'result': 200.8033875687598}, {'tag': 1, 'result': 200.6628249954859}, {'tag': 2, 'result': 200.6617630355885}, {'tag': 3, 'result': 200.30450775355195}]

Notice that a single simulation returns a dictionary as a result. For example simulation with tag ``1`` returned
``{'tag': 1, 'result': 200.6628249954859}``. By "consuming" this dictionary in Python we can extract identifier using
``ret_values[1]['tag']`` syntax and if we want to get the result we would use ``ret_values[1]['result']``.

Notice that in this example ``ret_values[1]['result']`` is a floating point number but you can write your simulation
in such a way that the result can be another dictionary where you could return multiple values.

Applications
~~~~~~~~~~~~

We mentioned it at the beginning , but the examples we are showing here are only to illustrate a technique of how to
call CC3D engine from Python script. Executing several simulations inside a Python loop is not that exciting but
coupling it to an optimization algorithm or sensitivity analysis script is actually more practical. We will add those
more advanced capabilities top CC3D in upcoming releases but for now we want to give you ability explore those avenues
on your own without worrying too much about technical details of calling  CC3D from a script. Simply, use above script
and modify it according to your needs.

Step 3
~~~~~~

In order to run above script you need to set up few environment variables and, in particular, specify location of
appropriate Python interpreter. This must be a Python interpreter that is either shipped with CC3D binary distribution
or a one that you used to compile CC3D against. Let's get started. We will walk you steps necessary to run above scripts on
various platforms. For your convenience we provide simple scripts where you specify two paths (CC3D installation path
and Path to Python interpreter) and then the script takes care of setting your environment

Let's start with windows.

Windows
~~~~~~~

Go to ``CompuCell3D/core/Demos/CallableCC3D/environment_var_setters/cc3d_caller_env_var_set_windows.bat`` and open it
in your editor and you will see the following content:

.. code-block:: console

    @ECHO OFF
    @SET PREFIX_CC3D=<path to where cc3d is installed>
    @SET PYTHON_INSTALL_PATH=<path to where python used for cc3d is installed>
    @SET PYTHONPATH=%PREFIX_CC3D%\lib\site-packages

Replace it with actual paths to where CC3D is installed and to location where python interpreter used with CC#D resides

For example in my case CC3D is installed to ``c:\CompuCell3D-py3-64bit\`` so I modify the script as follows:

.. code-block:: console

    @ECHO OFF
    @SET PREFIX_CC3D=`c:\CompuCell3D-py3-64bit
    @SET PYTHON_INSTALL_PATH=`c:\CompuCell3D-py3-64bit\python36
    @SET PYTHONPATH=%PREFIX_CC3D%\lib\site-packages


I save this script as ``c:\CompuCell3D-py3-64bit\Demos\CC3DCaller\environment_var_setters\win_set_path.bat``. I open
console and execute this script by typing:

.. code-block:: console

    cd \CompuCell3D-py3-64bit\Demos\CC3DCaller\environment_var_setters
    win_set_path.bat

Next I navigate to location where my script from ``Step 2`` is installed

.. code-block:: console

    cd ..\cc3d_call_single_cpu

I replace the line 11 of the script from ``Step 2``

.. code-block:: python

        simulation_fname = join(dirname(dirname(__file__)), 'cellsort_2D', 'cellsort_2D.cc3d')

with

.. code-block:: python

        simulation_fname = r'c:\CompuCell3D-py3-64bit\Demos\CallableCC3D\cellsort_2D\cellsort_2D.cc3d'

Finally, in the console I execute the following:

.. code-block:: console

    python cc3d_call_single_cpu.py

Make sure that you are in the correct directory when you run the last command.