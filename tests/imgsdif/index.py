

from skimage.io import imsave, imread
from skimage.util import img_as_ubyte, img_as_float, img_as_int
import numpy as np
from skimage.transform import resize
import time
start_time = time.time()


img1 = imread('img.png')
img2 = imread('img2.png')

img1 = resize(img1, (int((600 / img1.shape[1])*img1.shape[0]), 600))
img2 = resize(img2, (int((600 / img2.shape[1])*img2.shape[0]), 600))
        
white_image = img1.copy()
white_image[:,:,:] = 1
img2 = np.where(img2 != img1, img2, white_image)

imsave('diff.png', img_as_ubyte(img2))
print('end_time', time.time() - start_time)