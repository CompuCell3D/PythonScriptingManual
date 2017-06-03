def step(self, mcs):
    for cell in self.cellList:
        if cell.type == self.CONDENSING:
            self.deleteCell(cell)
