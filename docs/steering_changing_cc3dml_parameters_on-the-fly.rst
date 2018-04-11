Steering – changing CC3DML parameters on-the-fly.
=================================================

(You may skip this paragraph in the first reading)

In the CC3D terminology, steering means changing simulation parameters
on the fly as simulation is running. In fact the whole point of merging
Python scripting with CC3D core code is to enable steering. What about
parameters defined in CC3DML? Can they be modified as the simulation
runs? The short answer is **yes** but not all of them. There are two ways
of doing it – one way is to use player CC3DML panel and change
parameters in the GUI. The second way is to use Python. Python code that
alters CC3DML parameters during simulation runtime is quite
clumsy-looking. It is not difficult to understand but is quite verbose
and, to be honest it is not too much fun to write. Probably the best way
to learn how to modify CC3DML from Python is to look at several
examples. Let us start with the simplest one
(``Demos/SimulationSettings/Steering``):

Here we will modify two CC3DML parameters one will be Temperature from
the CC3DML Potts Section and the other one will be Contact energy
between Condensing and NonCondensing.

Let’s look at CC3DMLcode first:

.. code-block:: xml

    <Potts>
       <Dimensions x="100" y="100" z="1"/>
       <Steps>10000</Steps>
       <Temperature>10</Temperature>
       <NeighborOrder>2</NeighborOrder>
    </Potts>


Potts XML element has 4 child elements – Dimensions, Steps, Temperature
and NeighborOrder.

To modify Temperature parameter we use the following code:

.. code-block:: python

    class PottsSteering(SteppablePy):
        def __init__(self, _simulator, _frequency=1):
            SteppablePy.__init__(self, _frequency)
            self.simulator = _simulator

        def step(self, _mcs):
            # get Potts section of XML file
            pottsXMLData = self.simulator.getCC3DModuleData("Potts")
            # check if we were able to successfully get the section from simulator
            if pottsXMLData:
                # get Temperature XML element
                temperatureElement = pottsXMLData.getFirstElement("Temperature")
                # check if the attempt was succesful
                if temperatureElement:
                    # get value of the temperature and convert it to a floating point number
                    temperature = float(temperatureElement.getText())
                    # increase temperature by 1.0
                temperature += 1.0
                # update XML Temperature element by converting floating point
                temperatureElement.updateElementValue(str(temperature))
            # finally call simulator.updateCC3DModule(pottsXMLData) to update model
            # parameters - this is actual steering
            self.simulator.updateCC3DModule(pottsXMLData)

Each XML element that we fetch using Python (e.g. ``pottsXMLData``,
``temperatureElement``) has set of member functions that allow us to get to
elements nested one level deeper (child elements) or functions which
allow us to read and modify element values and element attributes. For
the temperatureElement we are modifying its value.

**Important**: XML stores text. All numbers or other data types stored
in the XML are converted to their text representations. Consequently,
depending on your needs and particular applications, you may need to
convert text to numbers and vice versa when interacting with XML
through Python interface.

In the code presented above we first fetch Potts element (pottsXMLData)
using special function from the simulator object. If the fetching
operation was successful we try to fetch first Temperature child element
of the Potts element. If this operation was successful we convert value
of the temperature element to floating point number:

.. code-block:: python

    temperature = float(temperatureElement.getText())

we increase value of this number by one and then update value of the
``temperatureElement``:

.. code-block:: python

    temperatureElement.updateElementValue(str(temperature))

Notice that we had to convert floating point number temperature back to
string using ``str(temperature)`` call.

The steppable ends with call to simulator member function that informs
CC3D that CC3DML was changed and simulation needs to get new parameters:

.. code-block:: python

    self.simulator.updateCC3DModule(pottsXMLData)

As you can see the code was not hard to write but is quite long and
clumsy. We could simplify it a bit but getting rid of comments and if
statements that check if fetching operation was successful. In such a
case the code would look like that:

.. code-block:: python

    class PottsSteering(SteppablePy):
        def __init__(self, _simulator, _frequency=1):
            SteppablePy.__init__(self, _frequency)
            self.simulator = _simulator

        def step(self, _mcs):
            pottsXMLData = self.simulator.getCC3DModuleData("Potts")
            temperatureElement = pottsXMLData.getFirstElement("Temperature")
            temperature = float(temperatureElement.getText())
            temperature += 1.0
            temperatureElement.updateElementValue(str(temperature))
            self.simulator.updateCC3DModule(pottsXMLData)

