/*
==Hardware===
- Arduino UNO R3
- MPU6050

===Software===
- Arduino IDE v1.8.12
- Arduino Wire library
- Arduino MPU6050_tockn library
*/

//inclui as bibliotecas
#include <Wire.h> //biblioteca para leitura dos dados recebidos nas portas A4 e A5
#include <MPU6050_tockn.h> //biblioteca para tratamento de dados do acelerometro/giroscopio

//=====MPU6050=====

//defini o primeiro MPU6050
MPU6050 mpu6050(Wire);

//defini as variaveis que receberao os valores
float AX = 0; //eixo X do acelerometro
float AY = 0; //eixo Y do acelerometro
float AZ = 0; //eixo Z do acelerometro
float GX = 0; //eixo X do giroscopio
float GY = 0; //eixo Y do giroscopio
float GZ = 0; //eixo Z do giroscopio
//defini o numero de pontos para o filtro de media movel
#define n 50

//defini o vetor com os valores para o filtro de media movel
float amostrasAX[n];
float amostrasAY[n];
float amostrasAZ[n];
float amostrasGX[n];
float amostrasGY[n];
float amostrasGZ[n];

//'cria' a funcao
float moving_averageAX();  //funcao para filtro de media movel
float moving_averageAY();
float moving_averageAZ();
float moving_averageGX();
float moving_averageGY();
float moving_averageGZ();


//=====MPU6050=====

/*

informacoes de outros sensores

*/

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
  //calcula a calibracao do giroscopio
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  //obtem os dados do MPU6050
  mpu6050.update();
  
  //limita a pesquisa por 0,1 segundo
//  if(millis() > 100){
    //valores do acelerometro e giroscopios
  AX = moving_averageAX(mpu6050.getAccX());
  AY = moving_averageAY(mpu6050.getAccY());
  AZ = moving_averageAZ(mpu6050.getAccZ());
  GX = moving_averageGX(mpu6050.getGyroX());
  GY = moving_averageGY(mpu6050.getGyroY());
  GZ = moving_averageGZ(mpu6050.getGyroZ());
    //aqui pega a hora
  
  //}
  
    //aqui envia para o servidor

  //imprime no monitor serial
  Serial.print("AX:");
  Serial.print(AX);
  Serial.print(" / ");
  Serial.print("AY: ");
  Serial.print(AY);
  Serial.print(" / ");
  Serial.print("AZ: ");
  Serial.print(AZ);
  Serial.print(" | ");
  
  Serial.print("GX: ");
  Serial.print(GX);
  Serial.print(" / ");
  Serial.print("GY: ");
  Serial.print(GY);
  Serial.print(" / ");
  Serial.print("GZ: ");
  Serial.print(GZ);
  Serial.println(" | ");

  //reseta os valores dos arrays
  AX = 0;
  AY = 0;
  AZ = 0;
  GX = 0;
  GY = 0;
  GZ = 0;
}

//=====Funcoes=====
float moving_averageAX(float eixo){
   //desloca os elementos do vetor de média móvel
   for(int i= n-1; i>0; i--) amostrasAX[i] = amostrasAX[i-1];
   amostrasAX[0] = eixo; //posição inicial do vetor recebe a leitura original
   float acc = 0; //acumulador para somar os pontos da média móvel
   for(int i=0; i<n; i++) acc += amostrasAX[i]; //faz a somatória do número de pontos
   return acc/n;  //retorna a média móvel
}

float moving_averageAY(float eixo){
   //desloca os elementos do vetor de média móvel
   for(int i= n-1; i>0; i--) amostrasAY[i] = amostrasAY[i-1];
   amostrasAY[0] = eixo; //posição inicial do vetor recebe a leitura original
   float acc = 0; //acumulador para somar os pontos da média móvel
   for(int i=0; i<n; i++) acc += amostrasAY[i]; //faz a somatória do número de pontos
   return acc/n;  //retorna a média móvel
}

float moving_averageAZ(float eixo){
   //desloca os elementos do vetor de média móvel
   for(int i= n-1; i>0; i--) amostrasAZ[i] = amostrasAZ[i-1];
   amostrasAZ[0] = eixo; //posição inicial do vetor recebe a leitura original
   float acc = 0; //acumulador para somar os pontos da média móvel
   for(int i=0; i<n; i++) acc += amostrasAZ[i]; //faz a somatória do número de pontos
   return acc/n;  //retorna a média móvel
}

float moving_averageGX(float eixo){
   //desloca os elementos do vetor de média móvel
   for(int i= n-1; i>0; i--) amostrasGX[i] = amostrasGX[i-1];
   amostrasGX[0] = eixo; //posição inicial do vetor recebe a leitura original
   float acc = 0; //acumulador para somar os pontos da média móvel
   for(int i=0; i<n; i++) acc += amostrasGX[i]; //faz a somatória do número de pontos
   return acc/n;  //retorna a média móvel
}

float moving_averageGY(float eixo){
   //desloca os elementos do vetor de média móvel
   for(int i= n-1; i>0; i--) amostrasGY[i] = amostrasGY[i-1];
   amostrasGY[0] = eixo; //posição inicial do vetor recebe a leitura original
   float acc = 0; //acumulador para somar os pontos da média móvel
   for(int i=0; i<n; i++) acc += amostrasGY[i]; //faz a somatória do número de pontos
   return acc/n;  //retorna a média móvel
}

float moving_averageGZ(float eixo){
   //desloca os elementos do vetor de média móvel
   for(int i= n-1; i>0; i--) amostrasGZ[i] = amostrasGZ[i-1];
   amostrasGZ[0] = eixo; //posição inicial do vetor recebe a leitura original
   float acc = 0; //acumulador para somar os pontos da média móvel
   for(int i=0; i<n; i++) acc += amostrasGZ[i]; //faz a somatória do número de pontos
   return acc/n;  //retorna a média móvel
}


