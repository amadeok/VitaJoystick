import vgamepad as vg
import pyautogui
from time import sleep
gamepad = vg.VX360Gamepad()
sleep(5)
while 1:
    for btn in vg.XUSB_BUTTON:
        print(btn)
        sleep(1)
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        sleep(0.050)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        #gamepad.left_joystick_float(0, 1800) 
        #gamepad.right_joystick_float(1800, 0) 
        #gamepad.update() 
        sleep(1)
