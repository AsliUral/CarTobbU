import numpy as np
import cv2

class ParkingLot:

  def __init__(self, parkingLotID, status, firstPoint, secondPoint, thirdPoint, fourthPoint):
    self.parkingLotID = parkingLotID
    self.status = status
    self.borderPoints = [firstPoint, secondPoint, thirdPoint, fourthPoint]

  def get_color(self):
    if (self.status == "Available"):
      return (0, 255, 0)
    else :
      return (0, 0, 255)

  def draw(self, frame):
    pts = np.array(self.borderPoints, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], True, self.get_color(), thickness = 2)

  def __repr__(self):
    return ("Parking Lot ID : " + self.parkingLotID +
           " Parking Lot Status : "  + self.status+
           " Parking Lot Border Points: "  + str(self.borderPoints))