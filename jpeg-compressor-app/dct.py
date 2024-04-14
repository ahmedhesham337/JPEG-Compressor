import scipy.fftpack as fftpack
import numpy as np

def forward_dct(image, block_size_x, block_size_y):
    sh = (
        image.shape[0] // block_size_x * block_size_x,
        image.shape[1] // block_size_y * block_size_y,
        3
    )
    newmtx = image[:sh[0], :sh[1]].reshape((
        sh[0] // block_size_x,
        block_size_x,
        sh[1] // block_size_y,
        block_size_y,
        3
    ))

    return fftpack.dctn(newmtx, axes=[1,3], norm='ortho')
    

def inverse_dct(mtx, block_size_x, block_size_y):
    return fftpack.idctn(mtx, axes=[1,3], norm='ortho').reshape((
        mtx.shape[0] * block_size_x,
        mtx.shape[2] * block_size_y,
        3
    ))