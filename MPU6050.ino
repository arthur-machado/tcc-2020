//inclui as bibliotecas
#include <MPU6050_tockn.h>
#include <Wire.h>

//defini o primeiro MPU6050
MPU6050 mpu6050(Wire);

long timer = 0;

//defini as variaveis que receberao os valores
float AX = 0;
float AY = 0;
float AZ = 0;
float GX = 0;
float GY = 0;
float GZ = 0;
float AAX = 0;
float AAY = 0;
float GAX = 0;
float GAY = 0;
float GAZ = 0;
float TEMP = 0;


  //inserir configuracoes restantes

void setup() {
  Serial.begin(9600);
  Wire.begin();
  //inicia o MPU6050
  mpu6050.begin();
  //reseta os valores das variaveis
  AX = 0;
  AY = 0;
  AZ = 0;
  GX = 0;
  GY = 0;
  GZ = 0;
  AAX = 0;
  AAY = 0;
  GAX = 0;
  GAY = 0;
  GAZ = 0;
  TEMP = 0;
  //calcula a calibracao do giroscopio
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  //obtem os dados do MPU6050
  mpu6050.update();
  
  //limita a pesquisa por meio segundo
  if(millis() > 100){
  //adiciona os valores do sensor nos arrays
    //valores do acelerometro e giroscopios
  AX = mpu6050.getAccX();
  AY = mpu6050.getAccY();
  AZ = mpu6050.getAccZ();
  GX = mpu6050.getGyroX();
  GY = mpu6050.getGyroY();
  GZ = mpu6050.getGyroZ();
    //valores dos angulos
  AAX = mpu6050.getAccAngleX();
  AAY = mpu6050.getAccAngleY();
  GAX = mpu6050.getGyroAngleX();
  GAY = mpu6050.getGyroAngleY();
  GAZ = mpu6050.getGyroAngleZ();
    //temperatura
  TEMP = mpu6050.getTemp();
    //aqui pega a hora
  }
  
    //aqui envia para o servidor

  
  //imprime no monitor serial
//  Serial.print("AX:");
//  Serial.print(AX);
//  Serial.print(" / ");
//  Serial.print("AY: ");
//  Serial.print(AY);
//  Serial.print(" / ");
//  Serial.print("AZ: ");
//  Serial.print(AZ);
//  Serial.print(" | ");
//
//  Serial.print("GX: ");
//  Serial.print(GX);
//  Serial.print(" / ");
//  Serial.print("GY: ");
//  Serial.print(GY);
//  Serial.print(" / ");
//  Serial.print("GZ: ");
//  Serial.print(GZ);
//  Serial.print(" | ");

//  Serial.print("AAX:");
//  Serial.print(AAX);
//  Serial.print(" / ");
//  Serial.print("AAY: ");
//  Serial.print(AAY);
//  Serial.print(" | ");

  Serial.print("GAX: ");
  Serial.print(GAX);
  Serial.print(" / ");
  Serial.print("GAY: ");
  Serial.print(GAY);
  Serial.print(" / ");
  Serial.print("GAZ: ");
  Serial.print(GAZ);
  Serial.print(" | ");

//  Serial.print("TEMP: ");
//  Serial.print(TEMP);
//  Serial.println(" ");
  
  //reseta os valores dos arrays
  AX = 0;
  AY = 0;
  AZ = 0;
  GX = 0;
  GY = 0;
  GZ = 0;
  AAX = 0;
  AAY = 0;
  GAX = 0;
  GAY = 0;
  GAZ = 0;
  TEMP = 0;
  
}
