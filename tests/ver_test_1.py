"""Tests the basic usage of VerChecker."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from verace import VerChecker

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(test):
        test.verchk = VerChecker("Basic Version", __file__)

    def test_version(test):
        test.verchk.include("checkfiles/multi.txt", match="version =", splits=[('"',1)])
        test.assertEqual(test.verchk.string(), "1.2.3")

    def test_another(test):
        test.verchk.include("checkfiles/multi.txt", match="another =", splits=[(' ',2)])
        test.assertEqual(test.verchk.string(), "0.1.2")

    def test_onemore(test):
        test.verchk.include("checkfiles/multi.txt", match="onemore =", splits=[('`',1)])
        test.assertEqual(test.verchk.string(), "1.1.1")

    def test_different(test):
        test.verchk.include("checkfiles/multi.txt", match="different =", splits=[('"',1),(",",0)])
        test.assertEqual(test.verchk.string(), "0.0.0")

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
