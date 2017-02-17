##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

from verace import VerChecker

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

VERCHK = VerChecker("Verace Version String", __file__)
VERCHK.include(r"lib\setup.py", match="version = ", splits=[('"',1)])
VERCHK.include(r"lib\verace.py", match="__version__ = ", splits=[('"',1)])
VERCHK.include(r"README.adoc", match="# version found", splits=[(" = ",1)])
VERCHK.include(r"CHANGELOG.adoc", match="verace-", splits=[("-",1),(" ",0)], updatable=False)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    VERCHK.prompt()
