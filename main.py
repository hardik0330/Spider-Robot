
import cv2
import cv2.aruco
import numpy as np
import socket
from threading import Thread

HOST = '192.168.43.117'
PORT1 = 8081
PORT2 = 8082
PORT3 = 8083
PORT4 = 8084


def sock1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        s1.bind((HOST, PORT1))
        s1.listen(5)
        conn1, addr1 = s1.accept()
        print('Got connection from', addr1)


def sock2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.bind((HOST, PORT2))
        s2.listen(5)
        conn2, addr2 = s2.accept()
        print('Got connection from', addr2)


def sock3():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
        s3.bind((HOST, PORT3))
        s3.listen(5)
        conn3, addr3 = s3.accept()
        print('Got connection from', addr3)


def sock4():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s4:
        s4.bind((HOST, PORT4))
        s4.listen(5)
        conn4, addr4 = s4.accept()
        print('Got connection from', addr4)


def send_data(data, marker):
    message = str(data)
    if marker == 211:
        sock1().conn1.send(message.encode())
    elif marker == 123:
        sock2().conn2.send(message.encode())
    elif marker == 177:
        sock3().conn3.send(message.encode())
    elif marker == 89:
        sock4().conn4.send(message.encode())
    print(message)


def createGrid(img):
    i = 0
    # basically just drawing a line after every quarter of the screen
    # vertical
    while i < 12:
        pt1_x = pt2_x = (int)(i * (img.shape[1] / 12))
        pt1_y = 0
        pt2_y = (int)(img.shape[0])
        cv2.line(img, (pt1_x, pt1_y), (pt2_x, pt2_y), (0, 0, 0), 1, 0, 0)
        i = i + 1
    i = 0
    # horizontal
    while i < 12:
        pt1_y = pt2_y = (int)(i * (img.shape[0] / 12))
        pt1_x = 0
        pt2_x = (int)(img.shape[1])
        cv2.line(img, (pt1_x, pt1_y), (pt2_x, pt2_y), (0, 0, 0), 1, 0, 0)
        i = i + 1


def checkMarker(img, ids, position):
    # Logic: divide the centre coordinates with the size of row/ column
    # The integer part of quotient is the grid box number
    # col_check and row_check for the size of col and row
    col_check = img.shape[1] / 12
    # img.shape[0] gives height of screen , 1 gives width
    row_check = img.shape[0] / 12
    div = [col_check, row_check]
    i = 0
    while i < len(position):
        result = np.divide(position[i], div)
        # converting the grid box coordinate (eg. (2,3)) to a single box number
        # Logic: for (x,y) box number is x+12y.
        print(ids, ":", (int)(result[0]) + (12 * (int)(result[1])))
        # ids is a 2d array returned by detectMarkers
        i = i + 1


def orientation(img, top_left, top_right, ids):
    x1 = top_left[0]
    y1 = top_left[1]
    x2 = top_right[0]
    y2 = top_right[1]
    s1 = (x1 + x2) / 2
    s2 = (y1 + y2) / 2
    # destination coord
    d1 = 250.0
    d2 = 250.0
    orient = ""
    if abs(x2 - x1) <= 20:
        if y1 > y2:
            orient = "west"
        elif y2 > y1:
            orient = "east"
    elif (x2 - x1) > 0:     # upright
        if abs(y2 - y1) <= 20:
            orient = "north"
        elif (y2 > y1):
            orient = "ne"
        elif (y1 > y2):
            orient = "nw"
    elif (x2 - x1) < 0:
        if abs(y2 - y1) <= 20:
            orient = "south"
        elif (y1 > y2):
            orient = "sw"
        elif (y2 > y1):
            orient = "se"
    # route planning
    # aruco facing up / north
    # source = s1,s2
    # destination = d1, d2
    if abs(s1 == d1) & abs(s2 == d2):
        data = 'Stop'
    # north ne nw
    elif orient == "north":
        if abs(s1 - d1) <= 10:
            if s2 > d2:
                data = 'for'
            else:
                data = 'back'
        elif s1 < d1:
            data = 'right'
        elif s1 > d1:
            data = 'left'
    elif orient == "nw":
        if abs(s1 - d1) <= 10:
            if s2 > d2:
                data = 'fleft'
            else:
                data = 'brt'
        elif s1 < d1:
            data = 'frt'
        elif s1 > d1:
            data = 'bleft'
    elif orient == "ne":
        if abs(s1 - d1) <= 10:
            if s2 > d2:
                data = 'frt'
            else:
                data = 'bleft'
        elif s1 < d1:
            data = 'brt'
        elif s1 > d1:
            data = 'fleft'
    # south sw se
    elif orient == "south":
        if abs(s1 - d1) <= 10:
            if s2 > d2:
                data = 'back'
            else:
                data = 'for'
        elif s1 < d1:
            data = 'left'
        elif s1 > d1:
            data = 'right'
    elif orient == "se":
        if abs(s1 - d1) <= 10:
            if s2 > d2:
                data = 'fleft'
            else:
                data = 'brt'
        elif s1 < d1:
            data = 'frt'
        elif s1 > d1:
            data = 'bleft'
    elif orient == "sw":
        if abs(s1 - d1) <= 10:
            if s2 > d2:
                data = 'frt'
            else:
                data = 'bleft'
        elif s1 < d1:
            data = 'brt'
        elif s1 > d1:
            data = 'fleft'
    # east and west
    elif orient == "east":
        if abs(s2 - d2) <= 10:
            if s1 < d1:
                data = 'for'
            else:
                data = 'back'
        elif s2 < d2:
            data = 'left'
        elif s2 > d2:
            data = 'right'
    elif orient == "west":
        if abs(s2 - d2) <= 10:
            if s1 < d1:
                data = 'back'
            else:
                data = 'for'
        elif s2 < d2:
            data = 'right'
        elif s2 > d2:
            data = 'left'
    send_data(data, ids)


t1 = Thread(target=sock1)
t2 = Thread(target=sock2)
t3 = Thread(target=sock3)
t4 = Thread(target=sock4)
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()
cap = cv2.VideoCapture(1)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
while True:
    ret, frame = cap.read()
    # getting all the values in different variables
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, dictionary)
    # createGrid(frame)
    if len(corners) > 0:
        # draw only if aruco detected
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        i = 0
        # nested loop only for centre coordinates
        while i < len(corners):
            # corners contains 4 coordinates of the aruco (2d array)
            j = 0
            while j < len(corners[i]):
                # first taking sum of all x coord, then divide by 4. Then y
                pos = np.sum(corners[i], axis=1) / 4
                j = j + 1
                # call the function for position
                # checkMarker(frame, ids[i], pos)
                orientation(frame, corners[0][0][0], corners[0][0][1], ids[i])
            i = i + 1
        print("\n")
    cv2.imshow('out', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
