Managing CompuCell3D simulations (CC3D project files)
-----------------------------------------------------

Until version ``3.6.0`` CompuCell3D simulations were stored as a combination
of Python, CC3DML (XML), and PIF files. Starting with version
``3.6.0`` we introduced new way of managing CC3D simulations by enforcing
that a single CC3D simulation is stored in a folder containing ``.cc3d``
project file describing simulation resources (.cc3d is in fact XML),
such as CC3DML configuration file, Python scripts, PIF files,
Concentration files *etc…** and a directory called ``Simulation`` where all
the resources reside. The structure of the new-style CC3D simulation is
presented in the diagram below:

**->CellsortDemo**

    CellsortDemo.cc3d

   **->Simulation**

      Cellsort.xml

      Cellsort.py

      CellsortSteppables.py

      Cellsort.piff

      FGF.txt

Bold fonts denote folders. The benefit of using CC3D project files
instead of loosely related files are as follows:

1) Previously users had to guess which file needs to be open in CC3D –
   CC3DML or Python. While in a well written simulation one can link the
   files together in a way that when user opens either one the
   simulation would work but, nevertheless, such approach was clumsy and
   unreliable. Starting with ``3.6.0`` users open ``.cc3d`` file and they don’t
   have to stress out that CompUCell3D will complain with error message.

.. warning::

   The only way to load simulation in CompuCell3D is to use ``.cc3d`` project. We no longer
   support previous ways of opening simulations


2) All the files specified in the .cc3d project files are copied to the
   result output directory along with simulation results (uncles you
   explicitly specify otherwise). Thus, when you run multiple
   simulations each one with different parameters, the copies of all
   CC3DML and Python files are stored eliminating guessing which
   parameters were associated with particular simulations.

3) All file paths appearing in the simulation files are relative paths
   with respect to main simulation folder. This makes simulations
   portable because all simulation resources are contained withing
   single folder. In the example above when referring to ``Cellsort.piff``
   file from ``Cellsort.xml`` you use ``Simulation/Cellsort.piff``. This makes
   simulations easily exchangeable between collaborators

4) New style of storing CC3D simulations has also another advantage – it
   makes graphical management of simulation content and simulation
   generation very easy. As a matetr of fact new component of CC3D suite
   – Twedit++ - CC3D edition has a graphical tool that allows for easy
   project file management and it also has new simulation wizard which
   allows users to build template of CC3D simulation within less than a
   minute.

Let’s now look in detail at the structure of ``.cc3d`` files (we are using XML syntax here):

.. code-block:: xml

   <Simulation version="3.6.0">
       <XMLScript>Simulation/Cellsort.xml</XMLScript>
       <PythonScript>Simulation/Cellsort.py</PythonScript>
       <Resource Type="Python">Simulation/CellsortSteppables.py</Resource>
      <PIFFile>Simulation/Cellsort.piff</PIFFile>
       <Resource Type="Field" Copy="No">Simulation/FGF.txt</Resource>
   </Simulation>

As you can see the structure of the file is quite flat. All that we are
storing there is names of files that are used in the simulation. Two
files have special tags ``<XMLFile>`` which specifies name of the CC3DML
file storing "CC3DML portion" of the simulation and ``<PythonScript>`` which
specifies main Python script. We have also ``<PIFFile>`` tag which is used to
designate PIF files. All other files used in the simulation are referred
to as ``Resources``. For example Python steppable file is a resource of type
"Python" - ``<Resource Type="Python">Simulation/CellsortSteppables.py</Resource>`` .
FGF.txt is a resource of type "Field" - ``<Resource Type="Field" Copy="No">Simulation/FGF.txt</Resource>``.
Notice that all the files are specified using paths relative to main simulation directory i.e. w.r.t to the dir in which
``.cc3d`` file resides

As we mentioned before, when you run ``.cc3d`` simulation all the files
listed in the project file are copied to result folder. If for
some reason you want to avoid coping of some of the files, simply add
``Copy="No"`` attribute in the tag with file name specification for example"

.. code-block:: xml

    <PIFFile Copy="No">Simulation/Cellsort.piff</PIFFile>
    <Resource Type="Field" Copy="No">Simulation/FGF.txt</Resource>

