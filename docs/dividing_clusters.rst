Dividing Clusters (aka compartmental cells)
===========================================

So far we have shown examples of how to deal with cells which consisted
of only simple compartments. CC3D allows to use compartmental models
where a single cell is actually a cluster of compartments. A cluster is
a collection of cells with same clusterId . If you use "simple" (non-compartmentalized) cells
then you can check that each such cell has distinct id and clusterId. An
example of compartmental simulation can be found in
``CompuCellPythonTutorial/clusterMitosis``. The actual algorithm used to
divide clusters of cells is described in the appendix of the CompuCell3D
manual.

Let’s look at how we can divide "compact" clusters and by compact, we
mean "blob shaped" clusters:

.. code-block:: python

    class MitosisSteppableClusters(MitosisSteppableClustersBase):
        def __init__(self, _simulator, _frequency=1):
            MitosisSteppableClustersBase.__init__(self, _simulator, _frequency)

        def step(self, mcs):

            for cell in self.cellList:
                clusterCellList = self.getClusterCells(cell.clusterId)
                for cellLocal in clusterCellList:

            mitosisClusterIdList = []
            for compartmentList in self.clusterList:
                clusterId = 0
                clusterVolume = 0
                for cell in CompartmentList(compartmentList):
                    clusterVolume += cell.volume
                    clusterId = cell.clusterId

                if clusterVolume > 250:
                    mitosisClusterIdList.append(clusterId)
            for clusterId in mitosisClusterIdList:
                # to change mitosis mode uncomment one of the lines below
                self.divideClusterRandomOrientation(clusterId)
                # self.divideClusterOrientationVectorBased(clusterId,1,0,0)
                # self.divideClusterAlongMajorAxis(clusterId)
                # self.divideClusterAlongMinorAxis(clusterId)

        def updateAttributes(self):
            compartmentListParent = self.getClusterCells(self.parentCell.clusterId)

            for i in xrange(compartmentListParent.size()):
                compartmentListParent[i].targetVolume /= 2.0
            self.cloneParentCluster2ChildCluster()

The steppable is quite similar to the mitosis steppable which works for
non-compartmental cell. This time however, after mitosis happens you
have to reassign properties of ``children`` compartments and of ``parent``
compartments which usually means iterating over list of compartments.
Conveniently this iteration is quite simple and ``SteppableBasePy`` class
has a convenience function ``getClusterCells`` which returns a list of cells
belonging to a cluster with a given cluster id:

.. code-block:: python

    compartmentListParent = self.getClusterCells(self.parentCell.clusterId)

The call above returns a list of cells in a cluster with ``clusterID``
specified by ``self.parentCell.clusterId``. In the subsequent for loop we
iterate over list of cells in the parent cluster and assign appropriate
values of volume constraint parameters. Notice that
compartmentListParent is indexable (ie. we can access directly any
element of the list provided our index is not out of bounds).

.. code-block:: python

    for i in xrange(compartmentListParent.size()):
        compartmentListParent[i].targetVolume /= 2.0

Notice that nowhere in the update attribute function we have modified
cell types. This is because, by default, cluster mitosis module assigns
cell types to all the cells of child cluster and it does it in such a
way so that child cell looks like a quasi-clone of parent cell.

The next call in the ``updateAttributes`` function is
``self.cloneParentCluster2ChildCluster()``. This copies all the attributes
of the cells in the parent cluster to the corresponding cells in the
child cluster. If you would like to copy attributes from parent to child
cell skipping select ones you may use the following code:

.. code-block:: python

    compartmentListParent = self.getClusterCells(self.parentCell.clusterId)

    compartmentListChild = self.getClusterCells(self.childCell.clusterId)

    self.cloneClusterAttributes(self, sourceCellCluster=compartmentListParent,
                                targetCellCluster=compartmentListChild,
                                no_clone_key_dict_list=['ATTR_NAME_1', 'ATTR_NAME_2'])

where ``cloneClusterAttributes`` function allows specification of this
attributes are not to be copied (in our case ``cell.dict`` members
``ATTR_NAME_1`` and ``ATTR_NAME_2`` will not be copied).

Finally, if you prefer manual setting of the parent and child cells you
would use the flowing code:

.. code-block:: python

    class MitosisSteppableClusters(MitosisSteppableClustersBase):
        def __init__(self, _simulator, _frequency=1):
            MitosisSteppableClustersBase.__init__(self, _simulator, _frequency)

        def step(self, mcs):

            mitosisClusterIdList = []
            for compartmentList in self.clusterList:
                clusterId = 0
                clusterVolume = 0
                for cell in CompartmentList(compartmentList):
                    clusterVolume += cell.volume
                    clusterId = cell.clusterId

                if clusterVolume > 250:
                    mitosisClusterIdList.append(clusterId)

            for clusterId in mitosisClusterIdList:
                # to change mitosis mode uncomment one of the lines below
                self.divideClusterRandomOrientation(clusterId)
                # self.divideClusterOrientationVectorBased(clusterId,1,0,0)
                # self.divideClusterAlongMajorAxis(clusterId)
                # self.divideClusterAlongMinorAxis(clusterId)

        def updateAttributes(self):

            parentCell = self.mitosisSteppable.parentCell
            childCell = self.mitosisSteppable.childCell

            compartmentListChild \
                = self.getClusterCells(childCell.clusterId)
            compartmentListParent \
                = self.getClusterCells(parentCell.clusterId)

            for i in xrange(compartmentListChild.size()):
                compartmentListParent[i].targetVolume /= 2.0

                compartmentListChild[i].targetVolume \
                    = compartmentListParent[i].targetVolume
                compartmentListChild[i].lambdaVolume \
                    = compartmentListParent[i].lambdaVolume


Python helper for mitosis is available from Twedit++
``CC3D Python->Mitosis``.
