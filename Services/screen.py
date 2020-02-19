# Handles screen rotation using the Gyro
# ======================================

import smbus
import math
import time
import os

address = 0x69       # via i2cdetect (default is 68)

# Register https://www.i2cdevlib.com/devices/mpu6050#registers
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

# Pre-defined ranges
ACCEL_RANGE_2G = 0x00
ACCEL_RANGE_4G = 0x08
ACCEL_RANGE_8G = 0x10
ACCEL_RANGE_16G = 0x18

GYRO_RANGE_250DEG = 0x00
GYRO_RANGE_500DEG = 0x08
GYRO_RANGE_1000DEG = 0x10
GYRO_RANGE_2000DEG = 0x18

# Scale Modifiers
ACCEL_SCALE_MODIFIER_2G = 16384.0
ACCEL_SCALE_MODIFIER_4G = 8192.0
ACCEL_SCALE_MODIFIER_8G = 4096.0
ACCEL_SCALE_MODIFIER_16G = 2048.0

GYRO_SCALE_MODIFIER_250DEG = 131.0
GYRO_SCALE_MODIFIER_500DEG = 65.5
GYRO_SCALE_MODIFIER_1000DEG = 32.8
GYRO_SCALE_MODIFIER_2000DEG = 16.4

# Construct a SMBus
bus = smbus.SMBus(1)
bus.write_byte_data(address, PWR_MGMT_1, 0x00)
bus.write_byte_data(address, ACCEL_CONFIG, ACCEL_RANGE_2G)
bus.write_byte_data(address, GYRO_CONFIG, GYRO_RANGE_250DEG)

def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000): # -32768 +32768 
        return -((65535 - val) + 1)
    else:
        return val

def get_y_rotation(x,y,z):
    radians = math.atan2(x, math.sqrt((y*y)+(z*z)))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, math.sqrt((x*x)+(z*z)))
    return math.degrees(radians)

# ==============================

rotation = ""
while True:
        AX = []
        AY = []
        AZ = []
        for i in range(10):
                ax = 0
                ay = 0
                az = 0

                try:
                        ax = read_word_2c(ACCEL_XOUT_H) / ACCEL_SCALE_MODIFIER_2G
                        ay = read_word_2c(ACCEL_YOUT_H) / ACCEL_SCALE_MODIFIER_2G
                        az = read_word_2c(ACCEL_ZOUT_H) / ACCEL_SCALE_MODIFIER_2G
                except:
                        print("Error getting rotation")

                AX.append(ax)
                AY.append(ay)
                AZ.append(az)

                time.sleep(0.1)

        avg_x = sum(AX)/len(AX)
        avg_y = sum(AY)/len(AY)
        avg_z = sum(AZ)/len(AZ)

        r = round(get_y_rotation(avg_x, avg_y, avg_z))

        if r >= -20 and r <= 20:
                # Normal
                if(rotation != "normal"):
                        rotation = "normal"
                        print("Screen Rotate: Normal")
                        os.popen("xrandr -display :0.0 --output DSI-1 --rotate normal")
                        os.popen("DISPLAY=:0 xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 0 0 0 0 0 0 0 0")
        elif r < -20:
                # You rotate Left (Set Screen to Right)
                if(rotation != "left"):
                        rotation = "left"
                        print("Screen Rotate Left")
                        os.popen("xrandr -display :0.0 --output DSI-1 --rotate right")
                        os.popen("DISPLAY=:0 xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1")
        elif r > 20:
                # You rotate Right (Set Screen Left)
                if(rotation != "right"):
                        rotation = "right"
                        print("Screen Rotate Right")
                        os.popen("xrandr -display :0.0 --output DSI-1 --rotate left")
                        os.popen("DISPLAY=:0 xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 -1 1 1 0 0 0 0 1")
        else: 
                # Rotate 180
                if(rotation != "inverted"):
                        rotation = "inverted"
                        print("Rotate 180")
                        os.popen("xrandr -display :0.0 --output DSI-1 --rotate inverted")
                        os.popen("DISPLAY=:0 xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' -1 0 1 0 -1 1 0 0 1")