This is not so bad but still it is a lot of work to change one number.
But do we have a choice here? In fact we do. All we have to do is to
change cell membrane fluctuation amplitude using the following code:

.. code-block:: python

    newTemperature=51
    for cell in self.cellList:
        cell.fluctAmpl= newTemperature

In practice you don’t use need to modify CC3DML from Python level too
often. CC3D has modules e.g. ``AdhesionFlex``, ``FocalPointPlasticity``,
``VolumeLocalFlex`` that require initialization of their parameters in
Python but also offer much simpler programing interfaces making coding
much less cumbersome. Please make sure that before writing complicated
CC3DML steering code you familiarize yourself with modules that are
designed to be flexible and do not rely on CC3DML-type of steering.

Now let us take a look at the code that alters contact energy, but first
quick glance at the CC3DML that we will be modifying:

.. code-block:: xml

    <Plugin Name="Contact">
       <Energy Type1="NonCondensing" Type2="Condensing">11</Energy>
       <Energy Type1="Condensing"    Type2="Condensing">2</Energy>
    …
       <NeighborOrder>2</NeighborOrder>
     </Plugin>


Our task here is to first fetch Plugin XML Element and then fetch Energy
Element for type pair ``Condensing`` and ``NonCondensing``. Here is the code
that does it:

.. code-block:: python

    class ContactSteering(SteppablePy):
        def __init__(self, _simulator, _frequency=10):
            SteppablePy.__init__(self, _frequency)
            self.simulator = _simulator

        def step(self, mcs):
            # get <Plugin Name="Contact"> section of XML file
            contactXMLData = self.simulator.getCC3DModuleData("Plugin", "Contact")
            # check if we were able to successfully get the section from simulator
            if contactXMLData:
                # get <Energy Type1="NonCondensing" Type2="Condensing"> element
                energyNonCondensingCondensingElement = contactXMLData.getFirstElement \
                    ("Energy", d2mss({"Type1": "NonCondensing", "Type2": "Condensing"}))
                # check if the attempt was succesful
                if energyNonCondensingCondensingElement:
                    # get value of <Energy Type1="NonCondensing" Type2="Condensing"> element
                    # and convert it into float
                    val = float(energyNonCondensingCondensingElement.getText())
                    # increase the value by 1.0
                    val += 1.0
                    # update <Energy Type1="NonCondensing" Type2="Condensing"> element
                    # remembering abuot converting the value bask to string
                    energyNonCondensingCondensingElement.updateElementValue(str(val))
                # finally call simulator.updateCC3DModule(contactXMLData) to tell simulator
                # to update model parameters - this is actual steering
                self.simulator.updateCC3DModule(contactXMLData)

We first fetch Plugin element using simulator object member function:

.. code-block:: python
    contactXMLData = self.simulator.getCC3DModuleData("Plugin", "Contact")

When this operation succeeds we attempt to fetch Python object
representation for the

``<Energy Type1="NonCondensing" Type2="Condensing">11</Energy>`` element:

.. code-block:: python

    energyNonCondensingCondensingElement=contactXMLData.getFirstElement("Energy",
        d2mss({"Type1":"NonCondensing","Type2":"Condensing"})
    )


Notice that when we call ``getFirstElement`` member function of the
contactXMLData we pass the name of the element but also a partial list of
element attributes. Here we use ``d2mss`` function what converts Python
dictionary ``{"Type1":"NonCondensing","Type2":"Condensing"}`` to C++
``map<string,string>``. With so much information passed to ``getFirstElement``
function only one element fits the description and this is the one that
we are looking for. The reminder of the steppable looks almost identical
as in the example where we changed temperature.

The next example demonstrates how to update attribute of the XML
element. You can find full code in
``Demos/Models/bacterium_macrophage_2D_steering``. Again let us look at
the CC3DML that we will be modifying:

.. code-block:: xml

    <Plugin Name="Chemotaxis">
        <ChemicalField Source="FlexibleDiffusionSolverFE" Name="ATTR" >
        <ChemotaxisByType Type="Macrophage" Lambda="20"/>
        </ChemicalField>
    </Plugin>


We would like to periodically decrease ``lambda`` chemotaxis by 3 units.
This is how we do it in Python:

