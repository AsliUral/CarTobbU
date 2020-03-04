import cv2
import numpy
from parking_lot_manage_mark.parking_lot import ParkingLot
from tobb_etu_smart_car_park_python_api import smart_car_park_python_api

COLOR_WHITE = (255, 255, 255)
cameraID = "1"
parkZoneID = "1"
apiKey = "ABC"
camera = 'video/parking_lot_1.mp4'

cap = cv2.VideoCapture('video/parking_lot_1.mp4')
if cap.isOpened() == False:
    print(
        "Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")
parking_lots = []
ids = 0
a = 1
currentlyMarked = False
API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)



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

tempID = 1

coordinates = []

cv2.namedWindow('Tobb Etu Car Park')

cv2.setMouseCallback('Tobb Etu Car Park', draw_polygon)



while True:
    ret, frame = cap.read()
    for parking_lot in parking_lots:
        parking_lot.draw_parking_lot(frame)
        parking_lot.draw_contours(frame)
        parking_lot.draw_parking_lot_id(frame)


    if topLeft_clicked and botRight_clicked and topRight_clicked and botLeft_clicked and not currentlyMarked:
        parking_lot = ParkingLot(pt1, pt2, pt3, pt4, "P" +str(tempID), "MainCarPark",API)
        parking_lots.append(parking_lot)
        parking_lot.draw_parking_lot(frame)
        tempID = tempID + 1
        currentlyMarked = True


    cv2.imshow('Tobb Etu Car Park', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('r'):
        frame = frame.copy()


cap.release()
cv2.destroyAllWindows()
