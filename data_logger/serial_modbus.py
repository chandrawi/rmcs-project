import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import serial
import time
import config

# Get gateway ID from input argument and corresponding configurations from config file
invalid = True
if len(config.GATEWAY_MODBUS) > 0:
    gateway_id = next(iter(config.GATEWAY_MODBUS))
    if len(sys.argv) > 1:
        gateway_id = sys.argv[1] if sys.argv[1] in config.GATEWAY_MODBUS else gateway_id
    GATEWAY = config.GATEWAY_MODBUS[gateway_id]
    if all(k in GATEWAY for k in ("serial_port", "period_time")):
        invalid = False
if invalid:
    raise Exception("Gateway ID input is missing, invalid format, or invalid gateway configuration")

ser = serial.Serial(GATEWAY['serial_port'], 9600, timeout=1)

# SCL3300 inclinometer X, Y, Z inclination with 0x01 and 0x02 addresses
print("SCL3300 inclinometer")
commands = [
    b"\x01\x04\x00\x04\x00\x04\xB0\x08",
    b"\x02\x04\x00\x04\x00\x04\xB0\x3B",
    b"\x03\x04\x00\x04\x00\x04\xB1\xEA",
    b"\x04\x04\x00\x04\x00\x04\xB0\x5D"
]
for i, command in enumerate(commands):
    ser.write(command)
    s = ser.read(13)
    angle_x = s[3] * 2**8 + s[4]
    angle_y = s[5] * 2**8 + s[6]
    angle_z = s[7] * 2**8 + s[8]
    if angle_x >= 2**15 : angle_x = angle_x - 2**16
    if angle_y >= 2**15 : angle_y = angle_y - 2**16
    if angle_z >= 2**15 : angle_z = angle_z - 2**16
    print("    Angle {0:1d} (X|Y|Z): {1:5d} | {2:5d} | {3:5d}".format(i, angle_x, angle_y, angle_z))

# Soil inclinometer X, Y, and Z acceleration with 0x01 to 0x05 addresses
print("Soil Inclinometer")
commands = [
    b"\x01\x04\x00\x00\x00\x03\xB0\x0B",
    b"\x02\x04\x00\x00\x00\x03\xB0\x38",
    b"\x03\x04\x00\x00\x00\x03\xB1\xE9",
    b"\x04\x04\x00\x00\x00\x03\xB0\x5E",
    b"\x05\x04\x00\x00\x00\x03\xB1\x8F"
]
for i, command in enumerate(commands):
    ser.write(command)
    s = ser.read(11)
    accel_x = s[3] * 2**8 + s[4]
    accel_y = s[5] * 2**8 + s[6]
    accel_z = s[7] * 2**8 + s[8]
    if accel_x >= 2**15 : accel_x = accel_x - 2**16
    if accel_y >= 2**15 : accel_y = accel_y - 2**16
    if accel_z >= 2**15 : accel_z = accel_z - 2**16
    print("    Acceleration {0:1d} (X|Y|Z): {1:5d} | {2:5d} | {3:5d}".format(i, accel_x, accel_y, accel_z))

# HPT64 Piezometer pressure and level with 0x80 address 
ser.write(b"\x80\x04\x00\x10\x00\x06\x6F\xDC")
s = ser.read(17)
pressure = s[3] * 2**24 + s[4] * 2**16 + s[5] * 2**8 + s[6]
level = s[9] * 2**24 + s[10] * 2**16 + s[11] * 2**8 + s[12]
if pressure >= 2**31 : pressure = pressure - 2**32
if level >= 2**31 : level = level - 2**32
print("Piezometer")
print("    Pressure: {}".format(pressure))
print("    Level   : {}".format(level))

# RD-RGPBR-RS485 Rain gauge Rain Enquiry 10 bytes length with 0x90 address
time.sleep(0.02)
ser.write(b"\x90\x03\x00\x00\x00\x0A\xD9\x4C")
s = ser.read(25)
rain_yesterday = s[7] * 2**8 + s[8]
rain_today = s[3] * 2**8 + s[4]
rain_last_hour = s[13] * 2**8 + s[14]
rain_hourly = s[11] * 2**8 + s[12]
print("Rain Gauge")
print("    Yesterday Rainfall: {}".format(rain_yesterday))
print("    Today Rainfall    : {}".format(rain_today))
print("    Last Hour Rainfall: {}".format(rain_last_hour))
print("    Hourly Rainfall   : {}".format(rain_hourly))
