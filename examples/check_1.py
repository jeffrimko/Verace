import sys
sys.path.insert(0, "..\lib")
from verace import VerChecker, VerInfo

v1 = VerChecker("Example 1", __file__)
v1.include("file.txt", opts={'match':"version", 'delim':"="})
v1.include("file.txt", opts={'match':"another", 'delim':"="})
v1.include("file.txt", opts={'match':"onemore", 'delim':":"})
v1.run()

v2 = VerChecker("Example 2", __file__)
v2.include("file.txt", opts={'match':"version", 'delim':"="})
v2.include("file.txt", opts={'match':"another", 'delim':"="})
v2.include("file.txt", opts={'match':"diffver", 'delim':"= v"})
v2.run()
