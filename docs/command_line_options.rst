Command line options of CompuCell3D
-----------------------------------

Although most users run CC3D using Player GUI sometimes it is very
convenient to run CC3D using command line options. CC3D allows to invoke
Player directly from command line which is convenient because if saves
several clicks and if you run many simulations this might be quite
convenient.

**Remark:** On Windows we use .bat extension for run scripts and on
Linux/OSX it is .sh. Otherwise all the material in this section applies
to all the platforms.

CompuCell3D Player Command Line Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The command line options for running simulation with the player are as
follows:

.. code-block:: bash

   compucell3d.bat [options]

Options are:

``-i <simulation file>`` - users specify ``.cc3d`` simulation file they want to run.

``-s <screenshotDescriptionFileName>`` - name of the file containing
description of screenshots to be taken with the simulation. Usually this
file is prepared using Player by switching to different views, clickin
camera button and saving screenshot description file from the Player
File menu.

``-o <customScreenshotDirectoryName>`` - allows users to specify where
screenshots will be written. Overrides default settings.

``--noOutput`` - instructs CC3D not to store any screenshots. Overrides
Player settings.

``--exitWhenDone`` - instructs CC3D to exit at the end of simulation.
Overrides Player settings.

``-h``, ``--help`` - prints command line usage on the screen

Example command may look like (windows):

.. code-block:: bash

   compucell3d.bat –i Demos\Models\cellsort\cellsort_2D\cellsort_2d.cc3d --noOutput

or on linux:

.. code-block:: bash

   compucell3d.sh –i Demos/Models/cellsort/cellsort_2D/cellsort_2d.cc3d --noOutput

and OSX:

.. code-block:: bash

   compucell3d.command –i Demos/Models/cellsort/cellsort_2D/cellsort_2d.cc3d --noOutput


Running CompuCell3D in a GUI-Less Mode - Command Line Options.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes when you want to run CC3D on a cluster you will have to use
runScript.bat which allows running CC3D simulations without invoking
GUI. However, all the screenshots will be still stored.

**Remark:** current version of this script does not handle properly
relative paths so it has to be run from the installation directory of
CC3D i.e. you have to cd into this directory prior to runnit
runScript.bat. Another solution is to use full paths.

The output of this script is in the form of vtk files which can be
subsequently replayed in the Player (and one can take screenshots then).
By default all fields present in the simulation are stored in the vtk
file. If users want to remove some of the fields from being stored in
the vtk format they have to pass this information in the Python script:

.. code-block:: python

   CompuCellSetup.doNotOutputField(_fieldName)


Storing entire fields (as opposed to storing screenshots) preserves
exact snapshots of the simulation and allows result postprocessing. In
addition to the vtk files runScript stores lattice description file with
``.dml``` extension which users open in the Player (``File->Open Lattice Description Summary File…``)
if they want to reply generated vtk files.

The format of the command (windows):

.. code-block:: bash

   runScript.bat [options]

linux:

.. code-block:: bash

   runScript.sh [options]

OSX:

.. code-block:: bash

   runScript.command [options]


The command line options for runScript.bat are as follows:

``-i <simulation file>`` - users specify ``.cc3d`` simulation file they want to run.

``-c <outputFileCoreName>`` - allows users to specify core name for the vtk
files. The default name for vtk files is ``Step``

``-o <customVtkDirectoryName>`` - allows users to specify where vtk files
and the .dml file will be written. Overrides default settings

``-f <frequency>`` or ``–outputFrequency=<frequency>`` - allows to specify how
often vtk files are stored to the disk. Those files tend to be quite
large for bigger simulations so storing them every single MCS (default
setting) slows down simulation considerably and also uses a lot of disk
space.

``--noOutput`` - instructs CC3D not to store any output. This option makes
little sense in most cases.

``-h``, ``--help`` - prints command line usage on the screen

Example command may look as follows(windows):

.. code-block:: bash

   runScript.bat –i Demos\CompuCellPythonTutorial\InfoPrinter\cellsort_2D_info_printer.cc3d –f 10 –o Demos\CompuCellPythonTutorial\InfoPrinter\screenshots –c infoPrinter

linux:

.. code-block:: bash

   runScript.sh –i Demos/CompuCellPythonTutorial/InfoPrinter/cellsort_2D_info_printer.cc3d –f 10 –o Demos/CompuCellPythonTutorial/InfoPrinter/screenshots –c infoPrinter


osx:

.. code-block:: bash

   runScript.command –i Demos/CompuCellPythonTutorial/InfoPrinter/cellsort_2D_info_printer.cc3d –f 10 –o Demos/CompuCellPythonTutorial/InfoPrinter/screenshots –c infoPrinter
