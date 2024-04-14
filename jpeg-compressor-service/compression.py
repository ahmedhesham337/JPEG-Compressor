import zlib
import numpy as np
from enum import Enum

def compress_zip(mtx):
    return zlib.compress(mtx.astype(np.int8).tobytes())

def decompress_zip(mtx, shape):
    return np.frombuffer(zlib.decompress(mtx), dtype=np.int8).astype(float).reshape(shape)

class COMPRESSION_ALGORITHMS(Enum):
    ZIP = 0
    RLE = 1

