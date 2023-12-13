import sys, io
import pycdlib

class Iso:
    def __init__(self, data):
        pycd = pycdlib.PyCdlib()

        pycd._open_fp(io.BytesIO(data))
        for child in pycd.list_children(iso_path='/'):
            print(child.file_identifier())
