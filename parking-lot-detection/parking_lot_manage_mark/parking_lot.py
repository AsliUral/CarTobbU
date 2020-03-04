import numpy as numpy
import cv2

class ParkingLot:

  def __init__(self, pt1, pt2, pt3, pt4, parkingLotID, parkingZone,API):
    pts = numpy.array([list(pt1), list(pt2), list(pt3), list(pt4)], numpy.int32)
    pts = pts.reshape((-1, 1, 2))
    self.points = pts
    self.parkingLotID = parkingLotID
    self.parkingZone = parkingZone
    self.API = API

  def draw_parking_lot(self, frame):
    cv2.polylines(frame, [self.points], True, (51, 255, 255), 2)
    self.API.createParkingLot("Available",self.parkingLotID,"MainCarPark",self.points[0],self.points[1],self.points[2],self.points[3])


  def draw_contours(self, frame):
      COLOR_YELLOW = (51, 255, 255)
      cv2.drawContours(frame,
                       [self.points],
                       contourIdx=-1,
                       color=COLOR_YELLOW,
                       thickness=2,
                       lineType=cv2.LINE_8)

  def draw_parking_lot_id(self, frame):
      COLOR_WHITE = (255, 255, 255)
      moments = cv2.moments(self.points)
      center = (int(moments["m10"] / moments["m00"]) - 3,
                int(moments["m01"] / moments["m00"]) + 3)
      cv2.putText(frame, self.parkingLotID, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)



