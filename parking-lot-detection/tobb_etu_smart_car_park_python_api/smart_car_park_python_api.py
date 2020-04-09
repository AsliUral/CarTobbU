import requests

class SmartCarParkAPI:
  def __init__(self, cameraIP, parkZoneID, apiKey, parkZoneName):
    self.cameraIP = cameraIP
    self.parkZoneID = parkZoneID
    self.parkZoneName = parkZoneName
    self.apiEndpoint = "https://smart-car-park-api.appspot.com"
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
        "parkZoneName": self.parkZoneName,
        "firstPoint": firstPoint,
        "secondPoint": secondPoint,
        "thirdPoint": thirdPoint,
        "fourthPoint": fourthPoint
      }
      data = requests.post(url=URL + "/parkingLots", data=parkingLot_data)
      return data

  def updateParkingLotByID(self, targetParkingLotID, parkingLotStatus,parkingLotID, parkZoneName, firstPoint, secondPoint,thirdPoint,fourthPoint):
      URL = self.apiEndpoint
      parkingLot_data = {
        "status": parkingLotStatus,
        "parkingLotID": parkingLotID,
        "parkZoneName": self.parkZoneName,
        "firstPoint": firstPoint,
        "secondPoint": secondPoint,
        "thirdPoint": thirdPoint,
        "fourthPoint": fourthPoint
      }
      data = requests.put(url=URL + "/parkingLots/" + str(targetParkingLotID), data=parkingLot_data)
      return data

  def deleteParkingLotByID(self, parkingLotID):
      URL = self.apiEndpoint
      data = requests.delete(url=URL + "/parkingLots/" + str(parkingLotID))
      return data

  def handleParking(self, parkingLotID):
      URL = self.apiEndpoint
      requests.put(url=URL + "/handleParking" + "/" + str(parkingLotID))

  def handleLeaving(self, parkingLotID):
      URL = self.apiEndpoint
      requests.put(url=URL + "/handleLeaving" + "/" + str(parkingLotID))

  def handleLeaving(self, parkingLotID):
      URL = self.apiEndpoint
      requests.put(url=URL + "/handleLeaving" + "/" + str(parkingLotID))

  def login(self,username,password):
      URL = self.apiEndpoint
      user = {
        "username" : username,
        "password" : password,

      }
      successLogin = False
      response = requests.post(url=URL + "/user/login", data=user)
      responseJ= response.json()
      if 'ApiKey' in responseJ:
          successLogin = True
          return successLogin
      else:
           print("User name or password is incorrect")
           successLogin = False
           return successLogin

  def register(self, username, fullname, password,email,phone):
      URL = self.apiEndpoint
      user = {
          "username": username,
          "password": password,
          "personFullName": fullname,
          "PhoneNumber": phone,
          "Email": email,
          "userType":"Admin",
          "allowedCarParks":"Academic Only Car Park"

      }

      response = requests.post(url=URL + "/user/register", data=user)
      print(response.status_code)
      if response.status_code == 200:
          successRegister = True
          return successRegister
      else:
          print("Register problem")
          successRegister = False
          return successRegister


