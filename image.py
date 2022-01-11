import os
import numpy as np
from PIL import Image


def get_sharpness(image_path):
    # to grayscale
    im = Image.open(in_image_path).convert('L')
    array = np.asarray(im, dtype=np.int32)
    gy, gx = np.gradient(array)
    gnorm = np.sqrt(gx**2 + gy**2)
    return np.average(gnorm)
