Adding Steppable to Simulation using Twedit++
=============================================

In the above example Python steppable was created by a simulation
wizard. But what if you want to add additional steppable? Twedit++ lets
you do it with pretty much single click. In the CC3D Project Panel
right-click on Steppable Python file and choose Add Steppable option:

|image7|

*Figure 8 Adding seppable using Twedit++*

The dialog will pop up where you specify name and type of the new
steppable, call frequency. Click ``OK`` and new steppable gets added to your
code.

|image8|

Figure 9 Configuring basic steppable properties in Twedit++.

Notice that Twedit++ takes care of adding steppable registration code in
the main Python script:

.. code-block:: python

    from cellsortingSteppables import MyNewSteppable
   CompuCellSetup.register_steppable(steppable=MyNewSteppable(frequency=1))

.. |image7| image:: images/image8.jpeg
   :width: 3.25000in
   :height: 2.72526in
.. |image8| image:: images/image9.jpeg
   :width: 2.68750in
   :height: 2.16026in