.. code-block:: python

    class ChemotaxisSteering(SteppablePy):
        def __init__(self, _simulator, _frequency=100):
            SteppablePy.__init__(self, _frequency)
            self.simulator = _simulator

        def step(self, mcs):
            if mcs > 100 and not mcs % 100:
                # get <Plugin Name="Chemotaxis"> section of XML file
                chemotaxisXMLData = self.simulator.getCC3DModuleData("Plugin", "Chemotaxis")
                # check if we were able to successfully get the section from simulator
                if chemotaxisXMLData:
                    # get <ChemicalField Source="FlexibleDiffusionSolverFE" Name="ATTR" >
                    chemicalField = chemotaxisXMLData.getFirstElement("ChemicalField",
                                                                      d2mss({"Source": "FlexibleDiffusionSolverFE",
                                                                             "Name": "ATTR"}))
                    # check if the attempt was succesful
                    if chemicalField:
                        # get <ChemotaxisByType Type="Macrophage" Lambda="xxx"/>
                        chemotaxisByTypeMacrophageElement = chemicalField.getFirstElement("ChemotaxisByType",
                                                                                          d2mss({"Type": "Macrophage"}))
                        if chemotaxisByTypeMacrophageElement:
                            # get value of Lambda from <ChemotaxisByType> element
                            # notice that no conversion fro strin to float is necessary as
                            # getAttributeAsDouble returns floating point value

                            lambdaVal = chemotaxisByTypeMacrophageElement.getAttributeAsDouble("Lambda")
                            print "lambdaVal=", lambdaVal
                            # decrease lambda by 0.2
                            lambdaVal -= 3
                            # update attribute value of Lambda converting float to string
                            chemotaxisByTypeMacrophageElement.updateElementAttributes(d2mss({"Lambda": str(lambdaVal)}))
                self.simulator.updateCC3DModule(chemotaxisXMLData)


As you can see the structure of the code is very similar to the previous
2 examples. First we fetch Plugin element describing Chemotaxis
properties:

.. code-block:: python

    chemotaxisXMLData = self.simulator.getCC3DModuleData("Plugin","Chemotaxis")

Next, we fetch ChemicalField element:

.. code-block:: python

    chemicalField = chemotaxisXMLData.getFirstElement("ChemicalField",
                                                  d2mss({"Source": "FlexibleDiffusionSolverFE", "Name": "ATTR"}))


and using ChemicalField element we get ChemotaxisByType element:

.. code-block:: python

    chemotaxisByTypeMacrophageElement = chemicalField.getFirstElement("ChemotaxisByType",
                                                                      d2mss({"Type": "Macrophage"}))

Using ``chemotaxisByTypeMacrophageElement`` we fetch its attribute lambda
convert it to floating point number decrease by 3 units and assing new
value of lambda:

.. code-block:: python

    lambdaVal = chemotaxisByTypeMacrophageElement.getAttributeAsDouble("Lambda")
    lambdaVal -= 3
    chemotaxisByTypeMacrophageElement.updateElementAttributes(d2mss({"Lambda": str(lambdaVal)}))

The rest of the code is analogous to the previous examples. This
completes the discussion of CC3DML steering.

Simplifying steering - XML access path
--------------------------------------

Basic Terminology
-----------------

When accessing variables defined in the XML element we are typically dealing with ``attributes``
and ``values``. Let's consider the following XML element

.. code-block:: xml

    <Energy Type1=“Condensing” Type2=“NonCondensing”>20.0</Energy>

The difference between attribute and value of the element is that attributes are all the
labels inside ``<>`` element marker to which we assign some value. For example ``Type1`` and ``Type2``
are attributes of the XML element ``Energy``, whereas ``20.0`` is the value of this XML element.
In what follows below we will be accessing and modifying both attributes and Values of the XML elements.
Please pay close attention whwther the function we are using is of ``*XMLValue`` or ``*XMLAttributeValue`` type

**Note** Some XML elements might have only attributes e.g. :

.. code-block:: xml

    <VolumeConstraint LambdaVolume=“20” TargetVolume="125" Type="Condensing"/>

and some might have only values:

.. code-block:: xml

    <Steps>10000</Steps>





The above examples demonstrate how to steer CC3DML-based part of the
simulation in a fairly verbose way i.e. the amount of code is quite
significant. In 3.7.1 we have introduced more compact way to access and
modify CC3DML elements: Let us look at the implementation of the
``ContactSteeringAndTemperature`` steppable using new style coding:

