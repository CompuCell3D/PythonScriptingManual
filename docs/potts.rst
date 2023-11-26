Potts Section
--------------

The first section of the .xml file defines the global parameters of the
lattice and the simulation.

.. code-block:: xml

        <Potts>
            <Dimensions x="101" y="101" z="1"/>
            <Anneal>0</Anneal>
            <Steps>1000</Steps>
            <FluctuationAmplitude>5</FluctuationAmplitude>
            <Flip2DimRatio>1</Flip2DimRatio>
            <Boundary_y>Periodic</Boundary_y>
            <Boundary_x>Periodic</Boundary_x>
            <NeighborOrder>2</NeighborOrder>
            <DebugOutputFrequency>20</DebugOutputFrequency>
            <RandomSeed>167473</RandomSeed>
            <EnergyFunctionCalculator Type="Statistics">
                <OutputFileName Frequency="10">statData.txt</OutputFileName>
                <OutputCoreFileNameSpinFlips Frequency="1" GatherResults="" OutputAccepted="" OutputRejected="" OutputTotal=""/>
            </EnergyFunctionCalculator>
        </Potts>



This section appears at the beginning of the configuration file. Line
``<Dimensions x="101" y="101" z="1"/>`` declares the dimensions of the
lattice to be``101 x 101 x 1``, *i.e.*, the lattice is two-dimensional and
extends in the ``xy`` plane. The basis of the lattice is ``0`` in each
direction, so the ``101`` lattice sites in the ``x`` and ``y`` directions have
indices ranging from ``0`` to ``100``. ``<Steps>1000</Steps>`` tells CompuCell how
long the simulation lasts in MCS. After executing this number of steps,
CompuCell can run simulation at zero temperature for an additional
period. In our case it will run for ``<Anneal>10</Anneal>`` extra steps.
``FluctuationAmplitude`` parameter determines intrinsic fluctuation or
motility of cell membrane.

.. note::

   ``FluctuationAmplitude`` is a ``Temperature``
   parameter in classical GGH model formulation. We have decided to use
   ``FluctuationAmplitude`` term instead of temperature because using word
   ``Temperature`` to describe intrinsic motility of cell membrane was quite
   confusing.

In the above example, fluctuation amplitude applies to all cells in the
simulation. To define fluctuation amplitude separately for each cell
type we use the following syntax:

.. code-block:: xml

    <FluctuationAmplitude>
        <FluctuationAmplitudeParameters CellType="Condensing" FluctuationAmplitude="10"/>
        <FluctuationAmplitudeParameters CellType="NonCondensing" FluctuationAmplitude="5"/>
    </FluctuationAmplitude>



When CompuCell3D encounters expanded definition of ``FluctuationAmplitude``
it will use it in place of a global definition –

.. code-block:: xml

    <FluctuationAmplitude>5</FluctuationAmplitude>

To complete the picture CompuCell3D allows users to set fluctuation
amplitude individually for each cell. Using Python scripting we write:

.. code-block:: python

    for cell in self.cellList:
        if cell.type==1:
            cell.fluctAmpl=20



When determining which value of fluctuation amplitude to use, CompuCell
first checks if ``fluctAmpl`` is non-negative. If this is the case it will
use this value as fluctuation amplitude. Otherwise it will check if
users defined fluctuation amplitude for cell types using expanded CC3DML
definition and if so it will use those values as fluctuation amplitudes.
Lastly, it will resort to globally defined fluctuation amplitude
(``Temperature``). Thus, it is perfectly fine to use ``FluctuationAmplitude``
CC3DML tags and set ``fluctAmpl`` for certain cells. In such a case
CompuCell3D will use ``fluctAmpl`` for cells for which users defined it and
for all other cells it will use values defined in the CC3DML.

In GGH model, the fluctuation amplitude is determined taking into
account fluctuation amplitude of *"source"* (expanding) cell and
*"destination"* (being overwritten) cell. Currently CompuCell3D supports 3
type functions used to calculate resultant fluctuation amplitude (those
functions take as argument fluctuation amplitude of "source" and
*"destination"* cells and return fluctuation amplitude that is used in
calculation of pixel-copy acceptance). The 3 functions are ``Min``, ``Max``, and
``ArithmeticAverage`` and we can set them using the following option of the
Potts section:

.. code-block:: xml

    <Potts>
         <FluctuationAmplitudeFunctionName>Min</FluctuationAmplitudeFunctionName>
         …
    </Potts>

