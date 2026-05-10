#!/usr/bin/python3
# File name   : setup.py for WAVEGO
# Date        : 2022/1/5

import os
import time
import re

curpath = os.path.realpath(__file__)
thisPath = os.path.dirname(curpath)
venvPip = thisPath + '/venv/bin/pip'
venvPython = thisPath + '/venv/bin/python3'
CONFIG_TXT = '/boot/firmware/config.txt' if os.path.exists(
    '/boot/firmware/config.txt') else '/boot/config.txt'
CMDLINE_TXT = '/boot/firmware/cmdline.txt' if os.path.exists(
    '/boot/firmware/cmdline.txt') else CMDLINE_TXT


def replace_num(file, initial, new_num):
    newline = ""
    str_num = str(new_num)
    with open(file, "r") as f:
        for line in f.readlines():
            if line.find(initial) == 0:
                line = str_num + '\n'
            newline += line
    with open(file, "w") as f:
        f.writelines(newline)


def exec_with_retries(*commands, retries=3):
    for _ in range(retries):
        for cmd in commands:
            if os.system(cmd) == 0:
                return


exec_with_retries("sudo apt update")
exec_with_retries("sudo apt upgrade")
exec_with_retries("sudo apt clean")
exec_with_retries(
    "sudo apt-get install -y python3-pip python3-venv libfreetype6-dev libjpeg-dev build-essential")  # python-dev?
exec_with_retries("sudo apt-get install -y i2c-tools")
exec_with_retries("sudo apt-get install -y python3-smbus")
# exec_with_retries("sudo apt-get -y install libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev")  # ???

os.system("python3 -m venv " + thisPath + "/venv")

exec_with_retries(venvPip + " install -U pip")
exec_with_retries(venvPip + " install pyserial")
exec_with_retries(venvPip + " install flask")
exec_with_retries(venvPip + " install flask_cors")
exec_with_retries(venvPip + " install websockets")

try:
    replace_num(CONFIG_TXT, '[all]',
                '[all]\nenable_uart=1\ngpu_mem=128')
except:
    print('try again')

try:
    replace_num(CONFIG_TXT, 'camera_auto_detect=1',
                '#camera_auto_detect=1\nstart_x=1')
except:
    print('try again')

try:
    replace_num(CONFIG_TXT, 'camera_auto_detect=1',
                '#camera_auto_detect=1')
except:
    print('try again')

CMDLINE_FILE = open(CMDLINE_TXT, 'r')
OLD_LINES = CMDLINE_FILE.readlines()
CMDLINE_FILE.close()

CMDLINE_FILE = open(CMDLINE_TXT, 'w+')
for EACH_LINE in OLD_LINES:
    NEW_LINES = re.sub('console=serial0,115200', '', EACH_LINE)
    CMDLINE_FILE.writelines(NEW_LINES)
CMDLINE_FILE.close()

# ??? ==3.4.11.45
exec_with_retries(venvPip + " install opencv-contrib-python")
exec_with_retries(venvPip + " install opencv-python")
# exec_with_retries(venvPip + " uninstall -y numpy") # ???
exec_with_retries(venvPip + " install numpy")  # ==1.21
exec_with_retries(venvPip + " install imutils zmq pybase64 psutil")

exec_with_retries(
    "sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq")
exec_with_retries("cd " + thisPath +
                  " && cd .. && sudo git clone https://github.com/oblique/create_ap")

try:
    os.system("cd " + thisPath +
              " && cd .. && cd create_ap && sudo make install")
except:
    pass

init_script = """#!/bin/sh
### BEGIN INIT INFO
# Provides:          wavego-server
# Required-Start:    $remote_fs $syslog $network
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: WAVEGO web server
### END INIT INFO
cd {path} && {python} webServer.py &
""".format(path=thisPath, python=venvPython)

with open('/tmp/wavego-server', 'w') as f:
    f.write(init_script)
os.system("sudo mv /tmp/wavego-server /etc/init.d/wavego-server")
os.system("sudo chmod +x /etc/init.d/wavego-server")
os.system("sudo update-rc.d wavego-server defaults")

print('Completed!')

os.system("sudo reboot")
