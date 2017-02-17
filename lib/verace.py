"""Library for checking strings in files."""

##==============================================================#
## DEVELOPED 2015, REVISED 2017, Jeff Rimko.                    #
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
__version__ = "0.3.0-alpha2"

#: Contains information for a single checked item.
VerInfo = namedtuple("VerInfo", "path linenum string")

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class VerChecker(object):
    def __init__(self, name, root):
        """Initializes the checker object.

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
        """Returns the string if `run()` found no inconsistencies,
        otherwise None is returned. Always calls `run()`."""
        self.run(False)
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
        if (not func) or (not hasattr(func, "__call__")):
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
        Returns string if consistent else None."""
        vprint = get_vprint(verbose)
        strings = []
        vprint(self.name + ":")
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
                vprint("  [WARNING] Strings differ!")
        else:
            self._string = None
            vprint("  [WARNING] No string info found!")
        return self._string
    def update(self, newstr):
        """Updates all associated strings to the given new string. Use
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
                            line = line.replace(vinfo.string, newstr)
                        fo.write(line)
            os.remove(vinfo.path)
            os.rename(temp, vinfo.path)
            updated += 1
        return updated
    def prompt(self):
        """Shows the standard prompt for handling checked strings."""
        import qprompt
        self.run()
        if qprompt.ask_yesno("Update string?", dft="n"):
            newstr = qprompt.ask_str("New string")
            if newstr:
                self.update(newstr)
                self.prompt()

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

def check_basic(path, match="version", delim="=", delim2="", splitnum=1, splitnum2=0):
    """Basic check function."""
    for num,line in enumerate(open(path).readlines(), 1):
        if line.find(match) > -1:
            vstr = line.split(delim)[splitnum].strip()
            if delim2:
                vstr = vstr.split(delim2)[splitnum2].strip()
            return VerInfo(path, num, vstr)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    mychk = VerChecker("My Checker", __file__)
    mychk.include(r"setup.py", match="version = ", delim='"')
    mychk.prompt()
