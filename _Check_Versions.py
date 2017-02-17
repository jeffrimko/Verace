##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from verace import VerChecker

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

VERCHK = VerChecker("Verace Version String", __file__)
VERCHK.include(r"lib\setup.py", match="version = ", delim='"')
VERCHK.include(r"lib\verace.py", match="__version__ = ", delim='"')
VERCHK.include(r"README.adoc", match="# version found", delim=" = ")
VERCHK.include(r"CHANGELOG.adoc", match="verace-", delim="-", delim2=" ", updatable=False)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    VERCHK.prompt()
