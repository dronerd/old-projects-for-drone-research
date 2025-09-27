/* Get tilt angles on X and Y, and rotation angle on Z
 * Angles are given in degrees
 * 3.3v
connect scl to a5
connect sda to a4
 */

//This code actually worked with the esp32 dev kit,
//5v connected to vin,
//gnd connected to gnd
//22 connected to scl
//21 connected to sdk


#include "Wire.h"
#include <MPU6050_light.h>

#define I2C_SDA 2 //change here and also Wire.begin to change the scl sdk pins
#define I2C_SCL 14

MPU6050 mpu(Wire);
unsigned long timer = 0;
int readpitch = 0;
int readroll = 0;
int readyaw = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin(2,14);
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");
}

void loop() {
  mpu.update();
  
  readpitch = mpu.getAngleX();
  readroll = mpu.getAngleY();
  readyaw = mpu.getAngleZ();
  
  if((millis()-timer)>10){ // print data every 10ms
  Serial.print("X : ");
  Serial.print(readpitch);
  Serial.print("\tY : ");
  Serial.print(readroll);
  Serial.print("\tZ : ");
  Serial.println(readyaw);
  timer = millis();  
  }
}