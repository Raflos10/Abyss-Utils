import sys, io

class Sb7Header:
    def __init__(self, data):
        stream = io.BytesIO(data)
        self.magic = stream.read(4)
        assert self.magic == b'SB7 ', "This does not appear to be a SB7 file."

        self.date = stream.read(28)
        self.unknownPointer0 = int.from_bytes(stream.read(4), "little")
        self.textTable2 = int.from_bytes(stream.read(4), "little")

        # Info Code Block
        self.icbCount = int.from_bytes(stream.read(4), "little")
        self.icbSize = int.from_bytes(stream.read(4), "little")
        self.icbPointer = int.from_bytes(stream.read(4), "little")

        # Unknown section
        self.unknownPointer1 = int.from_bytes(stream.read(4), "little")

        # Text Table
        self.ttCount = int.from_bytes(stream.read(4), "little")
        self.ttSize = int.from_bytes(stream.read(4), "little")
        self.ttPointer = int.from_bytes(stream.read(4), "little")

        # Instructions
        self.iSize = int.from_bytes(stream.read(4), "little")
        self.iPointer = int.from_bytes(stream.read(4), "little")

        # Text
        self.tSize = int.from_bytes(stream.read(4), "little")
        self.tPointer = int.from_bytes(stream.read(4), "little")

        # Unknown
        self.unknownPointer2 = int.from_bytes(stream.read(4), "little")
        self.unknownPointer3 = int.from_bytes(stream.read(4), "little")


    def printInfo(self):
        print(f"Date: {self.date}")
        print(f"Text Table 2: {self.textTable2}")
        print(f"Info Code Block: Count: {self.icbCount}, Size: {self.icbSize}, Pointer: {self.icbPointer}")
        print(f"Text Table: Count: {self.ttCount}, Size: {self.ttSize}, Pointer: {self.ttPointer}")
        print(f"Instructions: Size: {self.iSize}, Pointer: {self.iPointer}")
        print(f"Text: Size: {self.tSize}, Pointer: {self.tPointer}")

class Sb7:
    def __init__(self, data):
        stream = io.BytesIO(data)
        self.header = Sb7Header(stream.read(92))
        self.textSets = []

        stream.seek(self.header.ttPointer)
        # this is a list of pointers to the start of each set of line pointers
        textSetPointers = []

        for i in range(self.header.ttCount):
            textSetPointers.append(int.from_bytes(stream.read(4), "little"))
        # add the size as the final pointer
        textSetPointers.append(self.header.ttSize)

        # this is a list of pointers to the start of each actual line of text
        linePointers = []
        # how many lines per set of text
        lineCounts = []

        # for each text set, get the line pointers
        for i in range(self.header.ttCount):
            # start position of this text set
            textPointersStart = textSetPointers[i]
            stream.seek(self.header.ttPointer + textPointersStart)

            # line count is determined by how many pointers (4 bytes each) are in each set of text set pointers
            lineCounts.append(int((textSetPointers[i+1] - textPointersStart) / 4))

            for j in range(lineCounts[i]):
                linePointers.append(int.from_bytes(stream.read(4), "little"))

            # for the last line of the last set, add the size as the final pointer
            if i == self.header.ttCount - 1:
                linePointers.append(self.header.tSize)

        nextLinePointer = 0
        # finally get the actual lines of text from the pointers
        for lineCount in lineCounts:
            lines = []
            for i in range(lineCount):
                stream.seek(self.header.tPointer + linePointers[nextLinePointer])
                lineSize = linePointers[nextLinePointer+1] - linePointers[nextLinePointer]
                lines.append(stream.read(lineSize))
                nextLinePointer += 1
            self.textSets.append(lines)


    def printInfo(self):
        self.header.printInfo()

    def printTexts(self):
        print("Text:")
        for textSet in self.textSets:
            for line in textSet:
                print(line)


def getFileBytes(fileName):
    with open(fileName, "rb") as f:
        return f.read(-1)

def writeFileBytes(fileName, data):
    with open(fileName, "wb") as f:
        f.write(data)

def printInfo(fileName):
    data = getFileBytes(fileName)
    sb7File = Sb7(data)
    # sb7File.printInfo()
    sb7File.printTexts()
