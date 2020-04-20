import yaml
from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
from tobb_etu_smart_park_desktop_app.GUI.parking_lot import ParkingLot
from tobb_etu_smart_park_desktop_app.GUI.VideoEditor import ShowVideo, ImageViewer, getPoint

cameraID = "global"
parkZoneID = "global"
parkZoneName = "global"
apiKey = "ABC"

class LogDB():
    data = None
    globalAPI = smart_car_park_python_api.SmartCarParkAPI(cameraIP=cameraID,
                                                          parkZoneID=parkZoneID,
                                                          apiKey=apiKey,
                                                          parkZoneName=parkZoneName)
    def log(self,minute,date,day):
        self.ParkingLots = []
        strMin = str(minute)
        strDate = str(date)
        strDate = strDate.replace(':', '-')
        strMin = strMin.replace(':', '-')
        strMin = strMin[0:strMin.rindex('.')]
        strMin = str(strMin)
        data = self.getServerParkingLots(strMin,strDate,day)

        print(strDate)
        print(strMin)
        with open('log'+strDate+'-'+strMin+'.yml', 'w') as outfile:
            yaml.dump(self.ParkingLots, outfile, default_flow_style=False)

    def getServerParkingLots(self,minute,date,day):
        lots_JSON = self.globalAPI.getAllParkingLots()
        counter = 0

        for i in range(len(lots_JSON)):
            if (lots_JSON[i]["FirstPoint"] is not None and lots_JSON[i]["FirstPoint"] != ''):
                data = dict(
                    ParkingLot = lots_JSON[i]["ParkingLotID"],
                    ParkingLotStatus = lots_JSON[i]["ParkingLotStatus"],
                    ParkZoneName = lots_JSON[i]["ParkZoneName"],
                    Date = date,
                    Day = day,
                    Minute = minute

                )
                self.ParkingLots.append(data)
