.. Verace documentation master file, created by
   sphinx-quickstart on Thu Feb 16 20:43:30 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Verace
======

This is the main documentation for Verace (`GitHub <https://github.com/jeffrimko/Verace>`_, `PyPI <https://pypi.python.org/pypi/verace>`_), a Python library to aid checking strings in files.

VerChecker
----------
This class is used to create objects that will check/update strings in files:

.. autoclass:: verace.VerChecker
    :members:


Custom Check Functions
----------------------
A function can be provided to ``VerChecker.include()``. If no explicit function is provide, the following function will be used:

.. autofunction:: verace.check_basic

Custom functions can be defined to find strings. The first argument must be the file path and the function must return either a single ``VerInfo`` object or a list of ``VerInfo`` objects:

.. autodata:: verace.VerInfo

Use this convenience function to iterate through the lines in a given file:

.. autofunction:: verace.readlines
