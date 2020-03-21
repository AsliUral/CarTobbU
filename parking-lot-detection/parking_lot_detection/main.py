from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
from parking_lot_detection.ParkingLot.parkingLotGenerator import generateParkingLots
import cv2
import time
import sys
from model.yolo_model import YOLO


def get_classes(file):
    with open(file) as f:
        class_names = f.readlines()
        print("Class Names : " , class_names)
    class_names = [c.strip() for c in class_names]
    return class_names


def main():
    yolo = YOLO(0.5, 0.4)
    file = 'data/coco_classes.txt'
    classes = get_classes(file)
    cameraID = "1"

    parkZoneID = "1"# Test
    #parkZoneID = "15"#Tobb ETU Main

    camera = 'dataset/parking_lot_1.mp4'#Test
    #camera = 'dataset/tobb_etu_main.mp4'#Tobb ETU Main

    apiKey = "ABCD"

    API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)
    parkingLotsResponse = API.getAllParkingLotsOFParkZone()
    parkingLots = generateParkingLots(parkingLotsResponse)

    cap = cv2.VideoCapture(camera)
    fps = 150

    if cap.isOpened() == False:
        print(
            "Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")

    while cap.isOpened():

        ret, frame = cap.read()

        #Noise
        blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)

        #Minimize data
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        pos_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        if ret == True:
            for i in range(len(parkingLots)):
                parkingLots[i].check(pos_sec, gray, API, yolo, classes, frame)
                parkingLots[i].draw(frame)

            time.sleep(1 / fps)
            cv2.imshow('Tobb Etu Smart Car Park', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

