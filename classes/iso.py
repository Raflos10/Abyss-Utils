import sys, io
import pycdlib

class Iso:
    def __init__(self, data):
        self.pycd = pycdlib.PyCdlib()
        self.pycd.open_fp(io.BytesIO(data))

        self.rootFileNames = []
        for f in self.pycd.list_children(iso_path='/'):
            if f.is_file():
                self.rootFileNames.append(f.file_identifier().decode('utf-8'))

    def get_file_bytes(self, fileName):
        extractedData = io.BytesIO()
        self.pycd.get_file_from_iso_fp(extractedData, iso_path='/' + fileName)
        extractedData.seek(0)
        return extractedData.read()
