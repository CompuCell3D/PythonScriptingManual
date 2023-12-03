muParser
--------

CC3D uses ``muParser`` to allow users specify simple mathematical
expressions in the XML (or XML-equivalent Python scripts). The following
link points to full specification of the ``muParser``:
http://muparser.sourceforge.net/mup_features.html#idDef2. The general
guideline to using muParser syntax inside XML is to enclose ``muParser``
expression between ``<![CDATA[ and ]]>`` :

.. code-block:: xml

    <XML_ELEMENT_WITH_MUPARSER_EXPRESSION>
        <![CDATA[
            MUPARSER EXPRESSION
        ]]>
    </XML_ELEMENT_WITH_MUPARSER_EXPRESSION>

For example:

.. code-block:: xml

    <AdditionalTerm>
        <![CDATA[
            CellType<1 ? 0.01*F : 0.15*F
        ]]>
    </AdditionalTerm>

The reason for enclosing ``muParser`` expression between ``<![CDATA[`` and ``]]>``
is to prevent XML parser from interpreting ``<`` or ``>`` as beginning or end of
the XML elements

Alternatively you may replace XML with equivalent Python syntax in which
case things will look a bit simpler:

.. code-block:: python

    DiffusionDataElmnt_2.ElementCC3D("AdditionalTerm",{}," CellType<1 ? 0.01*F : 0.15*F ")

