import cv2 
import numpy as np

import colorspace
import quantization
import dct
import compression

class JPEGEncoder:

    def __init__(self,
                 fileName,
                 blockSize, 
                 quantizaionScale, 
                 compressionAlgorithm = compression.COMPRESSION_ALGORITHMS.ZIP,
                 bUseDefaultQMtx  = True,
                 bDownSampleColor = True):
        
        self.block_size          = blockSize
        self.quantization_scale  = quantizaionScale
        self.image_file_name     = fileName

        self.bDownSampleColor    = bDownSampleColor
        self.bUseDefaultQMtx     = bUseDefaultQMtx
        self.bCompressed         = False

        self.compression_alg     = compressionAlgorithm
        self.trans_shape         = None
        self.quantization_matrix = None

        self.image_data          = cv2.imread(self.image_file_name)
        self.compressed_image    = None

    def compress(self):
        tmp_image_data = self.image_data.copy()

        if (self.bDownSampleColor):
            tmp_image_data = colorspace.rgb2ycbcr(tmp_image_data)
        
        if (self.bUseDefaultQMtx):
            self.block_size = 8
            self.quantization_matrix = quantization.get_default_quantization_matrix(
                self.block_size, self.block_size)
        else:
            self.quantization_matrix = quantization.get_quantization_matrix(
                self.quantization_scale, self.block_size, self.block_size)
        
        image_dct           = dct.forward_dct(tmp_image_data, self.block_size, self.block_size)
        image_dct_quantized = quantization.quantize(image_dct, self.quantization_matrix)

        self.trans_shape    = image_dct_quantized.shape

        if self.compression_alg == compression.COMPRESSION_ALGORITHMS.ZIP:
            self.compressed_image = compression.compress_zip(image_dct_quantized)
        
        self.bCompressed = True

    def get_compressed_image(self):
        return self.compressed_image
    
    def save_compressed_file(self, path):
        if self.bCompressed:
            with open("{}.compressed".format(path), "wb") as f:
                f.write(self.compressed_image)

    def get_stats(self):
        
        if self.bCompressed:
            return {
                "original_file_name": self.image_file_name,
                "compressed_blob_size": len(self.compressed_image),
                "color_downsampled": self.bDownSampleColor,
                "block_size": self.block_size,
                "quantization_scale": "N/A" if self.bUseDefaultQMtx else self.quantization_scale,
                "quantization_matrix": self.quantization_matrix,
                "compression": "ZIP" if self.compression_alg == compression.COMPRESSION_ALGORITHMS.ZIP else "RLE",
                "trans_shape": self.trans_shape 
            }
        
        return None
    

class JPEGDecoder:
    
    def __init__(self,
                 encodedImage,
                 blockSize,
                 quantizationMatrix,
                 transShape,
                 compressionAlgorithm = compression.COMPRESSION_ALGORITHMS.ZIP,
                 bColorDownSampled = True):
        
        self.block_size          = blockSize
        self.quantization_matrix = quantizationMatrix

        self.bColorDownSampled   = bColorDownSampled
        self.bDecompressed       = False

        self.compression_alg     = compressionAlgorithm
        self.trans_shape         = transShape

        self.image_data          = encodedImage
        self.decompressed_image  = None

    def decompress(self):

        if compression.COMPRESSION_ALGORITHMS[self.compression_alg] == compression.COMPRESSION_ALGORITHMS.ZIP:
            image_decompressed = compression.decompress_zip(self.image_data, self.trans_shape)
        else:
            image_decompressed = None

        image_dequantized = quantization.dec_quantize(image_decompressed, self.quantization_matrix)
        image_idct        = dct.inverse_dct(image_dequantized, self.block_size, self.block_size)

        if self.bColorDownSampled:
            self.decompressed_image = colorspace.ycbcr2rgb(image_idct)
        else:
            self.decompressed_image = image_idct

        self.bDecompressed = True
    
    def get_decompressed_image(self):
        return self.decompressed_image
    
    def save_decompressed_image(self, path):
        if self.bDecompressed:
            cv2.imwrite("{}.jpeg".format(path), self.decompressed_image.astype(np.uint8))