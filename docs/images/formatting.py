class DemoVisSteppable(SteppableBasePy):
    def __init__(self, _simulator, _frequency=1):
        SteppableBasePy.__init__(self, _simulator, _frequency)
        self.track_cell_level_scalar_attribute(field_name='COM_RATIO',
                                               attribute_name='ratio')

        import math
        self.track_cell_level_scalar_attribute(field_name='SIN_COM_RATIO',
                                               attribute_name='ratio',
                                               function=lambda attr_val: math.sin(attr_val))

    def start(self):
        for cell in self.cellList:
            cell.dict['ratio'] = cell.xCOM / cell.yCOM

    def step(self, mcs):
        for cell in self.cellList:
            cell.dict['ratio'] = cell.xCOM / cell.yCOM
