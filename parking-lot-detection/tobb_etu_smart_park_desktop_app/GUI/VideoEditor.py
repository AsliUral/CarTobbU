# Importing necessary libraries, mainly the OpenCV, and PyQt libraries
import cv2
import numpy as np
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
import time
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QToolBar, QToolButton, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout

from parking_lot_detection.model.yolo_model import YOLO
from parking_lot_detection.ParkingLot.parkingLotGenerator import generateParkingLots


from tobb_etu_smart_park_desktop_app.GUI.parking_lot import ParkingLot
from tobb_etu_smart_car_park_python_api import smart_car_park_python_api

def getPoint(point):
    if point is not None:
        point = point[1:len(point) - 1]
        point = point.split(',')
        return [int(point[0]) , int(point[1])]

def get_parking_lots(API):
    parking_lot_JSON = API.getAllParkingLotsOFParkZone()
    parkingLots = []
    counter = 1
    max = 0
    for i in range(len(parking_lot_JSON)):
        if (parking_lot_JSON[i]["FirstPoint"] is not None and parking_lot_JSON[i]["FirstPoint"] != ''):
            parkingLots.append(ParkingLot(
                                          from_server=True,
                                          parkingLotID=parking_lot_JSON[i]["ParkingLotID"],
                                          pt1=(getPoint(parking_lot_JSON[i]["FirstPoint"])[0],getPoint(parking_lot_JSON[i]["FirstPoint"])[1]),
                                          pt2=(getPoint(parking_lot_JSON[i]["SecondPoint"])[0],getPoint(parking_lot_JSON[i]["SecondPoint"])[1]),
                                          pt3=(getPoint(parking_lot_JSON[i]["ThirdPoint"])[0],getPoint(parking_lot_JSON[i]["ThirdPoint"])[1]),
                                          pt4=(getPoint(parking_lot_JSON[i]["FourthPoint"])[0],getPoint(parking_lot_JSON[i]["FourthPoint"])[1]),
                                          API=API,
                                          parkingZone=parking_lot_JSON[i]["ParkZoneName"]))
            counter += 1
            id = parking_lot_JSON[i]["ParkingLotID"]
            if (int(id[1:]) > max):
                max = int(id[1:])

    #print("Return : " , parkingLots)
    return parkingLots, max + 1


cameraID = "1"
parkZoneID = "45"
parkZoneName = "Main Car Park 45"

apiKey = "ABC"
API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)


parking_lots, tempID  = get_parking_lots(API)

COLOR_WHITE = (255, 255, 255)

fps = 25

startDetection = False
currentlyMarked = False


def draw_polygon(event):
    global pt1, pt2, pt3, pt4, topLeft_clicked, botRight_clicked, topRight_clicked, botLeft_clicked
    global currentlyMarked
    x = event.x()
    y = event.y()

    if topLeft_clicked == True and botRight_clicked == True and botLeft_clicked == True and topRight_clicked == True:
        topLeft_clicked = False
        botRight_clicked = False
        botLeft_clicked = False
        topRight_clicked = False
        pt1 = (0, 0)
        pt2 = (0, 0)
        pt3 = (0, 0)
        pt4 = (0, 0)
        currentlyMarked = False

    if topLeft_clicked == False:
        pt1 = (x, y)
        topLeft_clicked = True

    elif botRight_clicked == False:
        pt2 = (x, y)
        botRight_clicked = True

    elif botLeft_clicked == False:
        pt3 = (x, y)
        botLeft_clicked = True

    elif topRight_clicked == False:
        pt4 = (x, y)
        topRight_clicked = True


pt1 = (0, 0)
pt2 = (0, 0)
pt3 = (0, 0)
pt4 = (0, 0)
topLeft_clicked = False
botRight_clicked = False
botLeft_clicked = False
topRight_clicked = False

coordinates = []
points = []


def slot_method():
    print('slot method called.')

class ShowVideo(QtCore.QObject):
    camera_port = "tobb_etu_main.mp4"
    camera = cv2.VideoCapture(camera_port)
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)


    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)
        self.parking_lots = []
        self.API = API
        self.parkZoneID = parkZoneID
        self.parkZoneName = parkZoneName
        self.occupancyDetectionStarted = False
        self.occupancyFirstRun = True

    def changeVideo(self):
        self.camera_port = "parking_lot_1.mp4"
        self.camera = cv2.VideoCapture(self.camera_port)
        self.VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    @QtCore.pyqtSlot()
    def startVideo(self):
        run_video = True
        while run_video:

            if (self.occupancyFirstRun == True and self.occupancyDetectionStarted == True):
                (self.yolo, self.classes, self.parkingLots_ODetection) = self.detectionConfigurations()
                self.occupancyFirstRun = False

            """Parking Slot Mode"""
            if self.occupancyDetectionStarted == False:
                ret, frame = self.camera.read()
                global currentlyMarked, tempID
                self.parking_lots = parking_lots
                for parking_lot in parking_lots:
                    parking_lot.draw_parking_lot(frame)
                    parking_lot.draw_contours(frame)
                    parking_lot.draw_parking_lot_id(frame)

                if topLeft_clicked and botRight_clicked and topRight_clicked and botLeft_clicked and not currentlyMarked:
                    parking_lot = ParkingLot(pt1, pt2, pt3, pt4, "Q" + str(tempID), "Ara Otopark", None,
                                             from_server=False)
                    parking_lots.append(parking_lot)
                    parking_lot.draw_parking_lot(frame)
                    tempID = tempID + 1
                    currentlyMarked = True

                color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, _ = color_swapped_image.shape
                qt_image = QtGui.QImage(color_swapped_image.data,
                                        width,
                                        height,
                                        color_swapped_image.strides[0],
                                        QtGui.QImage.Format_RGB888)
                self.VideoSignal.emit(qt_image)
                time.sleep(1 / fps)
            else:
                """Occupancy Detection Mode"""
                ret, frame = self.camera.read()

                # Noise
                blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)

                # Minimize data
                gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
                pos_sec = self.camera.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

                for i in range(len(self.parkingLots_ODetection)):
                    self.parkingLots_ODetection[i].check(pos_sec, gray, API, self.yolo, self.classes, frame)
                    self.parkingLots_ODetection[i].draw(frame)

                color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, _ = color_swapped_image.shape
                qt_image = QtGui.QImage(color_swapped_image.data,
                                        width,
                                        height,
                                        color_swapped_image.strides[0],
                                        QtGui.QImage.Format_RGB888)
                self.VideoSignal.emit(qt_image)
                time.sleep(1 / fps)


    def get_classes(self, file):
        with open(file) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def detectionConfigurations(self):
        yolo = YOLO(0.5, 0.4)
        file = '../../parking_lot_detection/data/coco_classes.txt'
        classes = self.get_classes(file)
        parkingLotsResponse = API.getAllParkingLotsOFParkZone()
        parkingLots_ODetection = generateParkingLots(parkingLotsResponse)
        return(yolo, classes, parkingLots_ODetection)





class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.mouseReleaseEvent = draw_polygon




    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    """
    def draw_polygon(self, event):

        x = event.x()
        y = event.y()
        #image = cv2.circle(image, center_coordinates, radius, color, thickness)
        points.append((x, y))
        print("X : " , x , " Y : " , y)
        self.currentPoint = (x,y)
        self.triggerFunction()

    """
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()
