Lattice Type
------------

Early versions of CompuCell3D allowed users to use only square lattice.
Most recent versions allow the simulation to be run on
hexagonal lattice as well.

.. note::

Full description of hexagonal lattice including detailed
derivations can be found in “Introduction to Hexagonal Lattices”
available from `http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf <http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf>`__

To enable hexagonal lattice you need to put

.. code-block:: xml

    <LatticeType>Hexagonal</LatticeType>

in the Potts section of the CC3DML configuration file.

There are few things to be aware of when using hexagonal lattice.
In 2D your pixels are hexagons but in 3D the voxels are rhombic dodecahedrons.
It is particularly important to realize that surface or perimeter of the pixel
(depending whether in 2D or 3D) is different than in the case of square
pixel. The way CompuCell3D hex lattice implementation was done was that
the volume of the pixel was constrained to be ``1`` regardless of the
lattice type.
There is also one to one correspondence between pixels of the square
lattice and pixels of the hex lattice. Consequently, we can come up with
transformation equations which give positions of hex pixels as a
function of square lattice pixel position:

.. math::
   :nowrap:

   \begin{cases}
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ \left ( x_{cart}+\frac{1}{2} \right ) L, \frac{\sqrt[]{3}}{2}y_{cart}L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=0 \text{ and } z \mod 3 = 0 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ x_{cart} L, \frac{\sqrt[]{3}}{2}y_{cart}L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=1 \text{ and } z \mod 3 = 0 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ x_{cart} L, \left ( \frac{\sqrt[]{3}}{2}y_{cart} +\frac{\sqrt[]{3}}{6} \right)L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=0 \text{ and } z \mod 3 = 1 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ \left ( x_{cart}+\frac{1}{2} \right ) L, \left ( \frac{\sqrt[]{3}}{2}y_{cart} +\frac{\sqrt[]{3}}{6} \right)L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=1 \text{ and } z \mod 3 = 1 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [  x_{cart}L, \left ( \frac{\sqrt[]{3}}{2}y_{cart} -\frac{\sqrt[]{3}}{6} \right)L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=0 \text{ and } z \mod 3 = 2 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [  \left ( x_{cart}+\frac{1}{2} \right ) L, \left ( \frac{\sqrt[]{3}}{2}y_{cart} -\frac{\sqrt[]{3}}{6} \right)L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=1 \text{ and } z \mod 3 = 2 \\
   \end{cases}


Based on the above facts one can work out how unit length and unit
surface transform to the hex lattice. The conversion factors are given
below:


.. math::
   :nowrap:

   \begin{eqnarray}
      S_{hex-unit}=\sqrt[]{\frac{2}{3\sqrt[]{3}}}\approx 0.6204
   \end{eqnarray}

For the 2D case, assuming that each pixel has unit volume, we get:

.. math::
   :nowrap:

   \begin{eqnarray}
      L_{hex-unit}=\sqrt[]{\frac{2}{\sqrt[]{3}}}\approx 1.075
   \end{eqnarray}


where :math:`S_{hex-unit}` denotes length of the hexagon and :math:`L_{hex-unit}` denotes a distance between
centers of the hexagons. Notice that unit surface in 2D is simply a
length of the hexagon side and surface area of the hexagon with side ``a``
is:

.. math::
   :nowrap:

   \begin{eqnarray}
      S = 6\frac{{\sqrt[]{3}}}{4}a^2
   \end{eqnarray}

In 3D we can derive the corresponding unit quantities starting with the
formulae for volume and surface of rhombic dodecahedron (12 hedra)

.. math::
   :nowrap:

   \begin{align*}
       &V = \frac{16}{9}{\sqrt[]{3}}a^3 \\
       &S = 8{\sqrt[]{2}}a^2
   \end{align*}

where ``a`` denotes length of dodecahedron edge.

Constraining the volume to be ``1`` we get:

.. math::
   :nowrap:

   \begin{eqnarray}
      a = \sqrt[3]{\frac{9V}{16\sqrt[]{3}}}
   \end{eqnarray}


and thus unit surface is given by:

.. math::
   :nowrap:

   \begin{eqnarray}
      S_{unit-hex} = \frac{S}{12} = \frac{8\sqrt[]{2}}{12}\sqrt[3]{\frac{9V}{16\sqrt[]{3}}}\approx 0.445
   \end{eqnarray}

and unit length by:

.. math::
   :nowrap:

   \begin{eqnarray}
      L_{unit-hex} = 2\frac{\sqrt[]{2}}{\sqrt[]{3}}a = 2\frac{\sqrt[]{2}}{\sqrt[]{3}} \sqrt[3]{\frac{9V}{16\sqrt[]{3}}}\approx 1.122
   \end{eqnarray}