By default we use ``Min`` function. Notice, that if you use global
fluctuation amplitude definition ``Temperature`` it does not really matter
which function you use. The differences arise when *"source"* and
*"destination"* cells have different fluctuation amplitudes.

The above concepts are best illustrated by the following example:

.. code-block:: xml

 <Potts>
   <Dimensions x="100" y="100" z="1"/>
   <Steps>10000</Steps>
   <FluctuationAmplitude>5</FluctuationAmplitude>
   <FluctuationAmplitudeFunctionName>ArithmeticAverage</FluctuationAmplitudeFunctionName>
   <NeighborOrder>2</NeighborOrder>
 </Potts>


Where in the CC3DML section we define global fluctuation amplitude and
we also use ``ArithmeticAverage`` function to determine resultant
fluctuation amplitude for the pixel copy.

In python script we will periodically set higher fluctuation amplitude
for lattice quadrants so that when running the simulation we can see
that cells belonging to different lattice quadrants have different
membrane fluctuations:

.. code-block:: python

    class FluctuationAmplitude(SteppableBasePy):
        def __init__(self, _simulator, _frequency=1):
            SteppableBasePy.__init__(self, _simulator, _frequency)

            self.quarters = [[0, 0, 50, 50], [0, 50, 50, 100], [50, 50, 100, 100], [50, 0, 100, 50]]

            self.steppableCallCounter = 0

        def step(self, mcs):

            quarterIndex = self.steppableCallCounter % 4
            quarter = self.quarters[quarterIndex]

            for cell in self.cellList:

                if cell.xCOM >= quarter[0] and cell.yCOM >= quarter[1] and cell.xCOM < quarter[2] and cell.yCOM < quarter[3]:
                    cell.fluctAmpl = 50
                else:
                    # this means CompuCell3D will use globally defined FluctuationAmplitude
                    cell.fluctAmpl = -1

            self.steppableCallCounter += 1



Assigning negative ``fluctuationAmplitude``, ``cell.fluctAmpl = -1`` is interpreted
by CompuCell3D as a hint to use fluctuation amplitude defined in the
CC3DML.

Let us revisit our original example of the ``Potts`` section CC3DML:

.. code-block:: xml

        <Potts>
            <Dimensions x="101" y="101" z="1"/>
            <Anneal>0</Anneal>
            <Steps>1000</Steps>
            <FluctuationAmplitude>5</FluctuationAmplitude>
            <Flip2DimRatio>1</Flip2DimRatio>
            <Boundary_y>Periodic</Boundary_y>
            <Boundary_x>Periodic</Boundary_x>
            <NeighborOrder>2</NeighborOrder>
            <DebugOutputFrequency>20</DebugOutputFrequency>
            <RandomSeed>167473</RandomSeed>
            <EnergyFunctionCalculator Type="Statistics">
                <OutputFileName Frequency="10">statData.txt</OutputFileName>
                <OutputCoreFileNameSpinFlips Frequency="1" GatherResults="" OutputAccepted="" OutputRejected="" OutputTotal=""/>
            </EnergyFunctionCalculator>
        </Potts>

Based on discussion about the difference between pixel-flip attempts and
MCS (see "Introduction to CompuCell3D") we can specify how many pixel
copies should be attempted in every MCS. We specify this number
indirectly by specifying the ``Flip2DimRatio`` by using

.. code-block:: xml

    <Flip2DimRatio>1</Flip2DimRatio>

which tells CompuCell that it should
make ``1 times number of lattice sites`` attempts per MCS – in our case one MCS
is 101x101x1 pixel-copy attempts. To set ``2.5 x 101 x 101 x 1`` pixel-copy
attempts per MCS you would write:

.. code-block:: xml

    <Flip2DimRatio>2.5</Flip2DimRatio>

The line beingning with ``<NeighborOrder>2</NeighborOrder>`` specifies the neighbor order.
The higher neighbor order the longer the Euclidian distance from a given pixel. In previous
The pixel neighbors are ranked according to their distance from a reference pixel (*i.e.* the one
you are measuring a distance from). thus we have 1\ :sup:`st`  2\ :sup:`nd`, 3\ :sup:`rd` and
so on nearest neighbors for every pixel in the lattice. Using 1\ :sup:`st` nearest neighbor
interactions may cause artifacts due to lattice anisotropy. The longer the interaction range
(*i.e.* 2\ :sup:`nd`, 3\ :sup:`rd` or higher ``NeighborOrder``), the more isotropic the
simulation and the slower it runs. In addition, if the interaction range
is comparable to the cell size, you may generate unexpected effects,
since non-adjacent cells will contact each other.

