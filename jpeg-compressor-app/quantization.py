import numpy as np

def get_quantization_matrix(quantization_scale, block_size_x, block_size_y):
    Q = \
    (np.ones((block_size_x, block_size_y)) * (quantization_scale * quantization_scale)) \
    .clip(-100, 100) \
    .reshape((1, block_size_x, 1, block_size_y, 1))
    return Q

def get_default_quantization_matrix(block_size_x = 8, block_size_y = 8):
    block_size_x = 8
    block_size_y = 8
    Q = np.array(
        [[16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 48, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]]
        ).reshape(1, block_size_x, 1, block_size_y, 1)
    return Q

def quantize(mtx, quantization_matrix):
    return (mtx / quantization_matrix).astype(np.int32)

def dec_quantize(mtx, quantization_matrix):
    return (mtx * quantization_matrix).astype(float)