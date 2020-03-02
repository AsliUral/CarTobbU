
import cv2
import numpy

cap=cv2.VideoCapture('video/parking_lot_1.mp4')
points = []

def draw_polygon(event, x, y, flags, param):
    global pt1, pt2,pt3,pt4, topLeft_clicked, botRight_clicked,topRight_clicked, botLeft_clicked

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



pt1 = (0,0)
pt2 = (0,0)
pt3 = (0,0)
pt4 = (0,0)
topLeft_clicked = False
botRight_clicked = False
botLeft_clicked = False
topRight_clicked = False

cv2.namedWindow('Tobb Etu Car Park')

cv2.setMouseCallback('Tobb Etu Car Park', draw_polygon)
while True:
    ret, frame = cap.read()

    for p in points:
        cv2.polylines(frame, [p], True, (51, 255, 255), 2)

    if topLeft_clicked and botRight_clicked and topRight_clicked and botLeft_clicked:
        pts = numpy.array([list(pt1) ,list(pt2) ,list(pt3) ,list(pt4)], numpy.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (51, 255, 255),2)
        points.append(pts)

    cv2.imshow('Tobb Etu Car Park', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()