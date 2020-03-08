import numpy as np
import cv2
import matplotlib.pyplot as plt
#test xml file with image
carpark = cv2.imread('vehicle.png', 0)

car_cascade = cv2.CascadeClassifier('cars.xml')

car_rects = car_cascade.detectMultiScale(carpark)

for (x,y,w,h) in car_rects:
    cv2.rectangle(carpark, (x,y), (x+w,y+h), (255,255,255), 10)

cv2.imshow('Result', carpark)
cv2.waitKey(0)

