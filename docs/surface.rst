Surface and Cell Contact
=======================================

By controlling a cell's surface, you can adjust the amount of perimeter it exposes to neighbors or the Medium.
We recommend to always add the Contact plugin when creating a new simulation.


Properties
****************************

**cell.targetSurface**: the "goal" surface that a cell tries to reshape itself to whenever possible. 
For roughly square or blob-shaped cells, ``targetSurface`` would be 4*sqrt(``targetVolume``).

**cell.lambdaSurface**: the strength of the surface constraint; that is, how quickly a cell will reshape itself to meet its targetSurface.

**********************************************


Relevant Examples:
    * `How to Detect Contact <example_contact_events.html>`_
    * `Epithelial-Mesenchymal Transition (EMT)<example_epithelial_mesenchymal_transition.html>`_
