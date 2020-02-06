# Handles the fan speed according to the CPU temperature
# ======================================================

import RPi.GPIO as GPIO
import sys
import time
import os

# Program variables
PWM_GPIO_PIN = 12       # The GPIO pin wired to the Mosfet Transistor
PWM_FREQUENCY = 50      # The PWN frequency (Don't change this, change the Duty Cycle)
DUTY_CYCLE = 0          # values between 0 and 100 to control fan speed

#temperatures levels
TEMP_LV_1 = 50          # Off (The typical opperating temerature)
TEMP_LV_2 = 60          # L1 - L2 = 60%
TEMP_LV_3 = 70          # L2 - L3 = 70%
TEMP_LV_4 = 75          # L3 - L4 = 80% (The official operating temperature limit is 85c)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_GPIO_PIN, GPIO.OUT)
pwmOut = GPIO.PWM(PWM_GPIO_PIN, PWM_FREQUENCY)

# Methods
# =======
def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        temp = (res.replace("temp=","").replace("'C\n",""))
        return float(temp)

def ControlFan():
        global DUTY_CYCLE

        CPU_temp = getCPUtemperature()

        if CPU_temp <= TEMP_LV_1: DUTY_CYCLE = 0
        if CPU_temp > TEMP_LV_1 and CPU_temp <= TEMP_LV_2: DUTY_CYCLE = 60
        if CPU_temp > TEMP_LV_2 and CPU_temp <= TEMP_LV_3: DUTY_CYCLE = 70
        if CPU_temp > TEMP_LV_3 and CPU_temp <= TEMP_LV_4: DUTY_CYCLE = 80
        if CPU_temp > TEMP_LV_4: DUTY_CYCLE = 100

        print("Temerature is: "+ str(CPU_temp) +", setting Fan to: "+ str(DUTY_CYCLE))

# Main program loop
# =================
pwmOut.start(DUTY_CYCLE)
while True:
        try:
                ControlFan()
                if(DUTY_CYCLE <= 0): DUTY_CYCLE = 0
                if(DUTY_CYCLE >= 100): DUTY_CYCLE = 100
                # print("Setting Fan to: "+ DUTY_CYCLE)
                pwmOut.ChangeDutyCycle(DUTY_CYCLE)

        except:
                print("Error setting fan speed")
        time.sleep(2)

# Unreachable
# ===========
pwmOut.stop()
GPIO.cleanup()