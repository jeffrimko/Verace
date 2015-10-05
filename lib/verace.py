"""Library for checking version strings in files."""

##==============================================================#
## DEVELOPED 2015, REVISED 2015, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os.path as op
from collections import namedtuple

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.2.0-alpha"

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
            self.root = op.dirname(root)
        self.root = op.abspath(self.root)
        self._vinfos = []
        self._checks = []
        self._string = None
    def string(self):
        """Returns the version string if `run()` found no inconsistencies,
        otherwise None is returned."""
        return self._string
    def include(self, path, func=None, opts={}, **kwargs):
        """Includes a file to check.

        **Params**:
          - path (str) - Path to a file to check.
          - func (function) - Function that performs check will be passed
            `path` and `opts`. Must return a list of VerInfo items.
          - opts (dict) - Options to pass to the check function. Any additional
            key word args will be included.
        """
        opts.update(kwargs)
        if not func:
            func = check_basic
        self._checks.append((path, func, opts))
    def run(self, verbose=True):
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
            self._vinfos.extend(c[1](path, c[2]))
        for vinfo in self._vinfos:
            vprint("  `%s` (%s:%u)" % (
                    vinfo.string,
                    op.relpath(vinfo.path),
                    vinfo.linenum))
        strings = set([v.string for v in self._vinfos])
        self._string = list(strings)[0] if 1 == len(strings) else None
        if not self._string:
            vprint("  [!] WARNING: Version numbers differ!")
        return self._string

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

def check_basic(path, opts):
    """Basic version check function."""
    for num,line in enumerate(open(path).readlines()):
        if line.find(opts['match']) > -1:
            ver = line.split(opts['delim'])[1].strip()
            if 'delim2' in opts.keys():
                ver = ver.split(opts['delim2'])[0].strip()
            return [VerInfo(path, num+1, ver)]

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    pass
