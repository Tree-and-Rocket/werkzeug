import os
import numpy as np
import cv2
import os
from multiprocessing import Pool
from PIL import Image


def get_sharpness(image_path):
    # to grayscale
    im = Image.open(in_image_path).convert('L')
    array = np.asarray(im, dtype=np.int32)
    gy, gx = np.gradient(array)
    gnorm = np.sqrt(gx**2 + gy**2)
    return np.average(gnorm)


def resize_save(url):

    img = cv2.imread('images/' + url) 
    img = cv2.resize(img, (1024, 1024))
    cv2.imwrite("sphaeraIMGS/"  + url[:-4] + ".png", img)
    
    

if __name__ == "__main__":
    cpu_cores = 8
    p = Pool(cpu_cores)
    p.map(proc, os.listdir('images/'))
