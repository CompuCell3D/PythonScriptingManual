Adding plots to the simulation
==============================

Some modelers like to monitor simulation progress bydisplaying “live”
plots that characterize current state of the simulation. In CC3D it is
very easy to add to the Player windows. The best way to add plots is via
Twedit++ CC3D Python->Scientific Plots menu. Take a look at example code
to get a flavor of what is involved when you want to work with plots in
CC3D:

.. code-block:: python

    class cellsortingSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=1):
            SteppableBasePy.__init__(self, _simulator, _frequency)

        def start(self):
            self.pW = self.addNewPlotWindow(
                _title='Average Volume And Volume of Cell 1',
                _xAxisTitle='MonteCarlo Step (MCS)',
                _yAxisTitle='Variables',
                _xScaleType='linear',
                _yScaleType='log',
                _grid=True # only in 3.7.6 or higher
            )

            self.pW.addPlot('AverageVol', _style='Dots', _color='red', _size=5)
            self.pW.addPlot('Cell1Vol', _style='Steps', _color='black', _size=5)

        def step(self, mcs):

            averVol = 0.0
            numberOfCells = 0

            for cell in self.cellList:
                averVol += cell.volume
                numberOfCells += 1

            averVol /= float(numberOfCells)

            cell1 = self.attemptFetchingCellById(1)
            print cell1

            self.pW.addDataPoint("AverageVol", mcs, averVol)  # name of the data series, x, y
            self.pW.addDataPoint("Cell1Vol", mcs, cell1.volume)  # name of the data series, x, y
            # self.pW.showAllPlots() # no longer necessary

In the ``start`` function we create plot window (``self.pW``) – the arguments of
this function are self explanatory. After we have plot windows object
(``self.pW``) we are adding actual plots to it. Here we will plot two
time-series data, one showing average volume of all cells and one
showing instantaneous volume of cell with id 1:

.. code-block:: python

    self.pW.addPlot('AverageVol',_style='Dots',_color='red',_size=5)
    self.pW.addPlot('Cell1Vol',_style='Steps',_color='black',_size=5)

We are specifying here plot symbol types (``Dots``, ``Steps``), their sizes and
colors. The first argument is then name of the data series. This name
has two purposes – **1.** It is used in the legend to identify data points
and **2.** It is used as an identifier when appending new data. We can also
specify logarithmic axis by using ``_yScaleType='log'`` as in the example
above.

In the ``step`` function we are calculating average volume of all cells and
extract instantaneous volume of cell with id ``1``. After we are done with
calculations we are adding our results to the time series:

.. code-block:: python

    self.pW.addDataPoint("AverageVol",mcs,averVol) # name of the data series, x, y
    self.pW.addDataPoint("Cell1Vol",mcs,cell1.volume) # name of the data series, x, y

Notice that we are using data series identifiers (``AverageVol`` and
``Cell1Vol``) to add new data. The second argument in the above function
calls is current Monte Carlo Step (mcs) whereas the third is actual
quantity that we want to plot on Y axis. We are done at this point

**Important:** Previous versions of CC3D required users to explicitly
update plots by calling self.pW.showAllPlots() . ***This is no longer
necessary although including this call will not cause any side-effects ***.
self.pW.showAllPlots() # DEPRECATED

The results of the above code may look something like:

|image12|

Figure 13 Displaying plot window in the CC3D Player with 2 time-series
data.

Notice that the code is fairly simple and, for the most parts,
self-explanatory. However, the plots are not particularly pretty and
they all have same style. This is because this simple code creates plots
based on same template. The plots are usable but if you need high
quality plots you should save your data in the text data-file and use
stand-alone plotting programs. Plots provided in CC3D are used mainly as
a convenience feature and used to monitor current state of the
simulation.

 Histograms
-----------

Adding histograms to CC3D player is a bit more complex than adding
simple plots. This is because you need to first process data to produce
histogram data. Fortunately Numpy has the tools to make this task
relatively simple. An example ``scientificHistBarPlots`` in
CompuCellPythonTutorial demonstrates the use of histogram. Let us look
at the example steppable (you can also find relevant code snippets in
``CC3D Python-> Scientific Plots`` menu):

