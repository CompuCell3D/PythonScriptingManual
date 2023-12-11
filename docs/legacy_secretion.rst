
Secretion Plugin (legacy version for pre-v3.5.0)
-----------------------------------------------------

.. warning::

    While we still support ``Secretion`` plugin as described
    in this section, we observed performance degradation when declaring
    ``<Field>`` elements inside the plugin. To resolve this issue we encourage
    users to implement secretion "by cell type" in the PDE solver and keep
    using secretion plugin to implement secretion on a per-cell basis using
    Python scripting.

.. note::

    In version 3.6.2 ``Secretion`` plugin should not be used with
    ``DiffusionSolverFE`` or any of the GPU-based solvers.

In earlier versions of CC3D, secretion was part of PDE solvers. We
still support this mode of model description however, starting in 3.5.0
we developed separate plugin which handles secretion only. Via secretion
plugin we can simulate cellular secretion of various chemicals. The
secretion plugin allows users to specify various secretion modes in the
CC3DML file – CC3DML syntax is practically identical to the
SecretionData syntax of PDE solvers. In addition to this Secretion
plugin allows users to manipulate secretion properties of individual
cells from Python level. To account for possibility of PDE solver being
called multiple times during each MCS, the ``Secretion`` plugin can be
called multiple times in each MCS as well. We leave it up to user the
rescaling of secretion constants when using multiple secretion calls in
each MCS.

.. note::

    Secretion for individual cells invoked via Python
    will be called only once per MCS.

Typical CC3DML syntax for Secretion plugin is presented below:

.. code-block:: xml

    <Plugin Name="Secretion">
        <Field Name="ATTR" ExtraTimesPerMC=”2”>
            <Secretion Type="Bacterium">200</Secretion>
            <SecretionOnContact Type="Medium" SecreteOnContactWith="B">300</SecretionOnContact>
            <ConstantConcentration Type="Bacterium">500</ConstantConcentration>
        </Field>
    </Plugin>



By default ``ExtraTimesPerMC`` is set to ``0`` - meaning no extra calls to
``Secretion`` plugin per MCS.

Typical use of secretion from Python is demonstrated best in the example
below:

.. code-block:: python

    class SecretionSteppable(SecretionBasePy):
        def __init__(self, _simulator, _frequency=1):
            SecretionBasePy.__init__(self, _simulator, _frequency)

        def step(self, mcs):
            attrSecretor = self.getFieldSecretor("ATTR")
            for cell in self.cellList:
                if cell.type == 3:
                    attrSecretor.secreteInsideCell(cell, 300)
                    attrSecretor.secreteInsideCellAtBoundary(cell, 300)
                    attrSecretor.secreteOutsideCellAtBoundary(cell, 500)
                    attrSecretor.secreteInsideCellAtCOM(cell, 300)