.. code-block:: python

    class ContactSteeringAndTemperature(SteppableBasePy):
        def __init__(self, _simulator, _frequency=10):
            SteppableBasePy.__init__(self, _simulator, _frequency)

        def step(self, mcs):
            temp = float(self.getXMLElementValue(['Potts'], ['Temperature']))
            self.setXMLElementValue(temp + 1, ['Potts'], ['Temperature'])

            val = float(
                self.getXMLElementValue(
                    ['Plugin', 'Name', 'Contact'], ['Energy', 'Type1', 'NonCondensing', 'Type2', 'Condensing']))

            self.setXMLElementValue(
                val + 1, ['Plugin', 'Name', 'Contact'], ['Energy', 'Type1', 'NonCondensing', 'Type2', 'Condensing']
            )

            self.updateXML()


Instead of using verbose code to access CC3DML elements we now specify
access path to particular element . Access path is a sequence of Python
lists. First element of each list is the name of the CC3DML element
followed by a sequence of pairs (attribute,value) which fully specify
the XML element:

``[ElementName, AttrName1, AttrValue1, Attr2, AttrValue2, …, AttrNameN, AttrValueN]``

In the CC3DML code below:

.. code-block:: xml

    <CompuCell3D>
     <Potts>
       <Dimensions x="100" y="100" z="1"/>
       <Anneal>10</Anneal>
       <Steps>10000</Steps>
       <Temperature>10</Temperature>
       <Flip2DimRatio>1</Flip2DimRatio>
       <NeighborOrder>2</NeighborOrder>
     </Potts>


     <Plugin Name="Volume">
       <TargetVolume>25</TargetVolume>
       <LambdaVolume>2.0</LambdaVolume>
     </Plugin>

    <Plugin Name="CellType">
        <CellType TypeName="Medium" TypeId="0"/>
        <CellType TypeName="Condensing" TypeId="1"/>
        <CellType TypeName="NonCondensing" TypeId="2"/>
     </Plugin>

     <Plugin Name="Contact">
       <Energy Type1="Medium" Type2="Medium">0</Energy>
       <Energy Type1="NonCondensing" Type2="NonCondensing">16</Energy>
       <Energy Type1="Condensing"    Type2="Condensing">2</Energy>
       <Energy Type1="NonCondensing" Type2="Condensing">11</Energy>
       <Energy Type1="NonCondensing" Type2="Medium">16</Energy>
       <Energy Type1="Condensing"    Type2="Medium">16</Energy>
       <NeighborOrder>2</NeighborOrder>
     </Plugin>

    ...
    </CompuCell3D>

to access Temperature element from the Potts section we construct our
access path following one simple rule:

1. Recursively identify child element of the current element that leads
   you to the desired place in the CC3DML code. **Notice:** we skip root
   element ``<CompuCell3D>`` element.

In our example to access ``<Temperature>`` element we first locate <Potts>
as a child of ``<CompuCell3D>`` element (remember in the access path we do
not include ``<CompuCell3D>`` element) and

then ``<Temperature>`` appears to be child of the ``<Potts>``. Hence our access
path is a simple sequence of two Python lists, each list with one
element:

.. code-block:: python

    ['Potts'],['Temperature']

A bit more complex, but still much simpler than our original code, is
the example where we locate one of the Contact plugin elements. ``<Plugin Name="Contact">``
is a child of the ``<CompuCell3D>`` hence:

.. code-block::  python

    ['Plugin','Name','Contact']

will be first Python list of ther access path. Notice that the first
element of this list is the same as name of the child element (``Plugin``)
and the two next elements constitute an XML attribute-value pair. In
other words, XML’s ``Name="Contact"`` gets translated into ``'Name'``,``'Contact'``
of the Python list.

Now we locate correct <Energy> element. Since there are many of these
the correct identification of the one which is of interest for us
will require specification of all its attributes: ``Type1="NonCondensing" Type2="Condensing"``.
Consequently our access path from ``<Plugin>`` to
``<Energy>`` will look as follows:

.. code-block:: python

    ['Energy','Type1','NonCondensing','Type2','Condensing']

And the full path is simply

.. code-block:: python

    ['Plugin','Name','Contact'],['Energy','Type1','NonCondensing','Type2','Condensing']
