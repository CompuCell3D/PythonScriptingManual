.. foldable table of content can be implemented by making sure that the headers
   follow proper hierarchy  - see http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html
    and making sure that the document that is at the "top of" of toc has subdocs listed as in this exa  mple

Steppable Section
=================

Steppables are CompuCell modules that are called every Monte Carlo Step
(MCS). More precisely, they are called after all the pixel copy attempts
in a given MCS have been carried out. Steppables may have various
functions - for example solving PDEs, checking if critical
concentration threshold have been reached, updating target volume or
target surface given the concentration of come growth factor,
initializing cell field, writing numerical results to a file, *etc...* In
general, steppables perform all functions that need to be done every
MCS. In the reminder of this section we will present steppables
currently available in the CompuCell3D and describe their usage.

.. tip::

    It is most convenient to implement Steppables in Python. However, in certain situations
    where code performance is an issue users can implement steppables in C++

This section "off-the-shelf" steppables that are available in CC3D and were implemented using C++

* :doc:`uniform_initializer`
* :doc:`blob_initializer`
* :doc:`pif_initializer`
* :doc:`pif_dumper`
* :doc:`mitosis`
* :doc:`box_watcher`
* :doc:`mu-parser`

.. include:: uniform_initializer.rst
.. include:: blob_initializer.rst
.. include:: pif_initializer.rst
.. include:: pif_dumper.rst
.. include:: mitosis.rst
.. include:: box_watcher.rst
.. include:: mu_parser.rst