.. code-block:: python

    class HistPlotSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=10):
            SteppableBasePy.__init__(self, _simulator, _frequency)

        def start(self):

            # initialize setting for Histogram
            self.pW = self.addNewPlotWindow(_title='HIstogram', _xAxisTitle='Cell #', _yAxisTitle='Volume')

            # _alpha is transparency 0 is transparent, 255 is opaque
            self.pW.addHistogramPlot(_plotName='Hist 1', _color='green', _alpha=100)
            self.pW.addHistogramPlot(_plotName='Hist 2', _color='red')
            self.pW.addHistogramPlot(_plotName='Hist 3', _color='blue')

        def step(self, mcs):
            volList = []
            for cell in self.cellList:
                volList.append(cell.volume)

            gauss = []
            for i in range(100):
                gauss.append(random.gauss(0, 1))

            self.pW.addHistogram(plot_name='Hist 1', value_array=gauss, number_of_bins=10)
            self.pW.addHistogram(plot_name='Hist 2', value_array=volList, number_of_bins=10)
            self.pW.addHistogram(plot_name='Hist 3', value_array=volList, number_of_bins=50)

            fileName = "HistPlots_" + str(mcs) + ".png"
            self.pW.savePlotAsPNG(fileName, 1000, 1000)  # here we specify size of the image

            fileName = "HistPlots_" + str(mcs) + ".txt"
            self.pW.savePlotAsData(fileName)

In the start function we call ``self.addNewPlotWindow`` to add new plot
window -``self.pW``- to the Player. Subsequently we specify display
properties of different data series (histograms). Notice that we can
specify opacity using ``_alpha`` parameter.

In the step function we first iterate over each cell and append their
volumes to Python list. Later plot histogram of the array using a very
simple call:

.. code-block:: python

    self.pW.addHistogram(plot_name='Hist 2' , value_array=volList ,number_of_bins=10)

that takes an array of values and the number of bins and adds histogram
to the plot window.

Alternatively we may use slightly more complex way od adding histogram
which in some situations may actually give you a bit more control. First
we bin array of values using numpy functionality:

.. code-block:: python

    (n, bins) = numpy.histogram(volList, bins=10)

The return values are two numpy arrays: n which specifies center of the
bin (we plot it on x axis) and bins which determines stores counts for a
given bin.

**Important**: Make sure you import random and numpy modules in the
steppable file. Place the following code:

.. code-block:: python

    import random, numpy

at the top of the file.

Next you add histogram data output from numpy to the plot using the
following call:

.. code-block:: python

    self.pW.addHistPlotData('Hist 2', n, bins)

The following snippet:

.. code-block:: python

        gauss = []
        for i in  range(100):
            gauss.append(random.gauss(0,1))

        (n2, bins2) = numpy.histogram(gauss, bins=10)

declares gauss as Python list and appends to it 100 random numbers which
are taken from Gaussian distribution centered at 0.0 and having standard
deviation equal to 1.0. We histogram those values using the following
code:

.. code-block:: python

    self.pW.addHistogram(plot_name='Hist 1' , value_array = gauss ,number_of_bins=10)

When we look at the code in the ``start`` function we will see that this
data series will be displayed using green bars.

**Imnportant:** Calling ``showAllHistPlots`` is no longer necessary


At the end of the steppable we output histogram plot as a png image file
using:

.. code-block:: python
    self.pW.savePlotAsPNG(fileName,1000,1000)


two last arguments of this function represent `x` and `y` sizes of the
image.

**Imnportant:** as of writing this manual we do not support scaling of the plot image output.
This might change in the future releases, however we strongly recommend that you save all the data you plot
in a separate file and post-process it in the full-featured plotting program

We construct fileName in such a way that it contains MCS in it.
The image file will be written in the simulation outpt directory.
Finally, for any plot we can output plotted data in the form of a text
file. All we need to do is to call ``savePlotAsData`` from the plot windows
object:

.. code-block:: python
    fileName = "HistPlots_"+str(mcs)+".txt"
    self.pW.savePlotAsData(fileName)

This file will be written in the simulation output directory. You can
use it later to post process plot data using external plotting software.

.. |image12| image:: images/image13.jpeg
   :width: 3.86458in
   :height: 2.10003in
