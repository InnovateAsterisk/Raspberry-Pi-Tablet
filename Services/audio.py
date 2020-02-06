# Handles the Volume Up/down and the Headphone Jack
# =================================================


import RPi.GPIO as GPIO
import sys
import time
import os
import alsaaudio

# print alsaaudio.cards()        # If we uninstall the primary card, this list is empty
# print alsaaudio.mixers() # [Master][Capture]
MasterMixer = alsaaudio.Mixer("Master")

IS_JACK_IN = False      # If the headphone jack is n use
VOL_UP_GPIO_PIN = 24    # The GPIO pin (BCM) for Volume Up (Green)
VOL_DOWN_GPIO_PIN = 23  # The GPIO pin (BCM) for Volume Down (Yellow)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(VOL_UP_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(VOL_DOWN_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def IncreaseVolume():
    # Get the current volume
    v = MasterMixer.getvolume()[0]
    if v >= 100:
        print("Max Volume!")
        return
    else:
        if v > 95: v = 95
        print("Increase Volume from "+ str(v) +" to "+ str(v+5) +"")
        MasterMixer.setvolume(v+5) 
        return

def DecreaseVolume():
    # Get the current volume
    v = MasterMixer.getvolume()[0]
    if v <= 0:
        print("Min Volume!")
        return
    else:
        if v < 5: v = 5
        print("Decrease Volume from "+ str(v)  +" to "+ str(v-5) +"")
        MasterMixer.setvolume(v-5)
        return

def button_volume(pin):
    # Check if muted, and if so, unmute
    if MasterMixer.getmute()[0]: 
        print("Unmuted")
        MasterMixer.setmute(0)

    # Identify Direction
    if pin == VOL_UP_GPIO_PIN:
        IncreaseVolume()
    elif pin == VOL_DOWN_GPIO_PIN:
        DecreaseVolume()
    else:
        print("Unknown PIN")

GPIO.add_event_detect(VOL_UP_GPIO_PIN, GPIO.FALLING, callback=button_volume, bouncetime=1000)
GPIO.add_event_detect(VOL_DOWN_GPIO_PIN, GPIO.FALLING, callback=button_volume, bouncetime=1000)

while True: # Run forever
    # Mute
    if (GPIO.input(VOL_UP_GPIO_PIN) == False and GPIO.input(VOL_DOWN_GPIO_PIN) == False):
        if MasterMixer.getmute()[0] == False:
            MasterMixer.setmute(1)
            print("Mute Active, press either volume up or down to unmute")
        else:
            print("Mute already active")
    else:
        # Vol Up
        if GPIO.input(VOL_UP_GPIO_PIN) == False:
            IncreaseVolume()
        # Vol Down
        if GPIO.input(VOL_DOWN_GPIO_PIN) == False:
            DecreaseVolume()

    # Slow
    time.sleep(0.1)