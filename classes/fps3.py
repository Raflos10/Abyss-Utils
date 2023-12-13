import sys, io

class Fps3EntryFile:
    def __init__(self, data):
        stream = io.BytesIO(data)
        self.start = int.from_bytes(stream.read(4), "little")
        self.size = int.from_bytes(stream.read(4), "little")
        self.name = stream.read(32)

class Fps3:
    def __init__(self, data):
        stream = io.BytesIO(data)
        self.magic = stream.read(4)
        assert self.magic == b'FPS3', "This does not appear to be an FPS3 archive file."

        self.count = int.from_bytes(stream.read(4), "little")
        self.starte = int.from_bytes(stream.read(4), "little")
        self.startd = int.from_bytes(stream.read(4), "little")
        self.unknown1 = int.from_bytes(stream.read(4), "little")
        self.unknown2 = int.from_bytes(stream.read(4), "little")
        self.unknown3 = int.from_bytes(stream.read(4), "little")

        self.files = {}
        for i in range(self.count):
            entry = Fps3EntryFile(stream.read(40))
            fileData = data[entry.start:entry.start+entry.size]
            self.files[entry.name] = fileData

    def printInfo(self):
        print("FPS3 File.")
        print(f"{self.count} files in archive.")
        for nameBytes in self.files:
            name = nameBytes.decode('utf-8')
            print(f"File: {name}, size: {len(self.files[nameBytes])}")

    def getFile(self, fileName):
        for nameBytes in self.files:
            name = nameBytes.decode('utf-8')
            if fileName in name:
                return self.files[nameBytes]
        return None
