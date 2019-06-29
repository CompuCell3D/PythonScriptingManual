Calculating distances in CC3D simulations.
==========================================

This may seem like a trivial task. After all, Pitagorean theorem is one
of the very first theorems that people learn in basic mathematics
course. The purpose of this section is to present convenience functions
which will make your code more readable. You can easily code such
functions yourself but you probably will save some time if you use ready
solutions. One of the complications in the CC3D is that sometimes you
may run simulation using periodic boundary conditions. If that’s the
case, imagine two cells close to the right hand side border of the
lattice and moving to the right. When we have periodic boundary
conditions along X axis one of such cells will cross lattice boundary
and will appear on the left hand side of the lattice. What should be a
distance between cells before and after once of them crosses lattice
boundary? Clearly, if we use a naïve formula the distance between cells
will be small when all cells are close to righ hand side border but if
one of them crosses the border the distance calculated using the simple
formula will jump dramatically. Intuitively we feel that this is
incorrect. The way solve this problem is by shifting one cell to
approximately center of the lattice and than applying the same shift to
the other cell. If the other cell ends up outside of the lattice we add
a vector whose components are equal to dimensions of the lattice but
only along this axes along which we have periodic boundary conditions.
The point here is to bring a cell which ends up outside the lattice to
beinside using vectors with components equal to the lattice dimensions.
The net result of these shifts is that we have two cells in the middle
of the lattice and the distance between them is true distance regardless
the type of boundary conditions we use. You should realize that when we
talk about cell shifting we are talking only about calculations and not
physical shifts that occur on the lattice.

Example ``CellDistance`` from ``CompuCellPythonTutorial`` directory
demonstrates the use of the functions calculating distance between
cells or between any 3D points:

.. code-block:: python




    class CellDistanceSteppable(SteppableBasePy):

        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)
            self.cellA = None
            self.cellB = None

        def start(self):
            self.cellA = self.potts.createCell()
            self.cellA.type = self.A
            self.cell_field[10:12, 10:12, 0] = self.cellA

            self.cellB = self.potts.createCell()
            self.cellB.type = self.B
            self.cell_field[92:94, 10:12, 0] = self.cellB

        def step(self, mcs):
            dist_vec = self.invariant_distance_vector_integer(p1=[10, 10, 0], p2=[92, 12, 0])

            print('dist_vec=', dist_vec, ' norm=', self.vector_norm(dist_vec))

            dist_vec = self.invariant_distance_vector(p1=[10, 10, 0], p2=[92.3, 12.1, 0])
            print('dist_vec=', dist_vec, ' norm=', self.vector_norm(dist_vec))

            print('distance invariant=', self.invariant_distance(p1=[10, 10, 0], p2=[92.3, 12.1, 0]))

            print('distance =', self.distance(p1=[10, 10, 0], p2=[92.3, 12.1, 0]))

            print('distance vector between cells =', self.distance_vector_between_cells(self.cellA, self.cellB))
            print('invariant distance vector between cells =',
                  self.invariant_distance_vector_between_cells(self.cellA, self.cellB))
            print('distanceBetweenCells = ', self.distance_between_cells(self.cellA, self.cellB))
            print('invariantDistanceBetweenCells = ', self.invariant_distance_between_cells(self.cellA, self.cellB))

In the start function we create two cells – ``self.cellA`` and ``self.cellB``.
In the step function we calculate invariant distance vector between two
points using ``self.invariant_distance_vector_integer`` function. Notice that
the word Integer in the function name suggests that the result of this
call will be a vector with integer components. Invariant distance vector
is a vector that is obtained using our shifting operations described
earlier.

The next function used inside step is ``self.vector_norm``. It returns length
of the vector. Notice that we specify vectors or 3D points in space
using ``[]`` operator. For example to specify vector, or a point with
coordinates ``x, y, z = (10, 12, -5)`` you use the following syntax:

.. code-block:: python

    [10, 12, -5]

If we want to calculate invariant vector but with components being
floating point numbers we use ``self.invariant_distance_vector`` function. You
may ask why not using floating point always? The reason is that
sometimes CC3D expects vectors/points with integer coordinates to e.g.
access specific lattice points. By using appropriate distance functions
you may write cleaner code and avoid casting and rounding operators.
However this is a matter of taste and if you prefer using floating point
coordinates it is perfectly fine. Just be aware that when converting
floating point coordinate to integer you need to use round and int
functions.

Function self.distance calculates distance between two points in a naïve
way. Sometimes this is all you need. Finally the set of last four calls
``self.distance_vector_between_cells``,
``self.invariant_distance_vector_between_cells``, ``self.distance_between_cells``,
``self.invariant_distance_between_cells`` calculates distances and vectors
between center of masses of cells. You could replace

.. code-block:: python

    self.invariant_distance_vector_between_cells(self.cellA,self.cellB)

with

.. code-block:: python

    self.invariant_distance_vector_between(
        p1=[ self.cellA.xCOM, self.cellA.yCOM, self.cellA.yCOM],
        p2=[ self.cellB.xCOM, self.cellB.yCOM, self.cellB.yCOM]
     )

but it is not hard to notice that the former is much easier to read.
