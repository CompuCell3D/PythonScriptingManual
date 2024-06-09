Appendix B: List of Cell Attributes
=============================================

In this appendix, we present an alphabetical list of CellG attributes:

clusterId`` - cluster id

``clusterSurface`` - total surface of a cluster that a given cell belongs
to. Needs ClusterSurface Plugin

``dict`` - stores any custom attributes you wish to assign to the cell

``ecc`` - eccentricity of cell . Needs MomentOfInertia plugin

``extraAttribPtr`` - a C++ pointer to Python dictionary attached to each
cell

``flag`` - integer ``variable`` - unused. Can be used from Python

``fluctAmpl`` - fluctuation amplitude. Default value ``is`` -1

``iXX`` - xx component of inertia tensor. Needs MomentOfInertia Plugin

``iXY``- xy component of inertia tensor. Needs MomentOfInertia Plugin

``iXZ``- xz component of inertia tensor. Needs MomentOfInertia Plugin

``iYY``- yy component of inertia tensor. Needs MomentOfInertia Plugin

``iYZ``- yz component of inertia tensor. Needs MomentOfInertia Plugin

``iZZ``- zz component of inertia tensor. Needs MomentOfInertia Plugin

``id`` - cell id

``lX`` - x component of orientation vector. Set by MomentOfInertia

``lY`` - y component of orientation vector. Set by MomentOfInertia

``lZ`` - z component of orientation vector. Set by MomentOfInertia

``lambdaClusterSurface`` - lambda (constraint strength) of cluster surface
constraint.Needs ClusterSurface Plugin

``lambdaSurface`` - lambda (constraint strength) of surface constraint.
Needs Surface Plugin

``lambdaVecX`` - x component of force applied to cell. Needs
ExternalPotential Plugin

``lambdaVecY`` - y component of force applied to cell. Needs
ExternalPotential Plugin

``lambdaVecZ`` - z component of force applied to cell. Needs
ExternalPotential Plugin

``lambdaVolume`` - lambda (constraint strength) of volume constraint. Needs
Volume Plugin

``subtype`` - currently unused

``surface`` - instantaneous cell surface. Needs Surface plugin

``targetClusterSurface`` - target value of cluster surface constraint.Needs
ClusterSurface Plugin

``targetSurface`` - target value of surface constraint. Needs Surface Plugin

``targetVolume`` - target value of volume constraint. Needs Volume Plugin

``type`` - cell type

``volume`` - instantaneous cell volume. Needs VolumeTracker plugin which is
loaded by default by every CC3D simulation.

``xCM`` - numerator of x-component expression for cell centroid

``xCOM`` - x component of cell centroid

``xCOMPrev`` - x component of cell centroid from previous MCS

``yCM`` - numerator of y-component expression for cell centroid

``yCOM`` - y component of cell centroid

``yCOMPrev`` - y component of cell centroid from previous MCS

``zCM`` - numerator of z-component expression for cell centroid

``zCOM`` - z component of cell centroid

``zCOMPrev`` - z component of cell centroid from previous MCS
