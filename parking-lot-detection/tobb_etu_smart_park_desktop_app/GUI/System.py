import time
from parking_lot_detection.model.yolo_model import YOLO
from parking_lot_detection.ParkingLot.parkingLotGenerator import generateParkingLots
from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
import cv2

class System:

  def __init__(self, parkZone):
    self.parkZone = parkZone
    self.API = None
    self.apiKey = "ABC"
    self.cameraConnectionClosed = False
    self.camera_port = parkZone.cameraIP
    self.camera = cv2.VideoCapture(parkZone.cameraIP)
    self.systemStarted = False
    self.API = smart_car_park_python_api.SmartCarParkAPI(cameraIP=self.parkZone.cameraIP,
                                                         parkZoneID=self.parkZone.parkingZoneID,
                                                         apiKey=self.apiKey,
                                                         parkZoneName=self.parkZone.parkZoneName)

    self.parkingLots_ODetection = self.getParkingLotsForDetection()
    self.fps = 25


  def loadModel(self):
      print("Model is loading...")
      self.yolo = YOLO(0.5, 0.4)
      self.file = '../../parking_lot_detection/data/coco_classes.txt'
      self.classes = self.get_classes(self.file)
      print("Model is loaded")

  def get_classes(self, file):
      with open(file) as f:
          class_names = f.readlines()
      class_names = [c.strip() for c in class_names]
      return class_names

  def createAPI(self):
      self.API = smart_car_park_python_api.SmartCarParkAPI(cameraIP=self.parkZone.cameraIP,
                                                           parkZoneID=self.parkZone.parkingZoneID,
                                                           apiKey=self.apiKey,
                                                           parkZoneName=self.parkZone.parkZoneName)

  def getParkingLotsForDetection(self):
      parkingLotsResponse = self.API.getAllParkingLotsOFParkZone()
      parkingLots_ODetection = generateParkingLots(parkingLotsResponse)
      return parkingLots_ODetection

  def readFrame(self):
      ret, frame = self.camera.read()
      return ret, frame

  def startSystem(self):
      print("Heyo")
      self.loadModel()
      if (self.parkZone.parkZoneName == "Ara Otopark" or self.parkZone.parkZoneName == "Main Car Park 45" ):
          print("Bu sistem basladı : ")
          print(self.parkZone.parkZoneName)

          self.createAPI()

          self.parkingLots_ODetection = self.getParkingLotsForDetection()

          self.camera = cv2.VideoCapture(self.camera_port)
          print("Su anda park zone " , self.parkZone.parkZoneName , " için çalısıyor ")
          while self.systemStarted == True:
              """Occupancy Detection Mode"""
              ret, frame = self.camera.read()

              # Noise
              blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)

              # Minimize data
              gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
              pos_sec = self.camera.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

              for i in range(len(self.parkingLots_ODetection)):
                  self.parkingLots_ODetection[i].check(pos_sec, gray, self.API, self.yolo, self.classes, frame)
                  self.parkingLots_ODetection[i].draw(frame)

              #frame = self.rescale_frame(frame)
              #color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
              #height, width, _ = color_swapped_image.shape
              """
              qt_image = QtGui.QImage(color_swapped_image.data,
                                      width,
                                      height,
                                      color_swapped_image.strides[0],
                                      QtGui.QImage.Format_RGB888)
              self.VideoSignal.emit(qt_image)
              """
              time.sleep(1 / self.fps)