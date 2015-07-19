from verace import VerChecker, VerInfo

class TestChecker(VerChecker):
    NAME = "Test"
    def check_version(self):
        path = r"file.txt"
        for num,line in enumerate(open(path).readlines()):
            if line.find("version") > -1:
                return [VerInfo(path, num+1, line.split('=')[1].strip())]
    def check_another(self):
        path = r"file.txt"
        for num,line in enumerate(open(path).readlines()):
            if line.find("another") > -1:
                return [VerInfo(path, num+1, line.split('=')[1].strip())]

if __name__ == '__main__':
    TestChecker().show()
    print "The version is `%s`." % (TestChecker().string())
    raw_input("Press ENTER to continue...")
