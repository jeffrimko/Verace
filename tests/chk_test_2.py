"""Tests the basic usage of VerChecker."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from testlib import *

from verace import VerChecker

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

FILETMPL = "# some text\n## foo-bar-{VERSION}\nmore text here\n"
FILENAME = get_main_name(prefix="__temp-", ext=".txt")
VCHKNAME = get_main_name().upper()
VERSION = "1.2.3"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCase(unittest.TestCase):

    def setUp(test):
        with open(FILENAME, "w") as fo:
            fo.write(FILETMPL.format(**globals()))
        test.verchk = VerChecker(VCHKNAME, __file__)
        test.verchk.include(FILENAME, match="foo-bar-", splits=[("-", 2)])

    def test_correct_string(test):
        test.assertEqual(test.verchk.string(), VERSION)

    def test_output_format(test):
        expect = "{VCHKNAME}:\n  `{VERSION}` ({FILENAME}:2)".format(**globals())
        sys.stdout = StringIO()
        test.assertEqual(test.verchk.run(), VERSION)
        test.assertEqual(sys.stdout.getvalue().strip(), expect)

    def tearDown(test):
        remove(FILENAME)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
