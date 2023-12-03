
Forward Euler method for solving PDE's in CompuCell3D.
------------------------------------------------------

.. note::

   We present more complete derivations of explicit finite
   difference scheme for diffusion solver in "Introduction to Hexagonal
   Lattices in CompuCell3D" (http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf).

In CompuCell3D most of the solvers uses explicit schemes (Forward Euler
method) to obtain PDE solutions. Thus for the diffusion equation we
have:

.. math::
   :nowrap:

   \begin{eqnarray}
      \frac{\partial c}{\partial t} = \frac{\partial^2 c}{\partial^2 x}+\frac{\partial^2 c}{\partial^2 y}+\frac{\partial^2 c}{\partial^2 z}
   \end{eqnarray}

In a discretetized form we may write:

.. math::
   :nowrap:

   \begin{eqnarray}
      \frac{c(x,t+\delta t)-c(x,t)}{\delta t} = \\
      \frac{c(x+\delta x,t) - 2c(x,t) + c(x-\delta x, t)}{\delta x^2} \\
      + \frac{c(y+\delta y,t) - 2c(y,t) + c(y-\delta y, t)}{\delta y^2} \\
      +\frac{c(z+\delta z,t) - 2c(z,t) + c(z-\delta z, t)}{\delta z^2}
   \end{eqnarray}

where to save space we used shorthand notation:

.. math::
   :nowrap:

   \begin{eqnarray}
     c(x+\Delta x,y,z,t)) \equiv c(x+\Delta x,,t)) \\
     c(x,y,z,t) \equiv c(x,t)
   \end{eqnarray}

and similarly for other coordinates.

After rearranging terms we get the following expression:

.. math::
   :nowrap:

   \begin{eqnarray}
     c(x, t + \delta t) = \left [ \frac{\delta t}{\delta x^2} \sum_{i=neighbors} \left ( c(i,t) - c(x,t)\right )\right ] - c(x,t)
   \end{eqnarray}


where the sum over index :math:`i` goes over neighbors of point :math:`(x,y,z)`
and the neighbors will have the following concentrations: :math:`c(x+\delta x, t)`,
:math:`c(y+\delta y, t)`, :math:`c(z+\delta z, t)` .
