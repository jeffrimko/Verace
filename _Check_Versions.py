##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from verace import VerChecker, VerInfo, show_prompt

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

VERCHK = VerChecker("Verace", __file__)
VERCHK.include(r"lib\setup.py", opts={'match':"version = ", 'delim':'"'})
VERCHK.include(r"lib\verace.py", match="__version__ = ", delim='"')
VERCHK.include(r"CHANGELOG.adoc", match="verace-", delim="-", delim2=" ", updatable=False)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    show_prompt(VERCHK)
