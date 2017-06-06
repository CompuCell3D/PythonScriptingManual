for cell in self.cellList:
    if cell.type == self.MACROPHAGE:
        cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ATTR")
        cd.setLambda(30.0)
        cd.setSaturationCoef(100)
        cd.assignChemotactTowardsVectorTypes([self.MEDIUM, self.BACTERIUM])

