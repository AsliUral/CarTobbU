class ParkingZone:

 def __init__(self,  parkingZoneID, parkZoneName,API, cameraIP):
   self.parkingZoneID = parkingZoneID
   self.parkZoneName = parkZoneName
   self.API = API
   self.isSelected = False
   self.button = None
   self.cameraIP = cameraIP
