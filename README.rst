========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |version| image:: https://img.shields.io/pypi/v/fseq.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/fseq

.. |commits-since| image:: https://img.shields.io/github/commits-since/federicobond/python-fseq/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/federicobond/python-fseq/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/fseq.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/fseq

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/fseq.svg
    :alt: Supported versions
    :target: https://pypi.org/project/fseq

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/fseq.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/fseq


.. end-badges

A fseq sequence file parser.

* Free software: MIT license

Installation
============

::

    pip install fseq

Documentation
=============


To use the project:

.. code-block:: python

    import fseq
    fseq.longest()


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
