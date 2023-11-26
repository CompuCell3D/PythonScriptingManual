ReactionDiffusionSolver
-----------------------

The reaction diffusion solver solves the following system of N reaction
diffusion equations:

.. math::
    :nowrap:

    \begin{align*}
     \frac{\partial c_1}{\partial t} = D \nabla^2c_1-kc_1+\text{secretion} + f_1(c_1,c_2,...,c_N, W) \\
     \frac{\partial c_2}{\partial t} = D \nabla^2c_2-kc_2+\text{secretion} + f_2(c_1,c_2,...,c_N,W) \\
     {\text ...} \\
     \frac{\partial c_N}{\partial t} = D \nabla^2c_N-kC_N+\text{secretion} + f_N(c_1,c_2,...,c_N, W)
    \end{align*}

where ``W`` denotes cell type

Let's consider a simple example of such system:

.. math::
    :nowrap:

    \begin{align*}
     \frac{\partial F}{\partial t} = 0.1 \nabla^2F - 0.1H \\
     \frac{\partial H}{\partial t} = 0.0 \nabla^2H + 0.1F
    \end{align*}


It can be coded as follows:

.. code-block:: xml

    <Steppable Type="ReactionDiffusionSolverFE">
      <AutoscaleDiffusion/>
      <DiffusionField Name="F">
        <DiffusionData>
          <FieldName>F</FieldName>
          <DiffusionConstant>0.010</DiffusionConstant>
          <ConcentrationFileName>
          Demos/diffusion/diffusion_2D.pulse.txt
          </ConcentrationFileName>
          <AdditionalTerm>-0.01*H</AdditionalTerm>
        </DiffusionData>
      </DiffusionField>

      <DiffusionField Name="H">
        <DiffusionData>
          <FieldName>H</FieldName>
          <DiffusionConstant>0.0</DiffusionConstant>
          <AdditionalTerm>0.01*F</AdditionalTerm>
        </DiffusionData>
      </DiffusionField>
    </Steppable>

Notice how we implement functions ``f`` from the general system of
reaction diffusion equations. We simply use ``<AdditionalTerm>`` tag and
there we type arithmetic expression involving field names (tags
``<FieldName>``). In addition to this we may include in those expression
word ``CellType``. For example:

.. code-block:: xml

    <AdditionalTerm>0.01*F*CellType</AdditionalTerm>

This means that function ``f`` will depend also on ``CellType`` . ``CellType``
holds the value of the type of the cell at particular location - ``x``, ``y``, ``z``
- of the lattice. The inclusion of the cell type might be useful if you
want to use additional terms which may change depending of the cell
type. Then all you have to do is to either use if statements inside
``<AdditionalTerm>`` or form equivalent mathematical expression using
functions allowed by ``muParser``: http://muparser.sourceforge.net/mup_features.html#idDef2

For example, let's assume that additional term for second equation is
the following:

.. math::
    :nowrap:

        f_F  =
         \begin{cases}
               0.1F  && \text{if CellType=1}\\
                0.51F  && \text{otherwise}
            \end{cases}


In such a case additional term would be coded as follows:

.. code-block:: xml

    <AdditionalTerm>CellType==1 ? 0.01*F : 0.15*F</AdditionalTerm>

Notice that we have used here, so called ternary operator which might be
familiar to you from other programing languages such as C or C++ and is
equivalent to`` if-then-els``e statement

The syntax of the ternary (aka ``if-then-else`` statement) is as follows:

.. code-block:: xml

    condition ? expression if condition is true : expression if condition false

.. warning::
    **Important:** If change the above expression to

    .. code-block::xml

        <AdditionalTerm>CellType<1 ? 0.01*F : 0.15*F</AdditionalTerm>

    we will get an XML parsing error. Why? This i because  XML parser will think
    that ``<1`` is the beginning of the new XML element. To fix this you could
    use two approaches:

    1.Present your expression as ``CDATA``

    .. code-block:: xml

        <AdditionalTerm>
            <![CDATA[
            CellType<1 ? 0.01*F : 0.15*F
            ]]>
        </AdditionalTerm>

    In this case XML parser will correctly interpret the expression enclosed
    between ``<![CDATA[`` and ``]]>`` .

    2. Replace XML using equivalent Python syntax - see (http://pythonscriptingmanual.readthedocs.io/en/latest/replacing_cc3dml_with_equivalent_python_syntax.html)
    in which case you would code the above XML element as the following Python statement:

    .. code-block:: python

        DiffusionDataElmnt\_2.ElementCC3D('AdditionalTerm', {}, 'CellType<1 ? 0.01*F : 0.15*F')

    The moral from this story is that if like to use muParser in the XML
    file make sure to use this general syntax:

    .. code-block:: xml

        <AdditionalTerm>
            <![CDATA[
                YOUR EXPRESSION
            ]]>
        </AdditionalTerm>

One thing to remember is that computing time of the additional term
depends on the level of complexity of this term. Thus, you might get some
performance degradation for very complex expressions coded in muParser

Similarly as in the case of ``FlexibleDiffusionSolverFE`` we may use
``<AutoscaleDiffusion>`` tag tells CC3D to automatically rescale diffusion
constant. See section ``FlexibleDiffusionSolver`` or the ``Appendix`` for more
information.
