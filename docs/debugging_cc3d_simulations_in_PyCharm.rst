Running and Debugging CC3D Simulations Using PyCharm
=====================================================

Twedit++ provides many convenience tools when it comes to setting up simulation and also quickly modifying the
content of the simulation using provided code helpers (see Twedit's CC3D Python and CC3D XML menus). Twedit also
allows rapid creation of CC3D C++ plugins and steppables (something we cover in a separate developer's manual).
However, as of current version, Twedit++ is just a code editor not an Integrated Development Environment (**IDE**).
A real development environment offers many convenience features that make development faster. In this chapter we will
teach you how to set up and use PyCharm to debug and quickly develope CC3D simulations. The ability of stepping up
through simulation code is essential during simulation development. There you can inspect every single variable
without using pesky **print** statements. You can literally see how your simulation is executed ,
statement-by-statement. In addition PyCharm provides nice context-based syntax completion so that by typing
few characters from e.g. steppable method name (they do not need to be beginning characters) PyCharm will display
available options, freeing you from memorizing every single method in CompuCell3D API.

First thing we need to do is to download and install PyCharm. Because PyCharm is written in Java
it is available for every single platform. Visit https://www.jetbrains.com/pycharm/download/
and get Community version of PyCharm for your operating system. YOu can also get professional version but you need to
pay for this one so depending on your needs you have to make a choice here. We are using Community version because it
is feature-rich and unless you do a lot of specialized Python development you will be fine with the free option.

After installing and doing basic configuration of PyCharm you are ready to open and configure CC3D to be executed from
the IDE.

Step 1 - opening CC3D code in PyCharm and configuring Python environment
------------------------------------------------------------------------

To open CC3D code in Pycharm,  navigate to ``File->Open...`` and go to the folder where you installed CC3D and
open the following subfolder <CC3D_install_folder>/lib/site-packages. In my case CC3D is installed in ``c:\CompuCell3D-py3-64bit\``
so I am opening ``c:\CompuCell3D-py3-64bit\lib\site-packages\``

.. figure:: |pycharm_win_01|
    :alt: Opening ``site-packages`` subfolder from CC3D installation directory

.. figure:: images/wizard_twedit.png
    :alt: Figure 1 Invoking the CompuCell3D Simulation Wizard from Twedit++.

    Figure 1 Invoking the CompuCell3D Simulation Wizard from Twedit++.


.. |pycharm_win_01| image:: images/pycharm_win_01.png
   :width: 4.2in
   :height: 4.8in
