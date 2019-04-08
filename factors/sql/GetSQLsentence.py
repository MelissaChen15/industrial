

class GetSQLsentence():
    def __init__(self):
        pass
    def readsql(self,filepath):
        readData = []
        for line in open(filepath, "rb").readlines():
            line = line.strip()

            if (len(line) != 0) & (b"--" not in line):  #  --开头的语句为注释
                readData.append(line)

        return readData