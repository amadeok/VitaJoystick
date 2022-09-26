import vgamepad as vg
from time import sleep
import socket
import time
import msvcrt
import keyboard, win32gui, win32com, win32com.client, win32con, pyautogui
pyautogui.PAUSE = 0
import configparser, os
import threading
from enum import Enum

## DISABLE MIC BUTTON IN VR CHAT SETTINGS

def callback(hwnd, joystick):
    winname = win32gui.GetWindowText(hwnd)
    if "vrchat" == winname.lower():
        print("VR chat Window found %s:" % win32gui.GetWindowText(hwnd))
        joystick.vr_chat_handle = hwnd


gamepad = vg.VX360Gamepad()


def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

class Map(Enum):
     left_x = 1
     left_y = 2
     right_x = 3
     right_y = 4

class wireless_joy():

    def read_conf_file(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.HOST = config['SETTINGS']["dev board ip address"]
        FocusVRCHAT = config['SETTINGS']['Focus VRChat window']
        if (FocusVRCHAT.lower() == "yes" or FocusVRCHAT == "true" or FocusVRCHAT == "1"):
            self.focus_vrchat_window =  True
        else: 
            self.focus_vrchat_window =   False
        self.max_x = int(config['CALIBRATION']['max_x'])
        self.max_y = int(config['CALIBRATION']['max_y'])
        self.min_x = int(config['CALIBRATION']['min_x'])
        self.min_y = int(config['CALIBRATION']['min_y'])
        self.axis1_mapping = Map[config['SETTINGS']["Axis 1 Mapping"]]
        self.axis2_mapping = Map[config['SETTINGS']["Axis 2 Mapping"]]

        self.pattern_key_press =  config['SETTINGS']['pattern key to press']

    def __init__(self) -> None:
        pass
        self.data = bytearray(8)
        self.joy_1 = 1800
        self.joy_2 = 1800
        self.switch_count = 0
        self.switcher = 0
        self.lastExtremeTimes = [float(0) for x in range(3)]
        self.milisecondsWindow = 0.5
        self.buttonDelay = 0.0200
        self.extreme_threshold = 0.8
        #thread1 = threading.Thread(target=self.key_lisesnt, args=())
        #thread1.start()
        self.vr_chat_handle = 0
        self.focus_vrchat_window = True
        win32gui.EnumWindows(callback, self)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        self.HOST = "192.168.1.0"  # The server's hostname or IP address
        self.PORT = 3333  # The port used by the server

        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0
        self.pattern_key_presss = " "
        self.axis1_mapping = ""
        self.axis2_mapping = ""

        if not os.path.isfile("settings.ini"):
            config = configparser.ConfigParser()

            config['SETTINGS'] = {'Dev Board Ip Address': '192.168.1.91',
                      'Focus VRChat window': 'true', 'pattern key to press': 'esc',
                      "Axis 1 Mapping": "right_x", "Axis 2 Mapping": "right_y"
                      }
            config['CALIBRATION'] = {'max_x': '3220',
                      'max_y': '3000', 'min_x': '586', 'min_y': '613'
                      }
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            self.read_conf_file()
        else:
            self.read_conf_file()
        
    def key_lisesnt(self):
        while 1:
            x = msvcrt.getch().decode('UTF-8')
                
            if x == 'q' or x == 'Q':
                exit()
            elif x == "1":
                self.buttonDelay+=0.005
                print("button delay: ", self.buttonDelay)
            elif x == "2":
                self.buttonDelay-=0.005
                print("button delay: ", self.buttonDelay)
            if self.buttonDelay < 0: self.buttonDelay = 0

    def focus_vrchat(self):
        print("\nFocusing VRchat window")
        rect = win32gui.GetWindowRect(self.vr_chat_handle)
        win32gui.ShowWindow(self.vr_chat_handle, win32con.SW_MAXIMIZE)
        pyautogui.click(rect[0] + 30, rect[1] + 30)
        win32gui.SetForegroundWindow(self.vr_chat_handle)

    def patter_detect(self):
        condition = False;

        if self.switcher == -1:
            condition = self.joy_1 > self.extreme_threshold or  self.joy_1 < -self.extreme_threshold;
        elif self.switcher:
            condition = self.joy_1 > self.extreme_threshold ; # top
        else:
            condition = self.joy_1 < -self.extreme_threshold; # bottom

        if condition: 
  
            self.switch_count+=1

            if self.joy_1 > self.extreme_threshold:
                self.switcher = 0
                print(self.switch_count, "Pattern up ")

            elif self.joy_1 < -self.extreme_threshold:
                self.switcher = 1
                print(self.switch_count, "Pattern down ")

            self.lastExtremeTimes[0] = self.lastExtremeTimes[1];
            self.lastExtremeTimes[1] = self.lastExtremeTimes[2];
            self.lastExtremeTimes[2] = time.time()
            if self.lastExtremeTimes[2] - self.lastExtremeTimes[0] < self.milisecondsWindow  and self.switch_count >= 3:
            
                print(self.switch_count, " Pattern triggered \n")

                self.switch_count = 0;
                gamepad.left_joystick_float(1800, 1800) 
                gamepad.update() 
                sleep(0.2)
                #gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
                #gamepad.update() 

                #sleep(self.buttonDelay);
                #gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
                #gamepad.left_joystick_float(1800, 1800) 
                #gamepad.update() 
                if self.focus_vrchat_window:
                    try:       
                        self.focus_vrchat()
                    except Exception as e:
                        win32gui.EnumWindows(callback, self)
                        try:
                            self.focus_vrchat()
                        except:
                            print("failed to get vr chat window, is it running?")
                            #pyautogui.click(50, 50)


                keyboard.press(self.pattern_key_press)
                sleep(self.buttonDelay);
                keyboard.release(self.pattern_key_press)


        if time.time() - self.lastExtremeTimes[2] >= self.milisecondsWindow:
            self.switch_count = 0
            if self.switcher != -1:
                print("")
                self.switcher = -1
  

    def main_loop(self):
        print("Main Loop")
        n = 0
        while 1:
            try:
                ret = self.s.recv_into(self.data, 8)
            except:
                print("Wifi transfer failed, restarting")
                return -1
            if ret == -1:
                break
            x = int.from_bytes(self.data[0:4], "little")
            y = int.from_bytes(self.data[4:8], "little")
            # if x > self.max_x: self.max_x = x
            # if y > self.max_y: self.max_y = y
            # if x < self.min_x: self.min_x = x
            # if y < self.min_y: self.min_y = y
            # s.send(self.data)

            self.joy_1 = scale(x, (self.min_x, self.max_x), (-1.0, +1.0))

            self.joy_2 = scale(y, (self.max_y, self.min_y), (-1.0, +1.0))
            self.patter_detect()

            if self.joy_1 < -1: self.joy_1 = -1
            elif self.joy_1 > 1: self.joy_1 = 1
            if self.joy_2 < -1: self.joy_2 = -1
            elif self.joy_2 > 1: self.joy_2 = 1

            final_x = 0
            final_y = 0

            if self.axis1_mapping == Map.right_x and self.axis2_mapping == Map.right_y:
                gamepad.right_joystick_float(self.joy_1, self.joy_2) 
            elif self.axis1_mapping == Map.right_y and self.axis2_mapping == Map.right_x:
                gamepad.right_joystick_float(self.joy_2, self.joy_1) 
            elif self.axis1_mapping == Map.left_x and self.axis2_mapping == Map.left_y:
                gamepad.left_joystick_float(self.joy_1, self.joy_2) 
            elif self.axis1_mapping == Map.left_y and self.axis2_mapping == Map.left_x:
                gamepad.left_joystick_float(self.joy_2, self.joy_1) 

            elif self.axis1_mapping == Map.right_x and self.axis2_mapping == Map.left_y:
                gamepad.right_joystick_float(self.joy_1, 0) 
                gamepad.left_joystick_float(0, self.joy_2) 
            elif self.axis1_mapping == Map.right_y and self.axis2_mapping == Map.left_x:
                gamepad.right_joystick_float(0, self.joy_1) 
                gamepad.left_joystick_float(self.joy_2, 0) 

            elif self.axis1_mapping == Map.left_x and self.axis2_mapping == Map.right_y:
                gamepad.left_joystick_float(self.joy_1, 0) 
                gamepad.right_joystick_float(0, self.joy_2) 
            elif self.axis1_mapping == Map.left_y and self.axis2_mapping == Map.right_x:
                gamepad.left_joystick_float(0, self.joy_1) 
                gamepad.right_joystick_float(self.joy_2, 0) 
                
            gamepad.update() 

            #print(x, y, self.joy_1, self.joy_2, self.data)
            #print(str(self.joy_1)[0:4], str(self.joy_2)[0:4])
            n+=1


    def loop(self):
        print("Creating Socket at IP: ",  self.HOST, " port: ", self.PORT)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            print("Connecting to socket..")

            self.s.connect((self.HOST, self.PORT))

        except Exception as e:
            print("Creating socket failed, restarting, error: ",  e)
            sleep(1)
            return -1

        print("Socket Connected")
        self.s.settimeout(3)
        if self.main_loop() == -1:
            return -1

joy = wireless_joy()

while 1:
    joy.loop()
