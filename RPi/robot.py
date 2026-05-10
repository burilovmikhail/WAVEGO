#!/usr/bin/env/python3
# File name   : robot.py
# Description : Robot interfaces.
import os
import time
import json
import threading
import serial

_SERIAL_PORT = next((p for p in ('/dev/serial0', '/dev/ttyAMA0', '/dev/ttyS0') if os.path.exists(p)), '/dev/ttyS0')
print(f'[serial] opening {_SERIAL_PORT}')
ser = serial.Serial(_SERIAL_PORT, 115200)
print(f'[serial] opened: {ser}')

def _serial_reader():
    while True:
        try:
            line = ser.readline()
            if line:
                print(f'[serial] << {line}')
        except Exception as e:
            print(f'[serial] read error: {e}')

threading.Thread(target=_serial_reader, daemon=True).start()
dataCMD = json.dumps({'var':"", 'val':0, 'ip':""})
upperGlobalIP = 'UPPER IP'


def _send(cmd):
    data = json.dumps(cmd).encode()
    print(f'[serial] >> {data}')
    try:
        ser.write(data)
    except Exception as e:
        print(f'[serial] write error: {e}')


pitch, roll = 0, 0


def setUpperIP(ipInput):
	global upperGlobalIP
	upperGlobalIP = ipInput

def forward(speed=100):
	_send({'var': "move", 'val': 1})
	print('robot-forward')

def backward(speed=100):
	_send({'var': "move", 'val': 5})
	print('robot-backward')

def left(speed=100):
	_send({'var': "move", 'val': 2})
	print('robot-left')

def right(speed=100):
	_send({'var': "move", 'val': 4})
	print('robot-right')

def stopLR():
	_send({'var': "move", 'val': 6})
	print('robot-stop')

def stopFB():
	_send({'var': "move", 'val': 3})
	print('robot-stop')

def lookUp():
	_send({'var': "ges", 'val': 1})
	print('robot-lookUp')

def lookDown():
	_send({'var': "ges", 'val': 2})
	print('robot-lookDown')

def lookStopUD():
	_send({'var': "ges", 'val': 3})
	print('robot-lookStopUD')

def lookLeft():
	_send({'var': "ges", 'val': 4})
	print('robot-lookLeft')

def lookRight():
	_send({'var': "ges", 'val': 5})
	print('robot-lookRight')

def lookStopLR():
	_send({'var': "ges", 'val': 6})
	print('robot-lookStopLR')

def steadyMode():
	_send({'var': "funcMode", 'val': 1})
	print('robot-steady')

def jump():
	_send({'var': "funcMode", 'val': 4})
	print('robot-jump')

def handShake():
	_send({'var': "funcMode", 'val': 3})
	print('robot-handshake')



def lightCtrl(colorName, cmdInput):
	colorNum = 0
	if colorName == 'off':
		colorNum = 0
	elif colorName == 'blue':
		colorNum = 1
	elif colorName == 'red':
		colorNum = 2
	elif colorName == 'green':
		colorNum = 3
	elif colorName == 'yellow':
		colorNum = 4
	elif colorName == 'cyan':
		colorNum = 5
	elif colorName == 'magenta':
		colorNum = 6
	elif colorName == 'cyber':
		colorNum = 7
	_send({'var': "light", 'val': colorNum})


def buzzerCtrl(buzzerCtrl, cmdInput):
	_send({'var': "buzzer", 'val': buzzerCtrl})



if __name__ == '__main__':
    # robotCtrl.moveStart(100, 'forward', 'no', 0)
    # time.sleep(3)
    # robotCtrl.moveStop()
    while 1:
        time.sleep(1)
        pass