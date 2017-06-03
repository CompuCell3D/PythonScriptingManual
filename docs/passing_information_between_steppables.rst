Passing information between steppables
======================================

When you work with more than one steppable (and it is a good idea to
work with several steppables each of which has well defined purpose) you
may sometimes need to acces/change member variable of one steppable
inside the code of another steppable. If you are seasoned Python
programmer, you can easily find workaround. However, we have added a
convenience function to SteppableBasePy class that makes accessing
content of one steppable from another module very easy and, let’s say,
elegant. Here is an example (see also
``Demos/CompuCellPythonTutorial/SteppableCommunication``):

.. code-block:: python

    class SteppableCommunicationSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=1):
            SteppableBasePy.__init__(self, _simulator, _frequency)

        def step(self, mcs):
            extraSteppable = self.getSteppableByClassName('ExtraSteppable')
            print 'extraSteppable.sharedParameter=', extraSteppable.sharedParameter


    class ExtraSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=1):
            SteppableBasePy.__init__(self, _simulator, _frequency)
            self.sharedParameter = 25

        def step(self, mcs):
            print "ExtraSteppable: This function is called every 1 MCS"


In the ``SteppableCommunicationSteppable`` class, inside step function we
fetch (using class name) another ``ExtraSteppble`` steppable. Once we have
access to object of type ``ExtraSteppble`` we can access/change parameters
of this steppable.

**Remark:** This approach will work fine if you create only one
steppable object for each steppable class. In case you create two
objects of the same steppable class, the presented method fails.
However, most, if not all, CC3D simulations rely on an unwritten rule -
one steppable object for each steppable class.
