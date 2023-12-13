import os
from ctypes import *

this_folder = os.path.dirname(__file__)
complib = CDLL(this_folder + "/lib/complib.so")

def decode(data):
    ver = data[0]
    lcomp = int.from_bytes(data[1:5], "little")
    luncomp = int.from_bytes(data[5:9], "little")
    innerData = data[9:lcomp+9]

    inBuffer = c_buffer(innerData)
    outBuffer = c_buffer(luncomp)
    error = complib.todecode(ver, byref(inBuffer), len(innerData), byref(outBuffer), byref(c_int(luncomp)))
    if error != 0:
        print(f"Error code: {error}")
        return None

    return outBuffer.raw
