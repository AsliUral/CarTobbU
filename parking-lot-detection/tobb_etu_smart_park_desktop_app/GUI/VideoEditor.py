# Importing necessary libraries, mainly the OpenCV, and PyQt libraries
import cv2
import os
import numpy as np
import tensorflow as tf
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

# Import utilites
from parking_slot_detection.utils import label_map_util
from parking_slot_detection.utils import visualization_utils as vis_util


rescaleFactor = None
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

    print("Return : " , parkingLots)
    return parkingLots, max + 1


cameraID = "1"
parkZoneID = "45"
parkZoneName = "Main Car Park 45"

apiKey = "ABC"
API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)

parking_lots, autoIncrement  = get_parking_lots(API)
autoLetter = 'Q'

COLOR_WHITE = (255, 255, 255)

fps = 25

startDetection = False
currentlyMarked = False




def draw_polygon(event):
    global pt1, pt2, pt3, pt4, topLeft_clicked, botRight_clicked, topRight_clicked, botLeft_clicked
    global currentlyMarked
    x = event.x()
    y = event.y()
    if(rescaleFactor):
        x=int(x*100/66)
        y=int(y*100/66)

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
    #camera_port = "parking_lot_1.mp4"
    camera_port = "tobb_etu_main.mp4"
    #camera_port = "parking_lot_1.mp4"
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

        self.slotDetectionStarted = False
        self.slotFirstRun = True
        self.autoIncrement = autoIncrement
        self.autoLetter = autoLetter

    def rescale_frame(self,frame):
        scale_percent_val = 66
        from win32api import GetSystemMetrics
        generalWidth = 1920
        generalHeight = 1080

        if GetSystemMetrics(0) > generalWidth and GetSystemMetrics(1) > generalHeight :
            width = int(frame.shape[1])
            height = int(frame.shape[0])
            dim = (width, height)
            global rescaleFactor
            rescaleFactor=False
            return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        else:
            width = int(frame.shape[1])
            height = int(frame.shape[0])
            if width < GetSystemMetrics(0) and height < GetSystemMetrics(1):
                dim = (width, height)
                rescaleFactor = False
                return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            else:
                width = int(frame.shape[1] * scale_percent_val / 100)
                height = int(frame.shape[0] * scale_percent_val / 100)
                dim = (width, height)
                rescaleFactor = True
                return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    @QtCore.pyqtSlot()
    def startVideo(self):
        run_video = True
        while run_video:

            if (self.occupancyFirstRun == True and self.occupancyDetectionStarted == True):
                (self.yolo, self.classes, self.parkingLots_ODetection) = self.detectionConfigurations()
                self.occupancyFirstRun = False

            if (self.slotFirstRun == True and self.slotDetectionStarted == True):
                self.parkingslotdetectionConfigurations()
                self.slotFirstRun = False

            """Parking Slot Mode"""
            if self.occupancyDetectionStarted == False:
                if self.slotDetectionStarted == False:
                    ret, frame = self.camera.read()

                    global currentlyMarked
                    self.parking_lots = parking_lots
                    for parking_lot in parking_lots:
                        parking_lot.draw_parking_lot(frame)
                        parking_lot.draw_contours(frame)
                        parking_lot.draw_parking_lot_id(frame)

                    if topLeft_clicked and botRight_clicked and topRight_clicked and botLeft_clicked and not currentlyMarked:
                        self.autoIncrement = int(self.autoIncrement)
                        parking_lot = ParkingLot(pt1, pt2, pt3, pt4, str(self.autoLetter) + str(self.autoIncrement), "Ara Otopark", None,
                                                 from_server=False)
                        parking_lots.append(parking_lot)
                        parking_lot.draw_parking_lot(frame)
                        self.autoIncrement = self.autoIncrement + 1
                        currentlyMarked = True

                    frame = self.rescale_frame(frame)
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

                    ret, frame = self.camera.read()
                    frame_expanded = np.expand_dims(frame, axis=0)

                    (boxes, scores, classes, num) = self.sess.run(
                        [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
                        feed_dict={self.image_tensor: frame_expanded})

                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        self.category_index,
                        use_normalized_coordinates=True,
                        line_thickness=1,
                        min_score_thresh=0.50)
                    frame = self.rescale_frame(frame)
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
                frame = self.rescale_frame(frame)
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

    def parkingslotdetectionConfigurations(self):
        import sys
        sys.path.append('C:/tensorflow1/models; C:/tensorflow1/models/research;C:/tensorflow1/models/research/slim')
        MODEL_NAME = 'inference_graph'
        CWD_PATH = os.getcwd()
        PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
        PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')
        NUM_CLASSES = 1

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)


        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.sess = tf.Session(graph=detection_graph)

        self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')


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
