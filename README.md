# Raspberry-Pi-Tablet
For the moment, this project contains pictures of the First attempt.

![Image of Raspberry Pi Tablet](https://github.com/InnovateAsterisk/Raspberry-Pi-Tablet/blob/master/V1/Pictures/IMG_2949.jpg)

## Project Goals
To develop a 3D printable, Raspberry Pi based tablet. All parts (components) must be easy to obtain and readily available. It must have a battery, and it must be the primary source of power (meaning, it will charge up with a cable plugged in, but must have enough power to run without it.) It must be able to opperate perfect fine without a keyboard (meaning, everything in the user interface should work without an issue even if you dont have a keyboard and mouse plugged in.)

## Version 1
- **SBC :** Raspberry Pi version 4B+
- **Display :** 7 inch LCD Display (with touch)
- **Power Supply :** PiJuice UPS (with battery) - right now it's a small underpowered battery - this may need to change.
- **Camera :** Official Raspberry Pi 1080p Camera (front-facing)
- **Sound & Speakers:** Waveshare Audio HAT - powers 2 speakers, and 2 microphones, and provides an audio jack for headphones.
- **Accelerometer:** MPU-6050 Gyro - to orientate the screen. (with python)
- **Cooling:** Fan (inside the red box/tube) connected to a Mosfet fan-speed controller (speed is controlled in python)
- **USB:** Breakout USB (not currently connected)
- **Buttons:**
  - Power Button
  - Volume Up/Down rocker
- **LEDs**
  - Charge
  - Power and activity LED light is redirected (using nylon) to the case.
- **Backplate:** Bamboo wood back, with laser etched decal