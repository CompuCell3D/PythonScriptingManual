How to Output Energy Changes
======================================================

**EnergyFunctionCalculator**: allows you to output statistical data from the simulation for further analysis. 

You can define this in XML like so:

.. code-block:: xml

        <Potts>
            <Dimensions x="256" y="256" z="1"/>
            <Steps>100000</Steps>
            <Temperature>5</Temperature>
            <NeighborOrder>2</NeighborOrder>
            <EnergyFunctionCalculator Type="Statistics">
                <OutputFileName Frequency="10">statData.txt</OutputFileName>
                <OutputCoreFileNameSpinFlips Frequency="1" GatherResults="" OutputAccepted="" OutputRejected="" OutputTotal=""/>
            </EnergyFunctionCalculator>
        </Potts>

.. note::

    CC3D has the option to run in parallel mode, but
    output from the energy calculator will only work when running in single-CPU mode.

The ``OutputFileName`` tag is used to specify the name of the file to which
CompuCell3D will write average changes in energies returned by each
plugin along with the corresponding standard deviations. 
``Frequency`` controls how often to record this data. In the above example, we would write data every 10 MCS.

Furthermore, the ``OutputCoreFileNameSpinFlips`` tag is used to tell
CompuCell3D to output the energy change for every plugin's pixel-copy operations. 

Finally, ``GatherResults=””`` will ensure
that there is only one file written for accepted (``OutputAccepted``),
rejected (``OutputRejected``), and both accepted and rejected (``OutputTotal``) pixel copies.
If you do not specify ``GatherResults``, CompuCell3D will output
separate files for different MCS's, and depending on the Frequency, you
may end up with many files in your directory.
