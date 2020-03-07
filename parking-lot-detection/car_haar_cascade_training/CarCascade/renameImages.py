# Renaming images according to our requirement

import os
import cv2
import numpy as np
i = 2925
path = r'C:\Users\BAG\Desktop\CarCascade\OwnCollection\non-vehicles\Right'
for image_name in os.listdir(path):
    old_file = os.path.join(path, image_name)
    
    if i < 1000:
        new_file = os.path.join(path,'image0'+str(i)+'.png' )
        os.rename(old_file,new_file)
    else:
        new_file = os.path.join(path,'image'+str(i)+'.png')
        os.rename(old_file,new_file)
        
    i+=1