On hex lattice those problems seem to be less severe and there
1\ :sup:`st` or 2\ :sup:`nd` nearest neighbor usually are sufficient.

The Potts section also contains tags called ``<Boundary_y>`` and
``<Boundary_x>``. These tags impose boundary conditions on the lattice. In
this case the ``x`` and ``y`` axes are **periodic**.

For example:

.. code-block:: xml

    <Boundary_x>Periodic</Boundary_x>


will cause that the pixels with coordinates ``x=0 , y=1, z=1``
will neighbor the pixel with coordinates ``x=100, y=1, z=1``. If you do not
specify boundary conditions CompuCell will assume them to be of type
**no-flux**, *i.e.* lattice will not be extended. The conditions are
independent in each direction, so you can specify any combination of
boundary conditions you like.

``DebugOutputFrequency`` is used to tell CompuCell3D how often it should
output text information about the status of the simulation. This tag is
optional.

``RandomSeed`` is used to initialize the random number generator. If you 
**do not include this tag** (and a value) then a **different** random seed will be chosen 
for each run by the operating sytem and each simulation will use a 
**different set of random nuymbers** and each simulaiton will produce a
**different result**.
In gerneal, this is the behavior you want. CompuCell3D simulations are meant 
to be stoichsaistic and a simualtion represents a plausible trajectory of the 
system through time. So generally you will **not** include a ``<RandomSeed>`` 
element.

However, in some cases, you want to force CompuCell3D to use the same random seed for 
multiple runs so that it will proudce the same output everytime. This is often 
useful for debugging or for when you are doing parameter estimation or 
data fitting. In these cases you include the ``<RandomSeed>`` tag with an integer 
of your choice. Every simualtion with the same seed will produce the same results.
Note though that if you also use a random number generator in your Python code
then you will need to specify a random seed there as well. The two seeds do 
not have to be the same. For example, in your Python Steppables file you might
include:

.. code-block:: python

    import random
    random.seed(54321)

This makes your python code use the same series of random numbers for every run.

``EnergyFunctionCalculator`` is another option of Potts object that allows
users to output statistical data from the simulation for further
analysis.

.. note::

    CC3D has the option to run in the parallel mode but
    output from energy calculator will only work when running in a single
    CPU mode.

The ``OutputFileName`` tag is used to specify the name of the file to which
CompuCell3D will write average changes in energies returned by each
plugins with corresponding standard deviations for those MCS whose
values are divisible by the ``Frequency`` argument. Here it will write these
data every 10 MCS.

A second line with ``OutputCoreFileNameSpinFlips`` tag is used to tell
CompuCell3D to output energy change for every plugin, every pixel-copy
for MCS' divisible by the frequency. Option ``GatherResults=””`` will ensure
that there is only one file written for accepted (``OutputAccepted``),
rejected (``OutputRejected``)and accepted and rejected (``OutputTotal``) pixel
copies. If you will not specify ``GatherResults`` CompuCell3D will output
separate files for different MCS's and depending on the Frequency you
may end up with many files in your directory.

One option of the Potts section that we have not used here is the
ability to customize acceptance function for Metropolis algorithm:

.. code-block:: xml

    <Offset>-0.1</Offset>
    <KBoltzman>1.2</KBoltzman>

This ensures that pixel copies attempts that increase the energy of the
system are accepted with probability

.. math::
   :nowrap:

   \begin{eqnarray}
        P = e^{(-\Delta E - \delta)/kT}
   \end{eqnarray}


where :math:`δ` and :math:`k` are specified by ``Offset`` and ``KBoltzman`` tags respectively.
By default :math:`δ=0` and :math:`k=1`.

As an alternative to exponential acceptance function you may use a
simplified version which is essentially 1 order expansion of the
exponential:

.. math::
   :nowrap:

   \begin{eqnarray}
        P = 1 - \frac{E-\delta}{kT}
   \end{eqnarray}


To be able to use this function all you need to do is to add the
following line in the Pots section:


.. code-block:: xml

    <AcceptanceFunctionName>FirstOrderExpansion</AcceptanceFunctionName>
