from parking_lot_detection.ParkingLot.parkingLot import ParkingLot

def getPoint(point):
    if point is not None:
        point = point[1:len(point) - 1]
        point = point.split(',')
        return [int(point[0]) , int(point[1])]

def generateParkingLots(parkingLotsResponse):
    parkingLots = []
    for i in range(len(parkingLotsResponse)):
        if (parkingLotsResponse[i]["FirstPoint"] is not None and parkingLotsResponse[i]["FirstPoint"] != ''):
            parkingLots.append(ParkingLot(parkingLotsResponse[i]["ParkingLotID"],
                                      parkingLotsResponse[i]["ParkingLotStatus"],
                                      getPoint(parkingLotsResponse[i]["FirstPoint"]),
                                      getPoint(parkingLotsResponse[i]["SecondPoint"]),
                                      getPoint(parkingLotsResponse[i]["ThirdPoint"]),
                                      getPoint(parkingLotsResponse[i]["FourthPoint"])))
    return parkingLots