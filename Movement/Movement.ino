#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  100 
#define SERVOMAX  600 

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  
  //delay(10);
}
void lto()
{
  pwm.setPWM(5, 0, 300);
  pwm.setPWM(1, 0, 300);
  pwm.setPWM(7, 0, 300);
  pwm.setPWM(2, 0, 300);

  pwm.setPWM(4, 0, SERVOMAX);
  pwm.setPWM(0, 0, SERVOMAX);
  pwm.setPWM(6, 0, SERVOMAX);
  pwm.setPWM(3, 0, SERVOMAX);
  delay(1000);
  pwm.setPWM(3, 0, SERVOMIN);
  delay(200);
  pwm.setPWM(5, 0, SERVOMIN);
  delay(200);
//  pwm.setPWM(3, 0, SERVOMAX);
//  delay(200);
//  pwm.setPWM(5, 0, 450);
//  pwm.setPWM(1, 0, SERVOMIN);
//  pwm.setPWM(7, 0, SERVOMIN);
  delay(10000);
}
void loop() {
  lto();
}
