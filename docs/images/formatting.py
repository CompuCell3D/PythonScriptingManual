class ContactSteeringAndTemperature(SteppableBasePy):
    def __init__(self, _simulator, _frequency=10):
        SteppableBasePy.__init__(self, _simulator, _frequency)

    def step(self, mcs):
        temp = float(self.getXMLElementValue(['Potts'], ['Temperature']))
        self.setXMLElementValue(temp + 1, ['Potts'], ['Temperature'])

        val = float(
            self.getXMLElementValue(
                ['Plugin', 'Name', 'Contact'], ['Energy', 'Type1', 'NonCondensing', 'Type2', 'Condensing']))

        self.setXMLElementValue(
            val + 1, ['Plugin', 'Name', 'Contact'], ['Energy', 'Type1', 'NonCondensing', 'Type2', 'Condensing']
        )

        self.updateXML()
