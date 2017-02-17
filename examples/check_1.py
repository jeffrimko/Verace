import env
from verace import VerChecker, VerInfo

v1 = VerChecker("Example 1a", __file__)
v1.include("file_1.txt")
v1.include("file_1.txt", match="another")
v1.include("file_1.txt", match="onemore", splits=[(":",0)])
v1.run()

v2 = VerChecker("Example 1b", __file__)
v2.include("file_1.txt")
v2.include("file_1.txt", match="another")
v2.include("file_1.txt", match="diffver", splits=[("= v",0)])
v2.run()
