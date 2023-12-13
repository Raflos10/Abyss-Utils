import io
from classes.iso import Iso

class Cvm:
    def __init__(self, data):
        stream = io.BytesIO(data)
        self.magic = stream.read(4)
        assert self.magic == b'CVMH', "This does not appear to be a CVM file."

        self.unknown = stream.read(6140)
        self.iso = Iso(stream.read())
