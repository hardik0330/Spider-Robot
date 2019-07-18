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

void loop() {
  pwm.setPWM(5, 0, SERVOMAX);
  pwm.setPWM(1, 0, SERVOMAX);
  pwm.setPWM(7, 0, SERVOMAX);
  pwm.setPWM(2, 0, SERVOMAX);

  pwm.setPWM(4, 0, SERVOMIN);
  pwm.setPWM(0, 0, SERVOMIN);
  pwm.setPWM(6, 0, SERVOMIN);
  pwm.setPWM(3, 0, SERVOMIN);
}
