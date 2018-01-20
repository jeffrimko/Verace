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
A function can be provided to ``VerChecker.include()``. The function will be used to parse the file for the target string.

If a tuple/list is provided as as the ``func`` argument, the first value must be a function and the second value must be the string ``'file'`` (default) or ``'line'``.

If no explicit function is provide, the following file function will be used:

.. autofunction:: verace.check_basic

File Functions
~~~~~~~~~~~~~~
File functions must handle the string search through the entire target file. The first argument must be the file path and the function must return either a single ``VerInfo`` object or a list of ``VerInfo`` objects:

.. autodata:: verace.VerInfo

Use this convenience function to iterate through the lines in a given file:

.. autofunction:: verace.readlines

Line Functions
~~~~~~~~~~~~~~
Line functions will be provided each line from the file one at a time. If the target string is found, simply return it. Otherwise return None (default return).
