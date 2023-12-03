ConvergentExtension plugin
--------------------------

.. note::

   This is very specialized plugin that is currently is in Tier 2
   plugins in terms of support. It attempts to implement energy term
   described in "Simulating Convergent Extension by Way of Anisotropic
   Differential Adhesion", *Zajac* M, *Jones* GL, and *Glazier* JA, Journal
   of Theoretical Biology **222** (2), 2003. However due to certain
   ambiguities in the plugin description we had difficulties to getting it
   to work properly.

.. note::

   A better way to implement convergent extension is to follow
   the simulations described in "Filopodial-Tension Model of Convergent-Extension of Tissues",
   *Julio M. Belmonte* , *Maciej H. Swat*, *James A. Glazier*, PLoS Comp Bio  https://doi.org/10.1371/journal.pcbi.1004952



``ConvergentExtension`` plugin presented here is a somewhat simplified version of
energy term described *Mark Zajac's* paper.

This plugin uses the following syntax:

.. code-block::

   <Plugin Name="ConvergentExtension">
      <Alpha Type="Condensing" >0.99</Alpha>
      <Alpha Type="NonCondensing" >0.99</Alpha>
      <NeighborOrder>2</NeighborOrder>
   </Plugin>

The ``Alpha`` tag represents numerical value of α parameter from the paper.
