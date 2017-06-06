def step(self, mcs):
    for cell in self.cellList:
        cell.dict["Double_MCS_ID"] = mcs * 2 * cell.id

    for cell in self.cellList:
        print 'cell.id=', cell.id, ' dict=', cell.dict
