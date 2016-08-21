"""Tests the basic usage of VerChecker."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from verace import VerChecker

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

TESTFILE = get_main_name(prefix="__temp-", ext=".txt")
VCHKNAME = get_main_name().upper()
VERSION = "1.0.0"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(test):
        with open(TESTFILE, "w") as fo:
            fo.write("version = {VERSION}\nmore text here\n".format(**globals()))
        test.verchk = VerChecker(VCHKNAME, __file__)
        # Not a function so should be ignored.
        not_a_func = True
        test.verchk.include(TESTFILE, func=not_a_func)

    def test_chk_1(test):
        test.assertEqual(test.verchk.string(), VERSION)

    def test_chk_2(test):
        expect = "{VCHKNAME} Version Information:\n  `{VERSION}` ({TESTFILE}:1)".format(**globals())
        sys.stdout = StringIO()
        test.assertEqual(test.verchk.run(), VERSION)
        test.assertEqual(sys.stdout.getvalue().strip(), expect)

    def tearDown(test):
        remove(TESTFILE)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
