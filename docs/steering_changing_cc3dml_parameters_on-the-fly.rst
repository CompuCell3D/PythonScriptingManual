Steering – changing CC3DML parameters on-the-fly.
=================================================

CC3D 4.0.0 greatly simplifies modification of CC3DML parameters from Python script as the
simulation runs. we call it programmatic steering.

Imagine that we would like to increase cell membrane fluctuation amplitude (in CC3D terminology ``Temperature``)
every 100 MCS by ``1`` unit. The ``Temperature`` is declared in the CC3DML so, unlike variables declared in
Python script, we dont have a direct access to it.

Let’s look at CC3DML code first:

.. code-block:: xml

    <Potts>
       <Dimensions x="100" y="100" z="1"/>
       <Steps>10000</Steps>
       <Temperature>10</Temperature>
       <NeighborOrder>2</NeighborOrder>
    </Potts>


The way CC3D 4.x solves this problem is very much inspired by Javascript/HTML approach.
First you tag element that you wish to change using ``id`` tag as shown below:

.. code-block:: xml

    <Potts>
       <Dimensions x="100" y="100" z="1"/>
       <Steps>10000</Steps>
       <Temperature id="temp_elem">10</Temperature>
       <NeighborOrder>2</NeighborOrder>
    </Potts>

Here we add ``id="temp_elem"``. If you have multiple ``id`` tags for in your XML script we require that
they are unique.

After we tagged the CC3DML elements we can easily access and modify them on-the-fly as shown below

.. code-block:: python

    class TemperatureSteering(SteppableBasePy):
        def __init__(self, frequency=100):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):
            temp_elem = self.get_xml_element('temp_elem')
            temp_elem.cdata = float(temp_elem.cdata) + 1

In the ``step`` function we first access the tagged element:

.. code-block:: python

    temp_elem = self.get_xml_element('temp_elem')

and then we modify its ``cdata`` portion using

.. code-block:: python

    temp_elem.cdata = float(temp_elem.cdata) + 1

After this last modification CC3D will take a notice that the change has been made and will update
appropriate internal variables.

XML Element Structure
---------------------

Each XML (CC3DML is also a valid XML) has the following structure

.. code-block:: xml

    <MyMLElement attr_1="attr_1_value"  attr_2="attr_2_value">cdata</MyMLElement>

For example in the following element

.. code-block:: xml

    <Energy Type1="Medium" Type2="Condensing">10</Energy>


the element name is ``Energy``. It has two attributes ``Type1`` with value ``Medium`` and ``Type2``
with value ``Condensing``. And the value of ``cdata`` component is ``10``

Similarly, the element ``ChemotaxisByType``

.. code-block:: xml

    <ChemotaxisByType Type="Macrophage" Lambda="20"/>

has two attributes ``Type`` and ``Lambda`` with values ``Macrophage`` and ``20`` respectively.

Modifying CC3DML attributes
---------------------------

If we want to modify attributes of the XML element we use similar approach to the one
outlined above. We tag element we want modify and then update attributes. Here is an example

.. code-block:: xml

    <Plugin Name="Chemotaxis">
        <ChemicalField Name="ATTR">
            <ChemotaxisByType id="macro_chem" Type="Macrophage" Lambda="20"/>
        </ChemicalField>
    </Plugin>


and the Python code that modifies ``Lambda`` attribute of ``ChemotaxisByType``

.. code-block:: python

    from cc3d.core.PySteppables import *


    class ChemotaxisSteering(SteppableBasePy):
        def __init__(self, frequency=100):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):
            if mcs > 100 and not mcs % 100:
                macro_chem_elem = self.get_xml_element('macro_chem')
                macro_chem_elem.Lambda = float(macro_chem_elem.Lambda) - 3


As you can see the syntax is quite straightforward. We first fetch the reference to the XML element
(we tagged it using ``id="macro_chem"``):

.. code-block:: python

    macro_chem_elem = self.get_xml_element('macro_chem')

and modify its ``Lambda`` attribute


.. code-block:: python

    macro_chem_elem = self.get_xml_element('macro_chem')
    macro_chem_elem.Lambda = float(macro_chem_elem.Lambda) - 3

Two things are worth mentioning here.

1. when we access attribute we use the name of the attribute and "dot" it with reference
to the XML element we fetched:

.. code-block:: python

    macro_chem_elem.Lambda

2. ``cdata`` and attributes are returned as strings so before doing any arithmetic operation we need to convert
strings to appropriate Python types. Here we convert string returned by ``macro_chem_elem.Lambda``
(first call will return string ``20``) to floating point number ``float(macro_chem_elem.Lambda)`` and subtract 3
. When we assign it back to the attribute we do not need to convert to string - CC3D will handle
this conversion automatically

Full example of steering can be found in ``Demos/Models/bacterium_macrophage_2D_steering``


