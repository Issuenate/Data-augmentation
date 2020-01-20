# -*- coding:utf-8 -*-
import random
import math
import cv2
import skimage
from skimage.util import random_noise
from skimage import img_as_ubyte
from skimage import exposure

def random_aug(img,x):
    #giving a x as random parameter to decide which transformation adopted
    if x ==1:
        img = increase_brightness(img, value=(random.randint(10,30)))
        
    elif x ==2:
        img = rotation_point(img,angle=(random.randint(10,170),True))
        
    elif x ==3:
        img = cv2.GaussianBlur(img, (3, 3), 0)
        
    elif x ==4:
        img = random_noise(img, mode='gaussian', seed=None, clip=True, **kwargs)
        img = img_as_ubyte(img)
        
    elif x ==5:
        img = aj_contrast(img)
        
    return img


def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def rotation_point(img,angle,keep_size = False):    
    if keep_size:
        cols = img.shape[1]
        rows = img.shape[0]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        img = cv2.warpAffine(img, M, (cols, rows))		
        return img
    else:
        cols = img.shape[1]
        rows = img.shape[0]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)

        heightNew = int(cols * math.fabs(math.sin(math.radians(angle))) + rows* math.fabs(math.cos(math.radians(angle))))
        widthNew = int(rows * math.fabs(math.sin(math.radians(angle))) + cols* math.fabs(math.cos(math.radians(angle))))
        M[0, 2] += (widthNew - cols) / 2
        M[1, 2] += (heightNew - rows) / 2

        img = cv2.warpAffine(img, M, (widthNew, heightNew))
        
        
        return img

def aj_contrast(img):    
    img= skimage.exposure.adjust_gamma(img,(random.random(0.5,1.5)))
    img = img_as_ubyte(img)
    return img
