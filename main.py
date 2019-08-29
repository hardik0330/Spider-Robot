import cv2
import cv2.aruco
import numpy as np
import sys
# import pygame
import time
import serial
from threading import Thread
ser1 = serial.Serial('/dev/ttyACM0', 9600)
ser2 = serial.Serial('/dev/ttyACM1', 9600)


# alpha-100  beta-150
def direction(img, top_left, top_right, centre, ids):
    x1 = top_left[0]
    y1 = top_left[1]
    x2 = top_right[0]
    y2 = top_right[1]
    s1 = (x1 + x2) / 2
    s2 = (y1 + y2) / 2
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
    return orient


def radio1(data, ids):
    if ids == 100:
        if data == 'for':
            print("forward")
            ser1.write('w'.encode())
        if data == 'lt':
            print("left")
            ser1.write('a'.encode())
        if data == 'rev':
            print("reverse")
            ser1.write('s'.encode())
        if data == 'rt':
            print("right")
            ser1.write('d'.encode())
        if data == 'z':
            sys.exit()
        if data == 'c':
            print("not pressed")
            ser1.write('q'.encode())
        time.sleep(0.1)


def radio2(data, ids):
    if ids == 150:
        if data == 'for':
            print("forward")
            ser2.write('w'.encode())
        if data == 'lt':
            print("left")
            ser2.write('a'.encode())
        if data == 'rev':
            print("reverse")
            ser2.write('s'.encode())
        if data == 'rt':
            print("right")
            ser2.write('d'.encode())
        if data == 'z':
            sys.exit()
        if data == 'c':
            print("not pressed")
            ser2.write('q'.encode())
        time.sleep(0.1)


def send_radio(data, ids):
    t1 = Thread(target=radio1, args=(data, ids))
    t2 = Thread(target=radio2, args=(data, ids))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def orientation(img, top_left, top_right, centre, ids):
    x1 = top_left[0]
    y1 = top_left[1]
    x2 = top_right[0]
    y2 = top_right[1]
    s1 = (x1 + x2) / 2
    s2 = (y1 + y2) / 2
    data = 'for'
    # centre1 = centre[0]
    # centre2 = centre[1]
    # destination coord
    d1 = 250.0
    d2 = 250.0
    orient = ""

    if abs(s1 - d1) <= 15 and abs(s2 - d2) <= 15:
        data = 'c'
    # north
    # orient = direction(img, top_left, top_right, centre, ids)
    if direction(img, top_left, top_right, centre, ids) == "north":
    	send_radio('c', ids)
    else:
        direc = direction(img, top_left, top_right, centre, ids)
        while direc != 'north':
            print("Stuck in loop")
            send_radio('rt', ids)
            send_radio('c', ids)
            direc = direction(img, top_left, top_right, centre, ids)
            break
        send_radio('c', ids)
    # send_radio(data, ids)



if __name__=='__main__':
    cap = cv2.VideoCapture(2)
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    while True:
        ret, frame = cap.read()
        # getting all the values in different variables
        corners, ids, rejected = cv2.aruco.detectMarkers(frame, dictionary)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        # createGrid(frame)
        cv2.imshow('out', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if len(corners) > 0:
            # draw only if aruco detected
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
                    # orient north and move
                    orientation(frame, corners[0][0][0], corners[0][0][1], pos, ids[i])
                i = i + 1
            print("\n")
        # cv2.imshow('out', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()
