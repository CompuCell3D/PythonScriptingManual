FastDiffusionSolver2D
---------------------

.. note::

    The current implementation of ``DiffusionSolverFE`` may actually be faster than this legacy module. So
    before commiting to it please verify the performance of teh ``DiffusionSolverFE`` vs ``FastDiffusionSolverFE``

``FastDiffusionSolver2DFE`` module is a simplified version of the
``FlexibleDiffusionSolverFE`` steppable. It runs several times faster that
flexible solver but lacks some of its features. Typical syntax is shown
below:

.. code-block:: xml

    <Steppable Type="FastDiffusionSolver2DFE">
       <DiffusionField Name="FGF">
         <DiffusionData>
           <UseBoxWatcher/>
           <FieldName>FGF</FieldName>
           <DiffusionConstant>0.010</DiffusionConstant>
           <DecayConstant>0.003</DecayConstant>
         <ExtraTimesPerMCS>2</ExtraTimesPerMCS>
           <DoNotDecayIn>Wall</DoNotDecay>
           <ConcentrationFileName>Demos/diffusion/diffusion_2D_fast_box.pulse.txt
           </ConcentrationFileName>
        </DiffusionData>
      </DiffusionField>
     </Steppable>

In particular, for fast solver you cannot specify cells into which
diffusion is prohibited. However, you may specify cell types where
diffusant decay is prohibited

For explanation on how ``<ExtraTimesPerMCS>`` tag works works see section on
``FlexibleDiffusionSolverFE``.

