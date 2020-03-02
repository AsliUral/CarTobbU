from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
from parking_lot_detection.ParkingLot.parkingLotGenerator import generateParkingLots
import cv2
import time

cameraID = "1"
parkZoneID = "1"
apiKey = "ABCD"
camera = 'dataset/parking_lot_1.mp4'

API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)
parkingLotsResponse = API.getAllParkingLotsOFParkZone()
parkingLots = generateParkingLots(parkingLotsResponse)

cap = cv2.VideoCapture(camera)
fps = 40

if cap.isOpened() == False:
    print(
        "Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")

while cap.isOpened():

    ret, frame = cap.read()

    blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
    gray = cv2.cvtColor(blur , cv2.COLOR_BGR2GRAY)
    new_frame = frame.copy()
    pos_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0


    if ret == True:
        for i in range(len(parkingLots)):
            parkingLots[i].check(pos_sec, gray, API)
            parkingLots[i].draw(frame)

        time.sleep(1 / fps)
        cv2.imshow('Tobb Etu Smart Car Park', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()

