import cv2
import numpy as np 

def rgb2ycbcr(rgb_image):
    rgb_image   = rgb_image.astype(np.float32)
    ycrcb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2YCR_CB)
    
    ycbcr_image = ycrcb_image[:, :, (0, 2, 1)].astype(np.float32)
    
    ycbcr_image[:, :, 0 ] = (ycbcr_image[:, :, 0 ] * (235-16)+16) / 255.0
    ycbcr_image[:, :, 1:] = (ycbcr_image[:, :, 1:] * (240-16)+16) / 255.0 
    
    return ycbcr_image


def ycbcr2rgb(ycbcr_image):
    ycbcr_image = ycbcr_image.astype(np.float32)
    
    ycbcr_image[:, :, 0 ] = (ycbcr_image[:, :, 0 ] * 255.0-16) / (235-16)
    ycbcr_image[:, :, 1:] = (ycbcr_image[:, :, 1:] * 255.0-16) / (240-16)
    
    ycrcb_image = ycbcr_image[:, :, (0, 2, 1)].astype(np.float32)
    rgb_image   = cv2.cvtColor(ycrcb_image, cv2.COLOR_YCR_CB2RGB)
    
    return rgb_image