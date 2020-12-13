#include <Wire.h>
#include "gyro_accel.h" 

#define dt 20                       // time difference in milli seconds
#define rad2degree 57.3              // Radian to degree conversion
#define Filter_gain 0.95             // e.g.  angle = angle_gyro*Filter_gain + angle_accel*(1-Filter_gain)

unsigned long t=0; // Time Variables
float angle_x_gyro=0,angle_y_gyro=0,angle_z_gyro=0,angle_x_accel=0,angle_y_accel=0,angle_z_accel=0,angle_x=0,angle_y=0,angle_z=0;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    MPU6050_ResetWake();
    MPU6050_SetGains(0,1);// Setting the lows scale
    MPU6050_SetDLPF(0); // Setting the DLPF to inf Bandwidth for calibration
    MPU6050_OffsetCal();
    MPU6050_SetDLPF(6); // Setting the DLPF to lowest Bandwidth

    Serial.print("\tangle_x_gyro");
    Serial.print("\tangle_y_gyro");
    Serial.print("\tangle_z_gyro");
    
    Serial.print("\tangle_x_accel");
    Serial.print("\tangle_y_accel");
    Serial.print("\tangle_z_accel");
    
}

void loop() {
  t=millis(); 

  MPU6050_ReadData();
  
  angle_x_gyro = (gyro_x_scalled*((float)dt/1000)+angle_x);
  angle_y_gyro = (gyro_y_scalled*((float)dt/1000)+angle_y);
  angle_z_gyro = (gyro_z_scalled*((float)dt/1000)+angle_z);

  angle_z_accel = atan(accel_z_scalled/(sqrt(accel_y_scalled*accel_y_scalled+accel_x_scalled*accel_x_scalled)))*(float)rad2degree;
  angle_y_accel = -atan(accel_y_scalled/(sqrt(accel_y_scalled*accel_y_scalled+accel_z_scalled*accel_z_scalled)))*(float)rad2degree;
  angle_x_accel = atan(accel_x_scalled/(sqrt(accel_x_scalled*accel_x_scalled+accel_z_scalled*accel_z_scalled)))*(float)rad2degree;

  Serial.print(angle_x_gyro);
  Serial.print("\t");
  Serial.print(angle_y_gyro);
  Serial.print("\t");
  Serial.print(angle_z_gyro);
  Serial.print("\t"); 
   
  Serial.print(angle_x_accel);
  Serial.print("\t");
  Serial.print(angle_y_accel);
  Serial.print("\t");
  Serial.print(angle_z_accel);
  Serial.print("\t"); 

  Serial.println(((float)(millis()-t)/(float)dt)*100);

  while((millis()-t) < dt){ // Making sure the cycle time is equal to dt
  // Do nothing
  }
}
