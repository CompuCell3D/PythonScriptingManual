Writing data files in the simulation output directory.
======================================================

Quite often when you run CC3D simulations you need to output data files
where you store some information about the simulation. When CC3D saves
simulation snapshots it does so in the special directory which is
created automatically and whose name consists of simulation core name
and timestamp. By default, CC3D creates such directories as subfolders
of ``<your_home_directory>/CC3DWorkspace``. You can redefine the location
of CC3D output in the Player. If standard simulation output is placed in
a special directory it makes a lot of sense to store your custom data
files in the same directory. The following code snippet shows you how to
accomplish this (the code to open file in the simulation output
directory can be inserted from Twedit++ - simply go to ``CC3D Python->Python Utilities``):

.. code-block:: python

    def step(self,mcs):
        fileName='myOutput+'+str(mcs)+'.txt'
        try:
            fileHandle,fullFileName\
            =self.openFileInSimulationOutputDirectory(fileName,"w")
        except IOError:
            print "Could not open file ", fileName," for writing. "
            return

        for cell in self.cellListByType(self.NONCONDENSING):
            print >>fileHandle, 'cell.id=',cell.id,'volume=',cell.volume

        fileHandle.close()

In the step function we create fileName by concatenating ``'myOutput'``,
current MCS - str(mcs), and extension ``'.txt'``. Inside ``try/except``
statement (refresh you knowledge about Python exceptions) we call
``self.openFileInSimulationOutputDirectory`` function where first argument
is file name and second argument is file open mode. Since we are opening
file for writing we use ``"w"`` . To open file in the read mode we would use
``"r"``. Please consult appropriate chapter from Python programing manual
for more information about file modes. If CC3D fails to open file in the
simulation directory we print error message and return from step function.
If the file open operation is successful we iterate over all cells of
type NonCondensing and print cell id and cell current volume. Notice
that when writing to a file in Python we have to use

.. code-block:: python

    print >>fileHandle

syntax. The reminder of this print statemnt looks exactly as a regular
print statement. Alternatively we can use the following syntax to write
to a file:

.. code-block:: python

    fileHandle.write('formatting string' %(values for formatting string))

The formatting string contains regular text and formatting characters
such as ``\n`` denoting end of line, %d denoting integer number, ``%f``
denoting floating point number and %s denoting strings. For more
information on this topic please see any Python manual or see online
Python documentation.

After we are done with writing we close the file which ensures that file
buffers are transferred to a disk. Do not forget to close the file after
you are done writing.

Notice that with self.openFileInSimulationOutputDirectory function we do
not need to know the actual nameof the output directory. This makes
things much easier than if we had to construct full file path. If you
would prefer to store your files in a separate subfolder of the
simulation directory all you have to do is to prepend filename with
the name of the subfolder followed by ``/``. For example the following
statement:

``self.openFileInSimulationOutputDirectory('OUTPUT_SUBFOLDER/myoutput.txt','w')``

creates subfolder called ``OUTPUT_SUBFOLDER`` inside simulation output
directory and inside this subfolder it opens file myoutput.txt for
writing. You can replace ``OUTPUT_SUBFOLDER` with any partial path e.g.
``OUTPUT/TXT_FILES`` and CC3D will make sure that all directories specified
in the partial paths get created. This greatly simplifies file output
operations in the CC3D.
