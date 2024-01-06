Stochasticity and RandomSeed
===================================

A CC3DML file may contain a ``<RandomSeed>`` tag like this:

.. code-block:: xml

        <Potts>
            <Dimensions x="101" y="101" z="1"/>
            <Steps>100000</Steps>
            <Temperature>10.0</Temperature>
            <NeighborOrder>2</NeighborOrder>
            <RandomSeed>167473</RandomSeed>
        </Potts>

If you *do not include this tag* and a value, then a *different* random seed will be chosen 
for each run by the operating system and each simulation will use a 
*different set of random numbers*, meaning that each simulation will produce a
**different result**.
In general, this is the behavior you want. CompuCell3D simulations are meant 
to be stochastic, and a simulation represents a plausible trajectory of the 
system through time. So, generally, you will **not** include a ``<RandomSeed>`` 
element.

However, in some cases, you want to force CompuCell3D to use the same random seed for 
multiple runs so that it will produce the same output every time. This is often 
useful for debugging or for when you are doing parameter estimation or 
data fitting. In these cases, you include the ``<RandomSeed>`` tag with an integer 
of your choice. Every simulation with the same seed will produce the same results.
Note though that if you also use a random number generator in your Python code
then you will need to specify a random seed there as well. The two seeds do 
not have to be the same. For example, in your Python Steppables file you might
include:

.. code-block:: python

    import random
    random.seed(54321)

This makes your Python code use the same series of random numbers for every run,
eliminating the stochasticity that would otherwise occur between simulations.
