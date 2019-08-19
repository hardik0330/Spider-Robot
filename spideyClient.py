import socket
import network
import machine

pin1 = machine.Pin(14, machine.Pin.OUT)  #D5
pin2 = machine.Pin(12, machine.Pin.OUT)  #D6
pin3 = machine.Pin(13, machine.Pin.OUT)  #D7

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

sta_if.connect('A30', '123456789')
s = socket.socket()
port = 8081
i = 0
s.connect(('192.168.43.117', port))
while True:
    data = s.recv(1024).decode()
    print(data)
    if data == 'for':
        pin1.value(0)
        pin2.value(0)
        pin3.value(0)
    elif data == 'frt':
        pin1.value(0)
        pin2.value(0)
        pin3.value(1)
    elif data == 'rt':
        pin1.value(0)
        pin2.value(1)
        pin3.value(0)
    elif data == 'brt':
        pin1.value(0)
        pin2.value(1)
        pin3.value(1)
    elif data == 'back':
        pin1.value(1)
        pin2.value(0)
        pin3.value(0)
    elif data == 'bleft':
        pin1.value(1)
        pin2.value(0)
        pin3.value(1)
    elif data == 'lt':
        pin1.value(1)
        pin2.value(1)
        pin3.value(0)
    elif data == 'flt':
        pin1.value(1)
        pin2.value(1)
        pin3.value(1)
    if not data:
        break
s.close()    
print("close")
