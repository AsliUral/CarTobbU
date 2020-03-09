import cv2
import numpy
from parking_lot_manage_mark.parking_lot import ParkingLot
from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
from parking_lot_detection.ParkingLot.parkingLotGenerator import generateParkingLots



def getPoint(point):
    if point is not None:
        point = point[1:len(point) - 1]
        point = point.split(',')
        return [int(point[0]) , int(point[1])]

def get_parking_lots(API):
    parking_lot_JSON = API.getAllParkingLotsOFParkZone()
    parkingLots = []
    counter = 1
    max = 0
    for i in range(len(parking_lot_JSON)):
        if (parking_lot_JSON[i]["FirstPoint"] is not None and parking_lot_JSON[i]["FirstPoint"] != ''):
            parkingLots.append(ParkingLot(
                                          from_server=True,
                                          parkingLotID=parking_lot_JSON[i]["ParkingLotID"],
                                          pt1=(getPoint(parking_lot_JSON[i]["FirstPoint"])[0],getPoint(parking_lot_JSON[i]["FirstPoint"])[1]),
                                          pt2=(getPoint(parking_lot_JSON[i]["SecondPoint"])[0],getPoint(parking_lot_JSON[i]["SecondPoint"])[1]),
                                          pt3=(getPoint(parking_lot_JSON[i]["ThirdPoint"])[0],getPoint(parking_lot_JSON[i]["ThirdPoint"])[1]),
                                          pt4=(getPoint(parking_lot_JSON[i]["FourthPoint"])[0],getPoint(parking_lot_JSON[i]["FourthPoint"])[1]),
                                          API=API,
                                          parkingZone=parking_lot_JSON[i]["ParkZoneName"]))
            counter += 1
            id = parking_lot_JSON[i]["ParkingLotID"]
            if (int(id[1:]) > max):
                max = int(id[1:])

    print("Return : " , parkingLots)
    return parkingLots, max + 1


COLOR_WHITE = (255, 255, 255)
cameraID = "1"
parkZoneID = "5"
apiKey = "ABC"
camera = 'video/parking_lot_1.mp4'


API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)
parking_lots, tempID  = get_parking_lots(API)
ids = 0
a = 1
startDetection = False
currentlyMarked = False




def draw_polygon(event, x, y, flags, param):
    global pt1, pt2, pt3, pt4, topLeft_clicked, botRight_clicked, topRight_clicked, botLeft_clicked
    global currentlyMarked
    if event == cv2.EVENT_LBUTTONDOWN:

        if topLeft_clicked == True and botRight_clicked == True and botLeft_clicked == True and topRight_clicked == True:
            topLeft_clicked = False
            botRight_clicked = False
            botLeft_clicked = False
            topRight_clicked = False
            pt1 = (0, 0)
            pt2 = (0, 0)
            pt3 = (0, 0)
            pt4 = (0, 0)
            currentlyMarked = False

        if topLeft_clicked == False:
            pt1 = (x, y)
            topLeft_clicked = True

        elif botRight_clicked == False:
            pt2 = (x, y)
            botRight_clicked = True

        elif botLeft_clicked == False:
            pt3 = (x, y)
            botLeft_clicked = True

        elif topRight_clicked == False:
            pt4 = (x, y)
            topRight_clicked = True

pt1 = (0, 0)
pt2 = (0, 0)
pt3 = (0, 0)
pt4 = (0, 0)
topLeft_clicked = False
botRight_clicked = False
botLeft_clicked = False
topRight_clicked = False

coordinates = []

cv2.namedWindow('Tobb Etu Car Park')

cv2.setMouseCallback('Tobb Etu Car Park', draw_polygon)



cap = cv2.VideoCapture('video/parking_lot_1.mp4')
if cap.isOpened() == False:
    print(
        "Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")
while True:
    ret, frame = cap.read()
    for parking_lot in parking_lots:
        parking_lot.draw_parking_lot(frame)
        parking_lot.draw_contours(frame)
        parking_lot.draw_parking_lot_id(frame)


    if topLeft_clicked and botRight_clicked and topRight_clicked and botLeft_clicked and not currentlyMarked:
        parking_lot = ParkingLot(pt1, pt2, pt3, pt4, "C" +str(tempID), "Main Car Park",API,from_server=False)
        parking_lots.append(parking_lot)
        parking_lot.draw_parking_lot(frame)
        tempID = tempID + 1
        currentlyMarked = True


    cv2.imshow('Tobb Etu Car Park', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('o'):
        startDetection = True



cap.release()
cv2.destroyAllWindows()


