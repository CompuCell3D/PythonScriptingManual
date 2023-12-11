Secretion Plugin Reference
======================================================

Related: 
    - `Secretion Guide <secretion.html>`_
    - `Field Secretion <field_secretion.html>`_ 
    - `Secretion (legacy version for pre-v3.5.0) <legacy_secretion.html>`_
    
****************************************

.. _SecretionReference:

FieldSecretor Methods
****************************

Secretion Modes
--------------------------

1. ``secreteInsideCell(cell, concentration: float) -> bool`` – secretion will occur
on every one of the given cell's pixels. 
``concentration`` determines how much to increase the amount of the field
present at that pixel. 

2. ``secreteInsideCellConstantConcentration(cell, concentration: float) -> bool`` – secretion will occur
on every one of the given cell's pixels.
The concentration will be fixed and uniform across all pixels. 

3. ``secreteInsideCellAtBoundary(cell, concentration: float) -> bool`` – secretion takes place in
pixels that are part of the cell's boundary.

4. ``secreteInsideCellAtBoundaryOnContactWith(cell, concentration: float, cell_types: list) -> bool`` - secretion takes place in
pixels that are part of the cell's boundary (i.e., its outermost pixels). 
Secretion only happens on pixels that are in contact with cells listed in ``cell_types``.

5. ``secreteOutsideCellAtBoundary(cell, concentration: float) -> bool`` – secretion takes place in
pixels that are outside the cell but touching its boundary. 

6. ``secreteOutsideCellAtBoundaryOnContactWith(cell, concentration: float, cell_types: list) -> bool`` - secretion takes place in
pixels that are outside the cell but touching its boundary. 
Secretion only happens on pixels that are in contact with cells listed in ``cell_types``.

7. ``secreteInsideCellAtCOM(cell, concentration: float) -> bool`` – secretion at 
the center of mass of the cell


Uptake Modes
--------------------------

    **Important:** Uptake works as follows: when available concentration
    is greater than ``max_amount``, then ``max_amount`` is subtracted from
    ``current_concentration``, otherwise we subtract
    ``relative_uptake*current_concentration``.
    Typically, ``max_amount`` is >=1.0 while ``relative_uptake`` is between 0 and 1.0.

1. ``uptakeInsideCell(cell, max_amount: float, relative_uptake: float) -> bool`` – uptake will occur
on every one of the given cell's pixels.

2. ``uptakeInsideCellAtBoundary(cell, max_amount: float, relative_uptake: float) -> bool`` – uptake takes place in
pixels that are part of the cell's boundary.

3. ``uptakeInsideCellAtBoundaryOnContactWith(cell, max_amount: float, relative_uptake: float, cell_types: list) -> bool`` - uptake takes place in
pixels that are part of the cell's boundary (i.e., its outermost pixels). 
Uptake only happens on pixels that are in contact with cells listed in ``cell_types``.

4. ``uptakeOutsideCellAtBoundary(cell, max_amount: float, relative_uptake: float) -> bool`` – uptake takes place in
pixels that are outside the cell but touching its boundary. 

5. ``uptakeOutsideCellAtBoundaryOnContactWith(cell, max_amount: float, relative_uptake: float, cell_types: list) -> bool`` - uptake takes place in
pixels that are outside the cell but touching its boundary. 
Uptake only happens on pixels that are in contact with cells listed in ``cell_types``.

6. ``uptakeInsideCellAtCOM(cell, max_amount: float, relative_uptake: float) -> bool`` – uptake at
the center of mass of the cell

Tracking Total Amount Secreted or Uptaken
---------------------------------------------------

The below methods can be used to get a FieldSecretorResult object, which will have a property called ``tot_amount`` 
that contains the summary of the secretion/uptake operation.
Just add "TotalCount" to the name of the same method you used above.
The arguments remain the same.

1. ``secreteInsideCellTotalCount(...)``

2. ``secreteInsideCellConstantConcentrationTotalCount(...)``

3. ``secreteInsideCellAtBoundaryTotalCount(...)``

4. ``secreteInsideCellAtBoundaryOnContactWithTotalCount(...)``

5. ``secreteOutsideCellAtBoundaryTotalCount(...)``

6. ``secreteOutsideCellAtBoundaryOnContactWithTotalCount(...)``

7. ``secreteInsideCellAtCOMTotalCount(...)``

and similarly for uptake:

1. ``uptakeInsideCellTotalCount(...)``

2. ``uptakeInsideCellAtBoundaryTotalCount(...)``

3. ``uptakeInsideCellAtBoundaryOnContactWithTotalCount(...)``

4. ``uptakeOutsideCellAtBoundaryTotalCount(...)``

5. ``uptakeOutsideCellAtBoundaryOnContactWithTotalCount(...)``

6. ``uptakeInsideCellAtCOMTotalCount(...)``