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
    self.updatedParkingLotID = parkingLotID
    self.from_server = from_server
    self.highlighted = False
    self.deleted = False


  def getParkingLotID(self):
    return self.parkingLotID

  def highlight(self):
      self.highlighted = True

  def releaseHighlight(self):
      self.highlighted = False

  def up(self):
      self.highlighted = False

  def down(self):
      self.highlighted = False

  def right(self):
      self.highlighted = False

  def left(self):
      self.highlighted = False

  def draw_parking_lot(self, frame):
    HIGHLIGHTED = 204, 255, 0
    YELLOW = (51, 255, 255)
    color = ""
    if (self.highlighted == True):
        color = HIGHLIGHTED
    else:
        color = YELLOW

    cv2.polylines(frame, [self.points], True, color, 2)


  def draw_contours(self, frame):
      HIGHLIGHTED = 204, 255, 0
      YELLOW = (51, 255, 255)
      color = ""
      if (self.highlighted == True):
          color = HIGHLIGHTED
      else:
          color = YELLOW

      cv2.drawContours(frame,
                       [self.points],
                       contourIdx=-1,
                       color=color,
                       thickness=2,
                       lineType=cv2.LINE_8)

  def draw_parking_lot_id(self, frame):
      COLOR_WHITE = ( 82, 15, 186)
      moments = cv2.moments(self.points)
      center = (int(moments["m10"] / moments["m00"]) - 3,
                int(moments["m01"] / moments["m00"]) + 3)
      cv2.putText(frame, self.parkingLotID, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 2, cv2.LINE_AA)



