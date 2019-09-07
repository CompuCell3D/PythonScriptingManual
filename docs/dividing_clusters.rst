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

    from cc3d.core.PySteppables import *


    class MitosisSteppableClusters(MitosisSteppableClustersBase):

        def __init__(self, frequency=1):
            MitosisSteppableClustersBase.__init__(self, frequency)

        def step(self, mcs):

            for cell in self.cell_list:
                cluster_cell_list = self.get_cluster_cells(cell.clusterId)
                print("DISPLAYING CELL IDS OF CLUSTER ", cell.clusterId, "CELL. ID=", cell.id)
                for cell_local in cluster_cell_list:
                    print("CLUSTER CELL ID=", cell_local.id, " type=", cell_local.type)

            mitosis_cluster_id_list = []
            for compartment_list in self.clusterList:
                # print( "cluster has size=",compartment_list.size())
                cluster_id = 0
                cluster_volume = 0
                for cell in CompartmentList(compartment_list):
                    cluster_volume += cell.volume
                    cluster_id = cell.clusterId

                # condition under which cluster mitosis takes place
                if cluster_volume > 250:
                    # instead of doing mitosis right away we store ids for clusters which should be divide.
                    # This avoids modifying cluster list while we iterate through it
                    mitosis_cluster_id_list.append(cluster_id)

            for cluster_id in mitosis_cluster_id_list:

                self.divide_cluster_random_orientation(cluster_id)

                # # other valid options - to change mitosis mode leave one of the below lines uncommented
                # self.divide_cluster_orientation_vector_based(cluster_id, 1, 0, 0)
                # self.divide_cluster_along_major_axis(cluster_id)
                # self.divide_cluster_along_minor_axis(cluster_id)

        def update_attributes(self):
            # compartments in the parent and child clusters are
            # listed in the same order so attribute changes require simple iteration through compartment list
            compartment_list_parent = self.get_cluster_cells(self.parent_cell.clusterId)

            for i in range(len(compartment_list_parent)):
                compartment_list_parent[i].targetVolume /= 2.0
            self.clone_parent_cluster_2_child_cluster()


The steppable is quite similar to the mitosis steppable which works for
non-compartmental cell. This time however, after mitosis happens you
have to reassign properties of ``children`` compartments and of ``parent``
compartments which usually means iterating over list of compartments.
Conveniently this iteration is quite simple and ``SteppableBasePy`` class
has a convenience function ``get_cluster_cells`` which returns a list of cells
belonging to a cluster with a given cluster id:

.. code-block:: python

    compartment_list_parent = self.get_cluster_cells(self.parent_cell.clusterId)

The call above returns a list of cells in a cluster with ``clusterId``
specified by ``self.parent_cell.clusterId``. In the subsequent for loop we
iterate over list of cells in the parent cluster and assign appropriate
values of volume constraint parameters. Notice that
``compartment_list_parent`` is indexable (ie. we can access directly any
element of the list provided our index is not out of bounds).

.. code-block:: python

    for i in range(len(compartment_list_parent)):
        compartment_list_parent[i].targetVolume /= 2.0

Notice that nowhere in the update attribute function we have modified
cell types. This is because, by default, cluster mitosis module assigns
cell types to all the cells of child cluster and it does it in such a
way so that child cell looks like a quasi-clone of parent cell.

The next call in the ``update_attributes`` function is
``self.clone_parent_cluster_2_child_cluster()``. This copies all the attributes
of the cells in the parent cluster to the corresponding cells in the
child cluster. If you would like to copy attributes from parent to child
cell skipping select ones you may use the following code:

.. code-block:: python

    compartment_list_parent = self.get_cluster_cells(self.parent_cell.clusterId)

    compartment_lis_child = self.get_cluster_cells(self.child_cell.clusterId)

    self.clone_cluster_attributes(source_cell_cluster=compartment_list_parent,
                                target_cell_cluster=compartment_list_child,
                                no_clone_key_dict_list=['ATTR_NAME_1', 'ATTR_NAME_2'])

where ``clone_cluster_attributes`` function allows specification of this
attributes are not to be copied (in our case ``cell.dict`` members
``ATTR_NAME_1`` and ``ATTR_NAME_2`` will not be copied).

Finally, if you prefer manual setting of the parent and child cells you
would use the flowing code:

.. code-block:: python

    class MitosisSteppableClusters(MitosisSteppableClustersBase):

        def __init__(self, frequency=1):
            MitosisSteppableClustersBase.__init__(self, frequency)

        def step(self, mcs):

            for cell in self.cell_list:
                cluster_cell_list = self.get_cluster_cells(cell.clusterId)
                print("DISPLAYING CELL IDS OF CLUSTER ", cell.clusterId, "CELL. ID=", cell.id)
                for cell_local in cluster_cell_list:
                    print("CLUSTER CELL ID=", cell_local.id, " type=", cell_local.type)

            mitosis_cluster_id_list = []
            for compartment_list in self.clusterList:
                # print( "cluster has size=",compartment_list.size())
                cluster_id = 0
                cluster_volume = 0
                for cell in CompartmentList(compartment_list):
                    cluster_volume += cell.volume
                    cluster_id = cell.clusterId

                # condition under which cluster mitosis takes place
                if cluster_volume > 250:
                    # instead of doing mitosis right away we store ids for clusters which should be divide.
                    # This avoids modifying cluster list while we iterate through it
                    mitosis_cluster_id_list.append(cluster_id)

            for cluster_id in mitosis_cluster_id_list:

                self.divide_cluster_random_orientation(cluster_id)

                # # other valid options - to change mitosis mode leave one of the below lines uncommented
                # self.divide_cluster_orientation_vector_based(cluster_id, 1, 0, 0)
                # self.divide_cluster_along_major_axis(cluster_id)
                # self.divide_cluster_along_minor_axis(cluster_id)

        def updateAttributes(self):

            parent_cell = self.mitosisSteppable.parentCell
            child_cell = self.mitosisSteppable.childCell

            compartment_list_child = self.get_cluster_cells(child_ell.clusterId)
            compartment_list_parent = self.get_cluster_cells(parent_cell.clusterId)

            for i in range(len(compartment_list_child)):
                compartment_list_parent[i].targetVolume /= 2.0

                compartment_list_child[i].targetVolume = compartment_list_parent[i].targetVolume
                compartment_list_child[i].lambdaVolume = compartment_list_parent[i].lambdaVolume


Python helper for mitosis is available from Twedit++
``CC3D Python->Mitosis``.
