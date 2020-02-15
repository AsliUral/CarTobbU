import requests

class SmartCarParkAPI:
  def __init__(self, cameraID, parkZoneID, apiKey):
    self.cameraID = cameraID
    self.parkZoneID = parkZoneID
    self.apiEndpoint = "http://localhost:3000"
    self.apiKey = apiKey
  def getAllParkingLots(self):
    URL = self.apiEndpoint
    response = requests.get(url = URL + "/parkingLots")
    data = response.json()
    return data
  def getAllOccupiedParkingLots(self):
    URL = self.apiEndpoint
    response = requests.get(url = URL + "/occupiedParkingLots")
    data = response.json()
    return data
  def getAllAvailableParkingLots(self):
    URL = self.apiEndpoint
    response = requests.get(url = URL + "/availableParkingLots")
    data = response.json()
    return data
  def getAllOutOfServiceParkingLots(self):
    URL = self.apiEndpoint
    response = requests.get(url = URL + "/outOfServiceParkingLots")
    data = response.json()
    return data
  def getParkingLotByID(self, parkingLotID):
    URL = self.apiEndpoint
    response = requests.get(url = URL + "/parkingLots" + "/" + parkingLotID)
    data = response.json()
    return data
  def getAllParkZones(self):
      URL = self.apiEndpoint
      response = requests.get(url=URL + "/parkZone")
      data = response.json()
      return data
  def getAllParkingLotsOFParkZone(self):
      URL = self.apiEndpoint
      response = requests.get(url=URL + "/parkZone" + "/" + self.parkZoneID + "/parkingLots")
      data = response.json()
      return data
  def getAvailableParkingLotsOFParkZone(self, parkZoneID):
      URL = self.apiEndpoint
      response = requests.get(url=URL + "/parkZone" + "/" + parkZoneID + "/availableParkingLots")
      data = response.json()
      return data
  def getOccupiedParkingLotsOFParkZone(self, parkZoneID):
      URL = self.apiEndpoint
      response = requests.get(url=URL + "/parkZone" + "/" + parkZoneID + "/occupiedParkingLots")
      data = response.json()
      return data
  def createParkingLot(self, parkingLotStatus,parkingLotID, parkZoneName, firstPoint, secondPoint,thirdPoint,fourthPoint):
      URL = self.apiEndpoint
      parkingLot_data = {
        "status": parkingLotStatus,
        "parkingLotID": parkingLotID,
        "parkZoneName": parkZoneName,
        "firstPoint": firstPoint,
        "secondPoint": secondPoint,
        "thirdPoint": thirdPoint,
        "fourthPoint": fourthPoint
      }
      data = requests.post(url=URL + "/parkingLots", data=parkingLot_data)
      return data