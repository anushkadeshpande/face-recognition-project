# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 02:00:04 2022

@author: Anushka
"""
def saveModels():
    from vgg16_rec2 import vgg16
    from facenet128 import facenet128
    from facenet512 import facenet512

    vgg16()
    facenet128()
    facenet512()