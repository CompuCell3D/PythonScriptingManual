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
