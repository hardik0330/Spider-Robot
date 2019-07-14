#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  100 
#define SERVOMAX  600 

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  
  delay(10);
}
// void setServoPulse(uint8_t n, double pulse) {
//   double pulselength;

//   pulselength = 1000000;   
//   pulselength /= 60;   // 60 Hz
//   Serial.print(pulselength); Serial.println(" us per period");
//   pulselength /= 4096;  // 12 bits of resolution
//   Serial.print(pulselength); Serial.println(" us per bit");
//   pulse *= 1000000;  // convert to us
//   pulse /= pulselength;
//   Serial.println(pulse);
//   pwm.setPWM(n, 0, pulse);
// }
void loop()
{
  //pwm.setPWM(servomumber, 0 , pulselength);
  //servonum in our case ranges from 0 to 7 
  //set position of servo only between SERVOMIN and SERVOMAX for servo to work properly
  pwm.setPWM(0, 0, SERVOMIN);   //sets position of servo to min
  delay(1000);
  pwm.setPWM(0, 0, SERVOMAX);   //sets position of servo to max
  delay(1000);
}

void loop() {
  pwm.setPWM(5, 0, 300);
  pwm.setPWM(1, 0, 300);
  pwm.setPWM(7, 0, 300);
  pwm.setPWM(2, 0, 300);

  pwm.setPWM(4, 0, 200);
  pwm.setPWM(0, 0, 200);
  pwm.setPWM(6, 0, 200);
  pwm.setPWM(3, 0, 200);
//  delay(00);

  pwm.setPWM(0,0,100);
  pwm.setPWM(1,0,450);
  delay(200);
  pwm.setPWM(0,0,200);
  pwm.setPWM(1,0,300);
  
  delay(200);
  pwm.setPWM(6,0,100);
  pwm.setPWM(7,0,200);
  delay(200);
  pwm.setPWM(6,0,200);
  pwm.setPWM(7,0,300);

  delay(200);
  pwm.setPWM(4,0,100);
  pwm.setPWM(5,0,200);
  delay(200);
  pwm.setPWM(4,0,200);
  pwm.setPWM(5,0,300);

  delay(200);
  pwm.setPWM(3,0,100);
  pwm.setPWM(2,0,450);
  delay(200);
  pwm.setPWM(3,0,200);
  pwm.setPWM(2,0,300);
  
  delay(200);
}