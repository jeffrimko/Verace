
##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import inspect
from collections import namedtuple

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.1.0"

#: Contains version information for a single checked item.
VerInfo = namedtuple("VerInfo", "path linenum string")

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class VerChecker(object):
    """Base class used to check version strings in a project. Subclasses may
    contain parsing methods that begin with `check_` which return a list of
    populated VerInfo items."""
    def __init__(self, debug=False):
        self.debug=debug
        self.run()
    def run(self):
        """Runs the parse on the checked items."""
        self._vinfos = []
        for i in inspect.getmembers(self.__class__, predicate=inspect.ismethod):
            if i[0].startswith("check_"):
                if self.debug: print i
                vinfo = getattr(self, i[0])()
                if vinfo:
                    self._vinfos.extend(vinfo)
                else:
                    print "[!] No VerInfo returned by `%s()`!" % (i[0])
    def show(self):
        """Shows the version information."""
        print "%s Version Numbers:" % (self.__class__.NAME)
        for vinfo in self._vinfos:
            print "  `%s` (%s:%u)" % (vinfo.string, vinfo.path, vinfo.linenum)
        if 1 != len(set([v.string for v in self._vinfos])):
            print "  [!] WARNING: Version numbers differ!"
    def string(self):
        """If the version strings of all checked items are consistent, the
        string is returned; otherwise None is returned."""
        vers = list(set([v.string for v in self._vinfos]))
        if 1 == len(vers):
            return vers[0]
        return None

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
