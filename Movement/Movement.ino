#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  100 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // this is the 'maximum' pulse length count (out of 4096)
#define SERVOMID  300
void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  delay(10);
}
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;

  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period");
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit");
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}
void tilt(int n)
{
  pwm.setPWM(5, 0, SERVOMID);
  pwm.setPWM(1, 0, SERVOMID);
  pwm.setPWM(7, 0, SERVOMID);
  pwm.setPWM(2, 0, SERVOMID);
  switch(n)
  {
    case 1:
    pwm.setPWM(4, 0, 250);
    pwm.setPWM(0, 0, 400);
    pwm.setPWM(6, 0, 100);
    pwm.setPWM(3, 0, 250);
    delay(200);
    pwm.setPWM(4, 0, 250);
    pwm.setPWM(0, 0, 100);
    pwm.setPWM(6, 0, 100);
    pwm.setPWM(3, 0, 250);
    break;

    case 2:
    pwm.setPWM(4, 0, 100);
    pwm.setPWM(0, 0, 250);
    pwm.setPWM(6, 0, 250);
    pwm.setPWM(3, 0, 400);
    delay(200);
    pwm.setPWM(4, 0, 100);
    pwm.setPWM(0, 0, 250);
    pwm.setPWM(6, 0, 250);
    pwm.setPWM(3, 0, 100);
    break;
  
    case 3:
    pwm.setPWM(4, 0, 400);
    pwm.setPWM(0, 0, 250);
    pwm.setPWM(6, 0, 250);
    pwm.setPWM(3, 0, 100);
    delay(200);
    pwm.setPWM(4, 0, 100);
    pwm.setPWM(0, 0, 250);
    pwm.setPWM(6, 0, 250);
    pwm.setPWM(3, 0, 100);
    break;

    case 4:
    pwm.setPWM(4, 0, 250);
    pwm.setPWM(0, 0, 100);
    pwm.setPWM(6, 0, 400);
    pwm.setPWM(3, 0, 250);
    delay(200);
    pwm.setPWM(4, 0, 250);
    pwm.setPWM(0, 0, 100);
    pwm.setPWM(6, 0, 100);
    pwm.setPWM(3, 0, 250);
    break;
  }
}
void test(int n)
{
  switch(n)
  {
    case 0:
    pwm.setPWM(0,0,SERVOMIN);
    delay(500);
    pwm.setPWM(0,0,SERVOMAX);
    delay(500);
    break;
    
    case 1:
    pwm.setPWM(1,0,SERVOMIN);
    delay(500);
    pwm.setPWM(1,0,SERVOMAX);
    delay(500);
    break;
    
    case 2:
    pwm.setPWM(2,0,SERVOMIN);
    delay(500);
    pwm.setPWM(2,0,SERVOMAX);
    delay(500);
    break;
    
    case 3:
    pwm.setPWM(3,0,SERVOMIN);
    delay(500);
    pwm.setPWM(3,0,SERVOMAX);
    delay(500);
    break;
    
    case 4:
    pwm.setPWM(4,0,SERVOMIN);
    delay(500);
    pwm.setPWM(4,0,SERVOMAX);
    delay(500);
    break;

    case 5:
    pwm.setPWM(5,0,SERVOMIN);
    delay(500);
    pwm.setPWM(5,0,SERVOMAX);
    delay(500);
    break;

    case 6:
    pwm.setPWM(6,0,SERVOMIN);
    delay(500);
    pwm.setPWM(6,0,SERVOMAX);
    delay(500);
    break;

    case 7:
    pwm.setPWM(7,0,SERVOMIN);
    delay(500);
    pwm.setPWM(7,0,SERVOMAX);
    delay(500);
    break;

  }
}
void idle()
{
  pwm.setPWM(5, 0, SERVOMID);
  pwm.setPWM(1, 0, SERVOMID);
  pwm.setPWM(7, 0, SERVOMID);
  pwm.setPWM(2, 0, SERVOMID);
  
  pwm.setPWM(4, 0, SERVOMIN);
  pwm.setPWM(0, 0, SERVOMIN);
  pwm.setPWM(6, 0, SERVOMIN);
  pwm.setPWM(3, 0, SERVOMIN);
}
void flex()
{
  pwm.setPWM(5, 0, SERVOMID);
  pwm.setPWM(1, 0, SERVOMID);
  pwm.setPWM(7, 0, SERVOMID);
  pwm.setPWM(2, 0, SERVOMID);
  
  pwm.setPWM(4, 0, SERVOMAX);
  pwm.setPWM(0, 0, SERVOMAX);
  pwm.setPWM(6, 0, SERVOMAX);
  pwm.setPWM(3, 0, SERVOMAX);
}
void motion(int n)
{
  switch(n)
  {
    case 1:
//    pwm.setPWM(5, 0, SERVOMID);
    pwm.setPWM(1, 0, SERVOMIN);
    delay(50);
    pwm.setPWM(0, 0, 400);
//    pwm.setPWM(7, 0, SERVOMID);
//    pwm.setPWM(2, 0, SERVOMID);
    break;

     case 2:
//    pwm.setPWM(5, 0, SERVOMID);
//    pwm.setPWM(1, 0, SERVOMID);
//    pwm.setPWM(7, 0, SERVOMID);
    pwm.setPWM(2, 0, SERVOMAX);
    delay(50);
    pwm.setPWM(3, 0, 400);
    break;

    case 3:
    pwm.setPWM(5, 0, SERVOMIN);
    delay(50);
    pwm.setPWM(4, 0, 400);
//    pwm.setPWM(1, 0, SERVOMID);
//    pwm.setPWM(7, 0, SERVOMID);
//    pwm.setPWM(2, 0, SERVOMID);
    break;

    case 4:
//    pwm.setPWM(5, 0, SERVOMID);
//    pwm.setPWM(1, 0, SERVOMID);
    pwm.setPWM(7, 0, SERVOMAX);
    delay(200);
    pwm.setPWM(6, 0, 400);
//    pwm.setPWM(2, 0, SERVOMID);
    break;
  }
}
void loop() {
//  tilt(1);
//  delay(2000);
//  tilt(2);
//  delay(2000);
tilt(1);
motion(1);
delay(20);
idle();
delay(20);
tilt(4);
motion(4);
delay(20);
idle();
delay(20);
tilt(2);
motion(2);
delay(20);
idle();
delay(20);
tilt(3);
motion(3);
delay(20);
idle();
delay(20);
}
