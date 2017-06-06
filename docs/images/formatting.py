self.field = self.getConcentrationField('ATTR')
lmfLength = 1.0;
xScale = 1.0
yScale = 1.0
zScale = 1.0
# FOR HEX LATTICE IN 2D
#         lmfLength=sqrt(2.0/(3.0*sqrt(3.0)))*sqrt(3.0)
#         xScale=1.0
#         yScale=sqrt(3.0)/2.0
#         zScale=sqrt(6.0)/3.0

for cell in self.cellList:
    # converting from real coordinates to pixels
    xCM = int(cell.xCOM / (lmfLength * xScale))
    yCM = int(cell.yCOM / (lmfLength * yScale))

    if cell.type == 3:
        self.field[xCM, yCM, 0] = self.field[xCM, yCM, 0] + 10.0
