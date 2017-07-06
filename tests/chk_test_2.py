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
VERSION = "1.2.3"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(test):
        with open(TESTFILE, "w") as fo:
            fo.write("# some text\n## foo-bar-{VERSION}\nmore text here\n".format(**globals()))
        test.verchk = VerChecker(VCHKNAME, __file__)
        test.verchk.include(TESTFILE, match="foo-bar-", splits=[("-", 2)])

    def test_chk_1(test):
        test.assertEqual(test.verchk.string(), VERSION)

    def test_chk_2(test):
        expect = "{VCHKNAME}:\n  `{VERSION}` ({TESTFILE}:2)".format(**globals())
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
