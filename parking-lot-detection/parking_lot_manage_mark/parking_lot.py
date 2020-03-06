import numpy as numpy
import cv2

class ParkingLot:

  def __init__(self, pt1, pt2, pt3, pt4, parkingLotID, parkingZone,API, from_server):
    pts = numpy.array([list(pt1), list(pt2), list(pt3), list(pt4)], numpy.int32)
    pts = pts.reshape((-1, 1, 2))
    self.points = pts
    self.parkingLotID = parkingLotID
    self.parkingZone = parkingZone
    self.API = API
    self.from_server = from_server
    first = "[" + str(pt1[0]) + "," + str(pt1[1]) + "]"
    second = "[" + str(pt2[0]) + "," + str(pt2[1]) + "]"
    third = "[" + str(pt3[0]) + "," + str(pt3[1]) + "]"
    fourth = "[" + str(pt4[0]) + "," + str(pt4[1]) + "]"
    if (from_server == False):
        self.API.createParkingLot("Available", self.parkingLotID, parkingZone, first, second, third, fourth)


  def draw_parking_lot(self, frame):
    cv2.polylines(frame, [self.points], True, (51, 255, 255), 2)


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



