import numpy as np
import cv2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class ParkingLot:

  def __init__(self, parkingLotID, status, firstPoint, secondPoint, thirdPoint, fourthPoint):
    self.parkingLotID = parkingLotID
    self.status = status
    self.sec = None
    self.borderPoints = [firstPoint, secondPoint, thirdPoint, fourthPoint]
    self.mask = 0
    self.contour = 0
    self.bound = 0
    self.bottom_left = (0, 0)
    self.bottom_right = (0, 0)
    self.top_left = (0, 0)
    self.top_right = (0, 0)
    self.pre_check()
    self.set_place_points([firstPoint, secondPoint, thirdPoint, fourthPoint])

  def set_place_points(self, points):
    self.set_top_points(points)
    self.set_bottom_point(points)

  def set_top_points(self, points):
    maxCurrent = points[0]
    maxCurrentValue = points[0][1]
    index = 0
    for i in range(len(points)):
      if(points[i][1] >= maxCurrentValue):
        maxCurrent = points[i]
        maxCurrentValue = points[i][1]
        index = i

    maxPrevious = -1
    maxPreviousValue = -1
    index2 = -1

    for j in range(len(points)):
      if(points[j][1] >= maxPreviousValue and index != j):
        maxPrevious = points[j]
        maxPreviousValue = points[j][1]
        index2 = j

    if (maxCurrent[0] < maxPrevious[0]):
      self.top_left = (maxCurrent, index)
      self.top_right = (maxPrevious, index2)
    else:
      self.top_left = (maxPrevious,index2)
      self.top_right = (maxCurrent, index)

  def set_bottom_point(self, points):
    bottomPrevious = points[0]
    bottomCurrent = points[0]
    counter = 1
    for i in range(len(points)):
      if ( i != self.top_left[1] and i != self.top_right[1] and counter == 1):
        bottomPrevious = (points[i], i)
        counter = counter + 1
      elif ( i != self.top_left[1] and i != self.top_right[1] and counter == 2):
        bottomCurrent = (points[i], i)

    if (bottomCurrent[0] < bottomPrevious[0]):
      self.bottom_left = bottomCurrent
      self.bottom_right = bottomPrevious
    else:
      self.bottom_left = bottomPrevious
      self.bottom_right = bottomCurrent

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

  def check(self, pos_sec, gray, centers_of_cars, API):
    status = self.get_status(gray, centers_of_cars)

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
    cv2.line(frame, tuple(self.top_left[0]), tuple(self.top_right[0]), self.get_color(), 2)
    cv2.line(frame, tuple(self.top_right[0]), tuple(self.bottom_right[0]), self.get_color(), 2)
    cv2.line(frame, tuple(self.bottom_right[0]), tuple(self.bottom_left[0]), self.get_color(), 2)
    cv2.line(frame, tuple(self.bottom_left[0]), tuple(self.top_left[0]), self.get_color(), 2)
    self.draw_parking_lot_id(frame)

  def draw_parking_lot_id(self, frame):
      COLOR_WHITE = (255, 255, 255)
      npBorderPoints = np.asarray(self.borderPoints)
      moments = cv2.moments(npBorderPoints)
      center = (int(moments["m10"] / moments["m00"]) - 3,
                int(moments["m01"] / moments["m00"]) + 3)
      cv2.putText(frame, self.parkingLotID, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)

  def get_status(self, grayed, centers_of_cars):
        coordinates = np.asarray(self.borderPoints)

        rectangle = self.bound

        region_of_interest = grayed[rectangle[1]:(rectangle[1] + rectangle[3]), rectangle[0]:(rectangle[0] + rectangle[2])]
        lap = cv2.Laplacian(region_of_interest, cv2.CV_64F)

        coordinates[:, 0] = coordinates[:, 0] - rectangle[0]
        coordinates[:, 1] = coordinates[:, 1] - rectangle[1]

        status = np.mean(np.abs(lap * self.mask)) < 1.4
        car_inside = self.car_inside(centers_of_cars)

        status_motion = self.motion_check(status)
        status_cascade = self.cascade_check(car_inside)
        """
        We can also use car cascade to detection
        """

        return status_motion

  def cascade_check(self, car_inside):
    if car_inside == True:
      return "Occupied"
    else:
      return "Available"

  def motion_check(self, status):
    if status == True:
      return "Available"
    else:
      return "Occupied"

  def car_inside(self, centers_of_cars):
    for i in range(len(centers_of_cars)):
      if (self.inside_polygon(centers_of_cars[i])):
        return True

    return False

  def inside_polygon(self, center_car):
    point = Point(center_car[0], center_car[1])
    polygon = Polygon([tuple(self.bottom_left[0]), tuple(self.bottom_right[0]), tuple(self.top_right[0]), tuple(self.top_left[0])])
    return polygon.contains(point)

  def __repr__(self):
    return ("Parking Lot ID : " + self.parkingLotID +
           " Parking Lot Status : "  + self.status+
           " Parking Lot Border Points: "  + str(self.borderPoints))