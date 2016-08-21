"""Library for checking version strings in files."""

##==============================================================#
## DEVELOPED 2015, REVISED 2016, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from __future__ import print_function

import copy
import os
import os.path as op
from collections import namedtuple

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.3.0-alpha"

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
    def include(self, path, func=None, opts=None, updatable=True, **kwargs):
        """Includes a file to check.

        **Params**:
          - path (str) - Path to a file to check.
          - func (function) - Function that performs check will be passed
            `path` and `opts`. Must return a list of VerInfo items.
          - opts (dict) - Options to pass to the check function. Any additional
            key word args will be included.
          - updatable (bool) - If true, string can be updated using `update()`.
        """
        if not opts:
            opts = {}
        opts.update(copy.deepcopy(kwargs))
        if not func:
            func = check_basic
        c = (path, func, copy.deepcopy(opts), updatable)
        self._checks.append(c)
    def iter_vinfo(self, get_updatable=False):
        """Iterates over the associated VerInfo objects. Optionally returns if
        the associated file is updatable."""
        for c in self._checks:
            path = c[0]
            if not op.isabs(path):
                path = op.join(self.root, path)
            path = op.normpath(path)
            vinfos = c[1](path, **c[2])
            if list != type(vinfos):
                vinfos = [vinfos]
            for vi in vinfos:
                yield (vi, c[3]) if get_updatable else vi
    def run(self, verbose=True):
        """Runs checks on all included items, reports any inconsistencies.
        Returns version string if consistent else None."""
        vprint = get_vprint(verbose)
        strings = []
        vprint("%s Version Information:" % (self.name))
        for vinfo in self.iter_vinfo():
            if vinfo.string not in strings:
                strings.append(vinfo.string)
            vprint("  `%s` (%s:%u)" % (
                    vinfo.string,
                    op.relpath(vinfo.path),
                    vinfo.linenum))
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
        caution as this will modify file content! Returns number of strings
        updated."""
        updated = 0
        for vinfo,updatable in self.iter_vinfo(get_updatable=True):
            if not updatable:
                continue
            with open(vinfo.path) as fi:
                temp = op.join(
                        op.dirname(vinfo.path),
                        "__temp-verace-" + op.basename(vinfo.path))
                with open(temp, "w") as fo:
                    for num,line in enumerate(fi.readlines(), 1):
                        if num == vinfo.linenum:
                            line = line.replace(vinfo.string, newver)
                        fo.write(line)
            os.remove(vinfo.path)
            os.rename(temp, vinfo.path)
            updated += 1
        return updated

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def get_vprint(verbose):
    """Helper function for optional verbose printing."""
    def _vprint(msg, end=None):
        if None != end:
            print(msg, end=end)
        else:
            print(msg)
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
            return VerInfo(path, num+1, ver)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    vprint = get_vprint(True)
    vprint("hello", end=" ")
    vprint("hello")
