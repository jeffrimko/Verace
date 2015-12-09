"""Library for checking version strings in files."""

##==============================================================#
## DEVELOPED 2015, REVISED 2015, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import copy
import os
import os.path as op
from collections import namedtuple

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.2.5"

#: Contains version information for a single checked item.
VerInfo = namedtuple("VerInfo", "path linenum string")

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class VerChecker(object):
    def __init__(self, name, root):
        """Initializes the version checker object.

        **Params**:
          - name (str) - Name associated with items checked.
          - root (str) - Root path used to resolve relative paths for checked
            files. Can be a file or directory."""
        self.name = name
        if op.isfile(root):
            root = op.dirname(root)
        self.root = op.abspath(root)
        self._vinfos = []
        self._checks = []
        self._string = None
    def string(self):
        """Returns the version string if `run()` found no inconsistencies,
        otherwise None is returned."""
        return self._string
    def include(self, path, func=None, opts=None, **kwargs):
        """Includes a file to check.

        **Params**:
          - path (str) - Path to a file to check.
          - func (function) - Function that performs check will be passed
            `path` and `opts`. Must return a list of VerInfo items.
          - opts (dict) - Options to pass to the check function. Any additional
            key word args will be included.
        """
        if not opts:
            opts = {}
        opts.update(copy.deepcopy(kwargs))
        if not func:
            func = check_basic
        c = (path, func, copy.deepcopy(opts))
        self._checks.append(c)
    def run(self, verbose=True, debug=False):
        """Runs checks on all included items, reports any inconsistencies."""
        vprint = get_vprint(verbose)
        self._vinfos = []
        vprint("%s Version Information:" % (self.name))
        # Execute checks and update version information list.
        for c in self._checks:
            path = c[0]
            if not op.isabs(path):
                path = op.join(self.root, path)
            path = op.normpath(path)
            self._vinfos.extend(c[1](path, **c[2]))
        for vinfo in self._vinfos:
            vprint("  `%s` (%s:%u)" % (
                    vinfo.string,
                    op.relpath(vinfo.path),
                    vinfo.linenum))
        strings = set([v.string for v in self._vinfos])
        if strings:
            self._string = list(strings)[0] if 1 == len(strings) else None
            if not self._string:
                vprint("  [!] WARNING: Version info differs!")
        else:
            self._string = None
            vprint("  [!] WARNING: No version info found!")
        return self._string
    def update(self, newver):
        """Updates all associated version strings to the given new string. Use
        caution as this will modify file content!"""
        self.run(verbose=False)
        for vi in self._vinfos:
            with open(vi.path) as fi:
                temp = op.join(
                        op.dirname(vi.path),
                        "__temp-verace-" + op.basename(vi.path))
                with open(temp, "w") as fo:
                    for num,line in enumerate(fi.readlines(), 1):
                        if num == vi.linenum:
                            line = line.replace(vi.string, newver)
                        fo.write(line)
            os.remove(vi.path)
            os.rename(temp, vi.path)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def get_vprint(verbose):
    """Helper function for optional verbose printing."""
    def _vprint(msg, endl=True):
        if endl:
            print msg
        else:
            print msg,
    def _nprint(msg, endl=True):
        pass
    if verbose:
        return _vprint
    return _nprint

def check_basic(path, match="version", delim="=", delim2=""):
    """Basic version check function."""
    for num,line in enumerate(open(path).readlines()):
        if line.find(match) > -1:
            ver = line.split(delim)[1].strip()
            if delim2:
                ver = ver.split(delim2)[0].strip()
            return [VerInfo(path, num+1, ver)]

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
