import numpy as np
import cv2

class ParkingLot:

  def __init__(self, parkingLotID, status, firstPoint, secondPoint, thirdPoint, fourthPoint):
    self.parkingLotID = parkingLotID
    self.status = status
    self.sec = None
    self.borderPoints = [firstPoint, secondPoint, thirdPoint, fourthPoint]
    self.mask = 0
    self.contour = 0
    self.bound = 0
    self.pre_check()

  def get_color(self):
    if (self.status == "Available"):
      return (0, 255, 0)
    else :
      return (0, 0, 255)

  def pre_check(self):
    npBorderPoints = np.asarray(self.borderPoints)
    bound_rectangle = cv2.boundingRect(npBorderPoints)

    coordinates = npBorderPoints.copy()
    coordinates[:, 0] = npBorderPoints[:, 0] - bound_rectangle[0]
    coordinates[:, 1] = npBorderPoints[:, 1] - bound_rectangle[1]

    self.contour = npBorderPoints
    self.bound = bound_rectangle

    mask = cv2.drawContours(
      np.zeros((bound_rectangle[3], bound_rectangle[2]), dtype=np.uint8),
      [coordinates],
      contourIdx=-1,
      color=255,
      thickness=-1,
      lineType=cv2.LINE_8)

    mask = mask == 255

    self.mask = mask

  def check(self, pos_sec, gray, API):
    status = self.get_status(gray)

    if self.sec is not None and (self.status == status):
      self.sec = None

    if self.sec is not None and (self.status != status):
      if pos_sec - self.sec >= 1:
        if (status == "Available"):
          API.handleLeaving(self.parkingLotID)
          print("Handle Leaving : ", self.parkingLotID)
        else:
          API.handleParking(self.parkingLotID)
          print("Handle Parking : ", self.parkingLotID)
        self.status = status
        self.sec = None


    if self.sec is None and (self.status != status):
      self.sec = pos_sec

  def draw(self, frame):
    pts = np.array(self.borderPoints, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], True, self.get_color(), thickness = 2)

  def get_status(self, grayed):

        coordinates = np.asarray(self.borderPoints)

        rectangle = self.bound

        region_of_interest = grayed[rectangle[1]:(rectangle[1] + rectangle[3]), rectangle[0]:(rectangle[0] + rectangle[2])]
        lap = cv2.Laplacian(region_of_interest, cv2.CV_64F)

        coordinates[:, 0] = coordinates[:, 0] - rectangle[0]
        coordinates[:, 1] = coordinates[:, 1] - rectangle[1]

        status = np.mean(np.abs(lap * self.mask)) < 1.4

        if (status == True):
          return "Available"
        else:
          return "Occupied"

  def __repr__(self):
    return ("Parking Lot ID : " + self.parkingLotID +
           " Parking Lot Status : "  + self.status+
           " Parking Lot Border Points: "  + str(self.borderPoints))