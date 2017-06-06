class VectorFieldVisualizationSteppable(SteppableBasePy):
    def __init__(self, _simulator, _frequency=10):
        SteppableBasePy.__init__(self, _simulator, _frequency)
        self.vectorField = self.createVectorFieldPy("VectorField")

    def step(self, mcs):
        self.vectorField[:, :, :, :] = 0.0  # clear vector field

        for x, y, z in self.everyPixel(10, 10, 5):
            self.vectorField[x, y, z] = [x * random(), y * random(), z * random()]
