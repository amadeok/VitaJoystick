import vgamepad as vg
from time import sleep
import socket
import time
import msvcrt
import keyboard

HOST = "192.168.1.91"  # The server's hostname or IP address
PORT = 3333  # The port used by the server
max_x = 3220
max_y = 3000
min_x = 586
min_y = 613
gamepad = vg.VX360Gamepad()
import threading


def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


class wireless_joy():
    def __init__(self) -> None:
        pass
        self.data = bytearray(8)
        self.joy_x = 1800
        self.joy_y = 1800
        self.switch_count = 0
        self.switcher = 0
        self.lastExtremeTimes = [float(0) for x in range(3)]
        self.milisecondsWindow = 0.5
        self.buttonDelay = 0.0200
        self.extreme_threshold = 0.8
        thread1 = threading.Thread(target=self.key_lisesnt, args=())
        thread1.start()

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


    def patter_detect(self):
        condition = False;

        if self.switcher == -1:
            condition = self.joy_x > self.extreme_threshold or  self.joy_x < -self.extreme_threshold;
        elif self.switcher:
            condition = self.joy_x > self.extreme_threshold ; # top
        else:
            condition = self.joy_x < -self.extreme_threshold; # bottom

  #    for (int n = 0; n < 3; n+=1)
  #    
  #      print(self.lastExtremeTimes[n]);
  #      print(" ");
  #    print(condition);

        if condition:  #  or self.joy_x < -self.extreme_threshold
  
            self.switch_count+=1

            if self.joy_x > self.extreme_threshold:
                self.switcher = 0
                print(self.switch_count, " high ")

            elif self.joy_x < -self.extreme_threshold:
                self.switcher = 1
                print(self.switch_count, " low ")

            self.lastExtremeTimes[0] = self.lastExtremeTimes[1];
            self.lastExtremeTimes[1] = self.lastExtremeTimes[2];
            self.lastExtremeTimes[2] = time.time()
            if self.lastExtremeTimes[2] - self.lastExtremeTimes[0] < self.milisecondsWindow  and self.switch_count >= 3:
            
                print(self.switch_count);

                print(" trigger\n");
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
                keyboard.press("esc")
                sleep(self.buttonDelay);
                keyboard.release("esc")


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
            # if x > max_x: max_x = x
            # if y > max_y: max_y = y
            # if x < min_x: min_x = x
            # if y < min_y: min_y = y
            # s.send(self.data)
            self.joy_x = scale(x, (min_x, max_x), (-1.0, +1.0))

            self.joy_y = scale(y, (max_y, min_y), (-1.0, +1.0))
            self.patter_detect()

            gamepad.left_joystick_float(self.joy_x, self.joy_y) 
            gamepad.update() 

            #print(x, y, self.joy_x, self.joy_y, self.data)
            #print(str(self.joy_x)[0:4], str(self.joy_y)[0:4])
            n+=1


    def loop(self):
        print("Creating Socket at IP: ",  HOST, " port: ", PORT)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            print("Connecting to socket..")

            self.s.connect((HOST, PORT))

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

exit()
print(f"Received self.data!r")
from time import sleep
import pyautogui
gamepad = vg.VX360Gamepad()

# for x in range(10):
#     gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # press the A button
#     gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)  # press the left hat button

#     gamepad.update()  # send the updated state to the computer

#     sleep(1)
#     gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # release the A button

#     gamepad.update() 
x_res = 2560
y_res = 1440
while 1:
    sleep(0.01)
    pos = pyautogui.position()
    x = (pos.x - x_res/2 ) / (x_res/2)
    y = (pos.y - y_res/2) / (y_res/2)
    print(pos, x, y)


    gamepad.left_joystick_float(x, y)  # values between -32768 and 32767
    gamepad.update() 
   # gamepad.right_joystick(x_value=-32768, y_value=15000)  
sleep(10)