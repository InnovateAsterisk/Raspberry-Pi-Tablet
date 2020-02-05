# Handles the fan speed according to the CPU temperature
# ======================================================

import RPi.GPIO as GPIO
import sys
import time
import os

# Program variables
PWM_GPIO_PIN = 27	# The GPIO pin wired to the Mosfet Transistor
PWM_FREQUENCY = 50	# The PWN frequency (Don't change this, change the Duty Cycle)
DUTY_CYCLE = 0 		# values between 0 and 100 to control fan speed

#temperatures levels
TEMP_LV_1 = 30  	# Off
TEMP_LV_2 = 40		# 25%
TEMP_LV_3 = 50		# 50%
TEMP_LV_4 = 60		# 75%

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_GPIO_PIN, GPIO.OUT)
pwmOut = GPIO.PWM(PWM_GPIO_PIN, PWM_FREQUENCY)
pwmOut.start(DUTY_CYCLE)


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
	if CPU_temp > TEMP_LV_1 and CPU_temp <= TEMP_LV_2: DUTY_CYCLE = 25
	if CPU_temp > TEMP_LV_2 and CPU_temp <= TEMP_LV_3: DUTY_CYCLE = 50
	if CPU_temp > TEMP_LV_3 and CPU_temp <= TEMP_LV_4: DUTY_CYCLE = 75
	if CPU_temp > TEMP_LV_4: DUTY_CYCLE = 100

# Main program loop
# =================
while True:
	try:
		ControlFan()
		if(DUTY_CYCLE <= 0): DUTY_CYCLE = 0
		if(DUTY_CYCLE >= 100): DUTY_CYCLE = 100
		pwmOut.ChangeDutyCycle(DUTY_CYCLE)

	except:
		print("Error setting fan speed")
	time.sleep(2)

# Unreachable
# ===========
GPIO.cleanup()