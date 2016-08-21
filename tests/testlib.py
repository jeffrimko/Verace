"""Provides a library to aid testing."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import __main__
import sys
import unittest
import os.path as op
from os import remove

# Handle Python 2/3 differences.
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

sys.path.append(r"..\lib")

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def get_main_name(ext="", prefix=""):
    """Returns the base name of the main script. Can optionally add an
    extension or prefix."""
    return prefix + op.splitext(op.basename(__main__.__file__))[0] + ext

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
