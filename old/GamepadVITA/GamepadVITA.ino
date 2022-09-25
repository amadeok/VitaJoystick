// Simple gamepad example that demonstraits how to read five Arduino
// digital pins and map them to the Arduino Joystick library.
//
// The digital pins 2 - 6 are grounded when they are pressed.
// Pin 2 = UP
// Pin 3 = RIGHT
// Pin 4 = DOWN
// Pin 5 = LEFT
// Pin 6 = FIRE
//
// NOTE: This sketch file is for use with Arduino Leonardo and
//       Arduino Micro only.
//
// by Matthew Heironimus
// 2016-11-24
//--------------------------------------------------------------------

#include <Joystick.h>

Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, JOYSTICK_TYPE_GAMEPAD,
                   2, 0,                  // Button Count, Hat Switch Count
                   true, true, false,     // X and Y, but no Z Axis
                   true, true, false,   // No Rx, Ry, or Rz
                   false, false,          // No rudder or throttle
                   false, false, false);  // No accelerator, brake, or steering

void setup() {
  // Initialize Button Pins
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
    CLKPR = 0x80; // (1000 0000) enable change in clock frequency
  CLKPR = 0x01; // (0000 0001) use clock division factor 2 to reduce the frequency from 16 MHz to 8 MHz

  // Initialize Joystick Library
  Joystick.begin();
  Joystick.setXAxisRange(200, 800);
  Joystick.setYAxisRange(200, 800);
  Joystick.setRxAxisRange(200, 800);
  Joystick.setRyAxisRange(200, 800);
}

// Last state of the buttons
unsigned long lastExtremeTimes[3] = {0, 0, 0};
int switcher = -1;
int switch_count = 0;
bool updateRotAxis = false;
int milisecondsWindow = 500;
int clickDeadZone = 100;
unsigned long lastImmobileTime = -1;
unsigned long immobileClickTime = 1000;
bool allowImmobileClick = false;
int buttonDelay = 25;

void loop()
{

  int xax = analogRead(A0);  
  int yax = analogRead(A3);  
    // Serial.print( xax);          
   //Serial.print(" ");    
  // Serial.println(yax);

 if (xax  < 500 - clickDeadZone || xax  > 500 + clickDeadZone ||
     yax  < 500 - clickDeadZone || yax  > 500 + clickDeadZone)
     {
      lastImmobileTime = millis();
      allowImmobileClick = true;
     }

if (millis() - lastImmobileTime > 1000 && allowImmobileClick)
{
  Joystick.pressButton(0);
  delay(buttonDelay);
  Joystick.releaseButton(0);
  
  Serial.println("immobile Click ");
  allowImmobileClick = false;
}

  bool condition = false;

  if (switcher == -1)
    condition = xax > 750 ||  xax < 250;
  else  if (switcher)
    condition = xax > 750 ; // top
  else
    condition = xax < 250; // bottom

  //    for (int n = 0; n < 3; n++)
  //    {
  //      Serial.print(lastExtremeTimes[n]);
  //      Serial.print(" ");
  //    }
  //
  //    Serial.println(condition);

  if (condition ) //  || xax < 250
  {
    switch_count++;

    if (xax > 750) {
      switcher = 0;
      Serial.print(switch_count);
      Serial.println(" high ");

    }
    else if (xax < 250) {
      switcher = 1;
      Serial.print(switch_count);
      Serial.println(" low ");

    }

    lastExtremeTimes[0] = lastExtremeTimes[1];
    lastExtremeTimes[1] = lastExtremeTimes[2];
    lastExtremeTimes[2] = millis();
    if (lastExtremeTimes[2] - lastExtremeTimes[0] < milisecondsWindow 
    && switch_count >= 3)
    {
      Serial.print(switch_count);

      Serial.println(" trigger\n");
      switch_count = 0;
      Joystick.setXAxis(512);
      Joystick.setYAxis(512);
      delay(100);
      Joystick.pressButton(1);
      delay(buttonDelay);
      Joystick.releaseButton(1);

      //      if (updateRotAxis)
      //      {
      //        updateRotAxis = false;
      //          Joystick.setRxAxis(512);
      //        Joystick.setRyAxis(512);
      //
      //        }
      //      else
      //      {
      //        updateRotAxis = true;
      //          Joystick.setXAxis(512);
      //        Joystick.setYAxis(512);
      //
      //      }
      //      Serial.print("switching axis");
      //      Serial.println(updateRotAxis);


    }
   // if (switch_count> 2)
  //  switch_count = 0;


  }
  if (millis() - lastExtremeTimes[2] >= milisecondsWindow)
  {
    switch_count = 0;

    if (switcher != -1)
      Serial.println("\n");
    switcher = -1;
  }
  if (!updateRotAxis)
  {
    Joystick.setXAxis(xax);
    Joystick.setYAxis(yax);
  }
  else
  {
    Joystick.setRxAxis(xax);
    Joystick.setRyAxis(yax);
  }

  delay(10);
}
