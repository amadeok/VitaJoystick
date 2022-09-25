# VitaJoystick

This repository contains the source for programming a esp32 development board to act as a xbox joystick by reading and sending the values of an ordinary joystick via wifi to a pc which then uses them to emulate an xbox joystick.

To program the esp32 you need to:
- Download Arduino IDE
- Install the ESP32 library into the Arduino IDE
- Specify the wifi ssid and password that the board will connect to in wjoystick.ino (line 26 and 27)
- Flash the esp32 board with the sketch wjoystick.ino
- The board will connect to the wifi automatically, then check the serial port to see which IP address the board gets, and write down the ip address

Then you have to run the pc program that will receive the data and emulate the joystick:
- install python
- install the dependecies: (open a command prompt and type: pip install vgamepad keyboard pywin32 pyautogui)
- open settings.ini and write the ip address you got earlier in the "dev board ip address" field
- open command prompt on same folder of wjoystick.py and type: python wjoystick.py
