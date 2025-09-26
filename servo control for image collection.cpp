//this code controls several servos with an arduino, to autonomously collect images from various angles
//the imgaes were used to train the ML model for autonomous obstacle avoidance

//根本からservo 1,2,3

//その順番で動いていく

#include <ESP32Servo.h>
Servo servo1;
Servo servo2;
Servo servo3;
int servoangle1;
int servoangle2;
int servoangle3;
int servo_1 = 0;
int servo_2 = 0;
int servo_3 = 0;

void setup() {
Serial.begin(115200);
servo1.setPeriodHertz(50); 
servo2.setPeriodHertz(50);
servo3.setPeriodHertz(50);
servo1.attach(12, 1000, 2000); 
servo2.attach(13, 1000, 2000);
servo3.attach(15, 1000, 2000);
delay(100);
}

void loop()
{

if ( 1<= servo_1 && servo_1 <=6){
if ( 1<= servo_2 && servo_2 <=6){
 if ( 1 <= servo_3 && servo_3 <=6){
servo3.write(servoangle3);    
delay(1000);
servoangle3 += 20;
servo_3 += 1;
  }
 else{
servo2.write(servoangle2);    
delay(1000);
servoangle2 += 20;
servo_2 += 1;
servo3.write(90);    
delay(1000);
servo_3 = 1;
servoangle3 = 30;
 }
}
else{
servo1.write(servoangle1);    
delay(1000);
servoangle1 += 20;
servo_1 += 1;  
servo2.write(140);    
delay(1000);
servo_2 = 1;
servoangle2 = 80;
}
}
else{
  servo1.write(90);
  delay(1000);
  servo_1 = 1;
  servoangle1 = 30;
}
}
 

