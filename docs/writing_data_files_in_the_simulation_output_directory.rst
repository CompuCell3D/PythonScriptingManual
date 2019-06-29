Writing data files in the simulation output directory.
======================================================

Quite often when you run CC3D simulations you need to output data files
where you store some information about the simulation. When CC3D saves
simulation snapshots it does so in the special directory which is
created automatically and whose name consists of simulation core name
and timestamp. By default, CC3D creates such directories as subfolders
of ``<your_home_directory>/CC3DWorkspace``. You can redefine the location
of CC3D output in the Player or from the command line. If standard simulation output is placed in
a special directory it makes a lot of sense to store your custom data
files in the same directory. The following code snippet shows you how to
accomplish this (the code to open file in the simulation output
directory can be inserted from Twedit++ - simply go to ``CC3D Python->Python Utilities``):

.. code-block:: python

    def step(self, mcs):

        output_dir = self.output_dir

        if output_dir is not None:
            output_path = Path(output_dir).joinpath('step_' + str(mcs).zfill(3) + '.dat')
            with open(output_path, 'w') as fout:

                attr_field = self.field.ATTR
                for x, y, z in self.every_pixel():
                    fout.write('{} {} {} {}\n'.format(x, y, z, attr_field[x, y, z]))

In the step function we create ``output_path`` by concatenating ``output_dir`` with a string
that contains word ``step_`` , current mcs (zero-filled up to 3 positions - note how we use standard string
function ``zfill``) and extension ``.dat``

.. note::

    ``self.output_dir`` is a special variable in each steppable that stores directory where the output
of the current simulation will be written.

.. note::

    Path concatenation in ``Path(output_dir).joinpath(...)`` is done using standard Python package ``pathlib``. we import this functionality using ``from pathlib import Path``


Next, we open file using ``with`` statement - if you are unfamiliar with this way of interacting with files in Python
 please check new Python tutorials online:

.. code-block:: python

    with open(output_path, 'w') as fout:
        # file is open at this point and there is no need to close it
        # because "with" statement will take care of it automatically
        ...

Inside ``with`` statement (where the file is open) we access chemical field ``ATTR`` and use ``self.every_pixel``
operator to access and write field values to the file:

.. code-block:: python

    with open(output_path, 'w') as fout:

        attr_field = self.field.ATTR
        for x, y, z in self.every_pixel():
            fout.write('{} {} {} {}\n'.format(x, y, z, attr_field[x, y, z]))


If we want to create directory inside simulaiton output folder we can use the following functionality of pathlib

.. code-block:: python

    new_dir = Path(self.output_dir).joinpath('new_dir/new_subdir')
    new_dir.mkdir(exist_ok=True, parents=True)

We first create path to the new directory using pathlib's ``Path`` object and its ``joinpath`` method. and then use
``Path``'s method  ``mkdir`` to create directory. The ``exist_ok=True, parents=True`` arguments ensure that the function will not crash if the directory already exists and all the paths along directory path will be created as needed (``parents=True``). In our case it means that ``new_dir`` and ``new_subdir`` will be created. ``self.output_dir`` will be created as well but in a different place by the CC3D simulation setup code.