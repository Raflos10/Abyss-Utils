import io, os

def getDualIntValue(littleEndianBytes, bigEndianBytes):
    littleEndianInt = int.from_bytes(littleEndianBytes, "little")
    bigEndianInt = int.from_bytes(bigEndianBytes, "big")
    assert littleEndianInt == bigEndianInt, "Little-endian did not match big-endian"
    return littleEndianInt

class PrimaryVolumeDescriptor:
    def __init__(self, data):
        stream = io.BytesIO(data)

        self.type_ = stream.read(1)
        assert self.type_ == b'\x01', "Non-type-1 Volume Descriptor found."

        self.magic = stream.read(5)
        self.version = stream.read(1)
        stream.seek(80)
        self.volumeSpaceSize = getDualIntValue(stream.read(4), stream.read(4))
        stream.seek(120)
        self.volumeSetSize = getDualIntValue(stream.read(2), stream.read(2))
        self.volumeSequenceNumber = getDualIntValue(stream.read(2), stream.read(2))
        self.logicalBlockSize = getDualIntValue(stream.read(2), stream.read(2))
        self.pathTableSize = getDualIntValue(stream.read(4), stream.read(4))
        self.typeLPathTableLocation = int.from_bytes(stream.read(4), "little")
        self.typeLOptionalPathTableLocation = int.from_bytes(stream.read(4), "little")
        self.typeMPathTableLocation = int.from_bytes(stream.read(4), "big")
        self.typeMOptionalPathTableLocation = int.from_bytes(stream.read(4), "big")

class Iso:
    def __init__(self, data):
        stream = io.BytesIO(data)
        # skip the system data
        stream.seek(32_768)

        # get the volume descriptor
        self.primaryVolumeDescriptor = PrimaryVolumeDescriptor(stream.read(2048))
        assert self.primaryVolumeDescriptor.magic == b'CD001', "This does not appear to be an ISO file."
