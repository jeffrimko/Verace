"""Library for checking strings in files."""

##==============================================================#
## DEVELOPED 2015, REVISED 2017, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from __future__ import print_function

import copy
import inspect
import os
import os.path as op
from collections import namedtuple

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Library version string.
__version__ = "0.4.1"

#: Contains information for a single checked item.
VerInfo = namedtuple("VerInfo", "path linenum string")

#: Defines a file check.
VerCheck = namedtuple("VerCheck", "path func opts updatable")

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
        self._string = None
        self._checks = []
        self._vinfos = []
        self.debug = False
    def _run_check(self, c):
        """Runs a single VerCheck and returns a list of (VerInfo,updatable)
        tuples."""
        dprint = get_vprint(self.debug)
        # Setup file path.
        path = c.path
        if not op.isabs(path):
            path = op.join(self.root, path)
        path = op.normpath(path)
        # Setup function and function type.
        if type(c.func) in [list, tuple]: func,ftyp = c.func
        else: func,ftyp = (c.func, "file")
        if (not func) or (not hasattr(func, "__call__")):
            func = check_basic
        # Run the function over the file and collect VerInfo objects.
        vinfos = []
        if "file" == ftyp:
            v = func(path, **c.opts)
            dprint((inspect.stack()[0][3], c, v))
            if list != type(v): v = [v]
            vinfos += v
        elif "line" == ftyp:
            for num,line in readlines(path):
                string = func(line, **c.opts)
                if string:
                    vinfos.append(VerInfo(path, num, string))
        self._vinfos += vinfos
        return [(v, c.updatable) for v in vinfos if v]
    def _iter_vinfo(self, get_updatable=False):
        """Iterates over the associated VerInfo objects. Optionally returns if
        the associated file is updatable."""
        vulist = [] # Holds (VerInfo,updatable) items.
        self._vinfos = []
        for c in self._checks:
            vulist += self._run_check(c)
        for vu in sorted(vulist, key=lambda i: (i[0].path, i[0].linenum)):
            if vu:
                yield vu if get_updatable else vu[0]
    def string(self):
        """Returns the string if `run()` found no inconsistencies,
        otherwise None is returned. Always calls `run()`."""
        self.run(False)
        return self._string
    def include(self, path, func=None, opts=None, updatable=True, **kwargs):
        """Includes a file to check.

        **Params**:
          - path (str) - Path to a file to check.
          - func (function|(tuple,str)) - Either a (func,type) tuple or a
            function (type defaults to 'file'). Valid type values are
            'file|line'. The type controls whether the file path or individual
            lines will be passed to the function. A file function may return
            either single VerInfo or a list of VerInfos. A line function may
            return a string.
          - opts (dict) - Options to pass to the check function. Any additional
            keyword args will be included.
          - updatable (bool) - If true, string can be updated using `update()`.
        """
        if not opts:
            opts = {}
        opts.update(copy.deepcopy(kwargs))
        c = VerCheck(path, func, copy.deepcopy(opts), updatable)
        self._checks.append(c)
    def run(self, verbose=True):
        """Runs checks on all included items, reports any inconsistencies.
        Returns string if consistent else None."""
        vprint = get_vprint(verbose)
        strings = []
        vprint(self.name + ":")
        for vinfo in self._iter_vinfo():
            if vinfo.string not in strings:
                strings.append(vinfo.string)
            vprint("  `%s` (%s:%u)" % (
                    vinfo.string,
                    op.relpath(vinfo.path),
                    vinfo.linenum))
        if strings:
            self._string = list(strings)[0] if 1 == len(strings) else None
            if not self._string:
                vprint("[WARNING] Strings differ!")
        else:
            self._string = None
            vprint("[WARNING] No string info found!")
        return self._string
    def update(self, newstr):
        """Updates all associated strings to the given new string. Use
        caution as this will modify file content! Returns number of strings
        updated."""
        updated = 0
        for vinfo,updatable in self._iter_vinfo(get_updatable=True):
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
        try:
            import qprompt
        except:
            print("The `qprompt` library is needed for this functionality!")
            return
        self.run()
        if not self._checks:
            qprompt.pause()
            return
        ns = len(self._vinfos)
        nu = len({v.string for v in self._vinfos})
        nf = len({v.path for v in self._vinfos})
        ss = "string" + ("s" if ns != 1 else "")
        sf = "file" + ("s" if nf != 1 else "")
        msg = "Found %u %s (%u unique) in %u %s." % (
                ns, ss, nu, nf, sf)
        qprompt.alert(msg)
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

def readlines(fpath):
    """Generator that reads the file at the given path line by line yielding
    (number,text) for each."""
    with open(fpath) as fi:
        for num,line in enumerate(fi.readlines(), 1):
            yield num,line

def check_basic(path, match="version", splits=None, single=True):
    """Basic check function. Iterates through files lines until the `match`
    string is found. The matching line will be split using the list of
    (characters,index) tuples/lists from `splits`. Can either return a single
    (first) result or all results in the file. **NOTE**: `splits` must be a
    list of tuples/lists!"""
    splits = splits or []
    vinfos = []
    for num,line in readlines(path):
        if line.find(match) > -1:
            vstr = line
            for char,indx in splits:
                vstr = vstr.split(char)[indx].strip()
            vinfos.append(VerInfo(path, num, vstr))
    if single and len(vinfos) > 1:
        return vinfos[0]
    return vinfos

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    mychk = VerChecker("My Checker", __file__)
    mychk.include(r"setup.py", match="version = ", splits=[('"', 1)])
    mychk.prompt()
