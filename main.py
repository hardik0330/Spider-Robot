
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


def sock1(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        if data == "1":
            s1.bind((HOST, PORT1))
            s1.listen(5)
            global conn1, addr1
            conn1, addr1 = s1.accept()
            print('Got connection from', addr1)
        else:
            conn1.send(data.encode())


def sock2(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        if data == "1":
            s2.bind((HOST, PORT2))
            s2.listen(5)
            global conn2, addr2
            conn2, addr2 = s2.accept()
            print('Got connection from', addr2)
        else:
            conn2.send(data.encode())


def sock3(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
        if data == "1":
            s3.bind((HOST, PORT3))
            s3.listen(5)
            global conn3, addr3
            conn3, addr3 = s3.accept()
            print('Got connection from', addr3)
        else:
            conn3.send(data.encode())


def sock4(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s4:
        if data == "1":
            s4.bind((HOST, PORT4))
            s4.listen(5)
            global conn4, addr4
            conn4, addr4 = s4.accept()
            print('Got connection from', addr4)
        else:
            conn4.send(data.encode())


def send_data(data, marker):
    message = str(data)
    if marker == 211:
        sock1(message)
    elif marker == 123:
        sock2(message)
    elif marker == 177:
        sock3(message)
    elif marker == 89:
        sock4(message)
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
    if abs(x2 - x1) <= 15:
        if y1 > y2:
            orient = "west"
        elif y2 > y1:
            orient = "east"
    elif (x2 - x1) > 0:     # upright
        if abs(y2 - y1) <= 15:
            orient = "north"
        elif (y2 > y1):
            orient = "ne"
        elif (y1 > y2):
            orient = "nw"
    elif (x2 - x1) < 0:
        if abs(y2 - y1) <= 15:
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
    # north
    elif orient == "north":
        if abs(s1 - d1) <= 15:
            if s2 > d2:
                data = 'for'
            else:
                data = 'rev'
        elif s1 < d1 and abs(s2 - d2) > 15 and s2 > d2:
            data = "frt"
        elif s1 > d1 and abs(s2 - d2) > 15 and s2 > d2:
            data = "flt"
        elif d1 < s1 and abs(s2 - d2) > 15 and d2 > s2:
            data = "blt"
        elif d1 > s1 and abs(s2 - d2) > 15 and d2 > s2:
            data = 'brt'
        elif s1 < d1:
            data = 'rt'
        elif s1 > d1:
            data = 'lt'
    # nw
    elif orient == "nw":
        if s1 > d1 and s2 > d2:
            data = "for"
        elif s1 < d1 and s2 > d2 and abs(s2 - d2) <= 15:
            data = 'rt'
        elif d1 > s1 and d2 > s2:
            data = 'rev'
        elif d1 < s1 and d2 > s2 and abs(s2 - d2) <= 15:
            data = "lt"
        if abs(s1 - d1) <= 15:
            if s2 > d2:
                data = 'flt'
            else:
                data = 'brt'
        elif s1 < d1:
            data = 'blt'
        elif s1 > d1:
            data = 'frt'
    # ne
    elif orient == "ne":
        if s1 < d1 and s2 > d2:
            data = "for"
        elif d1 < s1 and d2 > s2:
            data = "rev"
        elif d1 > s1 and abs(s2 - d2) <= 15 and d2 > s2:
            data = 'rt'
        elif s1 > d1 and abs(s2 - d2) <= 15 and s2 > d2:
            data = "lt"
        elif abs(s1 - d1) <= 15:
            if s2 > d2:
                data = 'frt'
            else:
                data = 'blt'
        elif s1 < d1:
            data = 'brt'
        elif s1 > d1:
            data = 'flt'
    # south
    elif orient == "south":
        if abs(s1 - d1) <= 15:
            if s2 > d2:
                data = 'rev'
            else:
                data = 'for'
        elif s1 < d1 and abs(s2 - d2) > 15 and s2 > d2:
            data = "blt"
        elif s1 > d1 and abs(s2 - d2) > 15 and s2 > d2:
            data = "brt"
        elif d1 < s1 and abs(s2 - d2) > 15 and d2 > s2:
            data = "frt"
        elif d1 > s1 and abs(s2 - d2) > 15 and d2 > s2:
            data = 'flt'
        elif s1 < d1:
            data = 'lt'
        elif s1 > d1:
            data = 'rt'
    # se
    elif orient == "se":
        if s1 < d1 and s2 < d2:
            data = "for"
        elif s1 > d1 and s2 < d2 and abs(s2 - d2) <= 15:
            data = 'rt'
        elif d1 < s1 and d2 < s2:
            data = 'rev'
        elif d1 > s1 and d2 < s2 and abs(s2 - d2) <= 15:
            data = "lt"
        if abs(s1 - d1) <= 15:
            if s2 < d2:
                data = 'flt'
            else:
                data = 'brt'
        elif s1 > d1:
            data = 'blt'
        elif s1 < d1:
            data = 'frt'
    # sw
    elif orient == "sw":
        if s1 > d1 and s2 < d2:
            data = "for"
        elif d1 > s1 and d2 < s2:
            data = "rev"
        elif d1 < s1 and abs(s2 - d2) <= 15 and d2 < s2:
            data = 'rt'
        elif s1 < d1 and abs(s2 - d2) <= 15 and s2 < d2:
            data = "lt"
        elif abs(s1 - d1) <= 15:
            if s2 < d2:
                data = 'frt'
            else:
                data = 'blt'
        elif s1 > d1:
            data = 'brt'
        elif s1 < d1:
            data = 'flt'
    # east
    elif orient == "east":
        if abs(s2 - d2) <= 15:
            if s1 < d1:
                data = 'for'
            else:
                data = 'rev'
        elif s1 < d1 and abs(s2 - d2) > 15 and s2 < d2:
            data = "frt"
        elif s1 < d1 and abs(s2 - d2) > 15 and s2 > d2:
            data = "flt"
        elif d1 < s1 and abs(s2 - d2) > 15 and d2 < s2:
            data = "blt"
        elif d1 < s1 and abs(s2 - d2) > 15 and d2 > s2:
            data = 'brt'
        elif s2 > d2:
            data = 'rt'
        elif s2 < d2:
            data = 'lt'
    # west
    elif orient == "west":
        if abs(s2 - d2) <= 15:
            if s1 < d1:
                data = 'for'
            else:
                data = 'rev'
        elif s1 > d1 and s2 > d2:
            data = "frt"
        elif s1 > d1 and s2 < d2:
            data = "flt"
        elif d1 > s1 and d2 > s2:
            data = "blt"
        elif d1 > s1 and d2 < s2:
            data = 'brt'
        elif s2 < d2:
            data = 'rt'
        elif s2 > d2:
            data = 'lt'
    send_data(data, ids)


t1 = Thread(target=sock1, args=("1",))
t2 = Thread(target=sock2, args=("1",))
t3 = Thread(target=sock3, args=("1",))
t4 = Thread(target=sock4, args=("1",))
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()
cap = cv2.VideoCapture(2)
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
