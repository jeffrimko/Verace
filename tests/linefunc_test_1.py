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
        def getver(line):
            if "version =" in line:
                return line.split('"')[1]
        test.verchk.include("checkfiles/multi.txt", func=(getver, "line"))
        test.assertEqual(test.verchk.string(), "1.2.3")

    def test_different(test):
        def getdiff(line):
            if "different =" in line:
                return line.split('"')[1].split(",")[0]
        test.verchk.include("checkfiles/multi.txt", func=(getdiff, "line"))
        test.assertEqual(test.verchk.string(), "0.0.0")

    def test_none(test):
        def getnone(line):
            return
        test.verchk.include("checkfiles/multi.txt", func=(getnone, "line"))
        test.assertEqual(test.verchk.string(), None)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
