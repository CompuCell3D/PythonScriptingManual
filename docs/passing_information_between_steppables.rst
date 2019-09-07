Passing information between steppables
======================================

When you work with more than one steppable (and it is a good idea to
work with several steppables each of which has a well defined purpose) you
may sometimes need to access or change member variable of one steppable
inside the code of another steppable. The most straightforward method to implement exchange of
information between steppables is to create a global python module (global from simulation stand point),
lets call it, ``global_vars.py``. Lets declare ``shared_parameter`` inside ``global_vars.py`` :

.. code-block:: python

    shared_parameter = 10

then we declare two steppables (e.g. in two different files)

.. code-block:: python

    # file SteppableCommunication.py
    import global_vars

    class SteppableCommunicationSteppable(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)

        def step(self, mcs):

            print ('global_vars.shared_parameters=', global_vars.shared_parameters)


.. code-block:: python

    # file ExtraSteppable.py
    import global_vars

    class ExtraSteppable(SteppableBasePy):
        def __init__(self, frequency=1):
            SteppableBasePy.__init__(self, frequency)
            global_vars.shared_parameters = 25

        def step(self, mcs):
            print ("ExtraSteppable: This function is called every 1 MCS")



``ExtraSteppable`` modifies ``global_vars.shared_parameter`` and ``SteppableCommunicationSteppable`` access it.
You may , come up with more "refined" use case but this simple one illustrates core mechanism where we use additioinal python module (``global_vars.py``) to exchange information between different classes