BoxWatcher Steppable
---------------------

.. warning::

    Functionality of this module has been reduced in CC3D
    versions that support parallel computations (``3.6.0`` and up). Main
    motivation for this module was to speed up computations but with
    parallel version the need for this module is somewhat smaller.

This steppable can potentially speed-up your simulation. Every MCS (or
every ``Frequency`` MCS) it determines maximum and minimum coordinates of
cells and then imposes slightly bigger box around cells and ensures that
in the subsequent MCS pixel copy attempts take place only inside this
box containing cells (plus some amount of medium on the sides). Thus,
instead of sweeping entire lattice and attempting random pixel copies
CompuCell3D will only spend time trying flips inside the box. Depending
on the simulation the performance gains are up to approx. 30%. The
steppable will work best if you have simulation with cells localized in
one region of the lattice with lots of empty space. The steppable will
adjust box every ``MCS`` (or every ``Frequency`` MCS) according to evolving
cellular pattern.

The syntax is as follows:

.. code-block::

    <Steppable Type="BoxWatcher">
        <XMargin>5</XMargin>
        <YMargin>5</YMargin>
        <ZMargin>5</ZMargin>
    </Steppable>

All that is required is to specify amount of extra space (expressed in
units of pixels) that needs to be added to a tight box i.e. the box
whose sides just touch most peripheral cells' pixels.
