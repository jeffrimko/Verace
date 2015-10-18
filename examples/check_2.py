import env
from verace import VerChecker, VerInfo

def check_ver(path):
    for num,line in enumerate(open(path).readlines()):
        if line.find("version") > -1:
            ver = line.split("=")[1]
            ver = ver.split('"')[1].split('"')[0]
            return [VerInfo(path, num+1, ver)]

v1 = VerChecker("Example 2", __file__)
v1.include("file_1.txt", match="onemore", delim=":")
v1.include("file_2.txt", check_ver)
v1.run()
