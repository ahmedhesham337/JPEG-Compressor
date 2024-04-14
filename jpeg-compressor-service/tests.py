from compression import COMPRESSION_ALGORITHMS
import JPEG

import cv2
import numpy as np
import os 
from json import JSONEncoder, dumps, loads

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def main():

    encoder = JPEG.JPEGEncoder(
        "./test_data/ritchie.png",
        8,
        5,
        COMPRESSION_ALGORITHMS.ZIP,
        True,
        True
    )

    encoder.compress()
    stats = encoder.get_stats()
    print(stats)
    x = dumps(stats, cls=NumpyArrayEncoder)
    print(x)
    d = loads(x)
    ff = np.asarray(d["quantization_matrix"])
    print(ff)
    

    compressed = encoder.get_compressed_image()
    with open("./compressed.dat", "wb") as f:
        f.write(compressed)
    

    decoder = JPEG.JPEGDecoder(
        compressed,
        stats["block_size"],
        stats["quantization_matrix"],
        stats["trans_shape"],
        stats["compression"],
        stats["color_downsampled"]
    )

    decoder.decompress()

    decompressed = decoder.get_decompressed_image()
    cv2.imwrite("./aaaa.jpeg", decompressed.astype(np.uint8))

    sz1 = os.path.getsize("./test_data/ritchie.png")
    sz2 = os.path.getsize("./aaaa.jpeg")

    print("{} {}".format(sz1, sz2))
    rat = (1 - (sz2 / sz1)) * 100  
    print(round(rat,2))

    """
    image = cv2.imread("./test_data/lenna.png")
    ycr = colorspace.rgb2ycbcr(image)
    quantization_scale = 5
    block_size = 8
    #quantization_matrix = quantization.get_default_quantization_matrix(block_size, block_size) 
    quantization_matrix = quantization.get_quantization_matrix(quantization_scale, block_size, block_size)

    imenc = dct.forward_dct(ycr, block_size, block_size)
    imencq = quantization.quantize(imenc, quantization_matrix)
    encz = compression.compress_zip(imencq)
    print(imencq.shape)
    decz = compression.decompress_zip(encz, imencq.shape)
    decq = quantization.dec_quantize(decz, quantization_matrix)
    dec = dct.inverse_dct(decq, block_size, block_size)
    img_bgr = colorspace.ycbcr2rgb(dec)

    cv2.imwrite("./compressed_test.jpeg", img_bgr.astype(np.uint8))
"""

if __name__ == "__main__":
    main()