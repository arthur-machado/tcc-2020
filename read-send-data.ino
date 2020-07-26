
/*
 WiFiEsp example: WebClient
 This sketch connects to google website using an ESP8266 module to
 perform a simple web search.
 For more details see: http://yaab-arduino.blogspot.com/p/wifiesp-example-client.html
*/

#include "WiFiEsp.h"
#include <Wire.h>
#include <MPU6050_tockn.h> //biblioteca para tratamento de dados do acelerometro/giroscopio


// Emulate Serial1 on pins 6/7 if not present
#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial Serial1(6, 7); // RX, TX
#endif

MPU6050 mpu6050(Wire);

float accX, accY, girX, girY, girZ; //variáveis para os eixos

char ssid[] = "GUSTAVO-LEOVIN-FIBER";//SSID 
char pass[] = "35297907";        // Password
int status = WL_IDLE_STATUS;     // the Wifi radio's status


// Initialize the Ethernet client object
WiFiEspClient client;


void setup()
{
  // initialize serial for debugging
  Serial.begin(9600);
  // initialize serial for ESP module
  Serial1.begin(9600);
  // initialize ESP module
  WiFi.init(&Serial1);

  Wire.begin();
  //inicia o MPU6050
  mpu6050.begin();

  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }

  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Tentando conectar à rede ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }

  // you're connected now, so print out the data
  Serial.println("Conectado!");

  //informações da conexão
  printWifiStatus();

  //calcula a calibracao do giroscopio
  mpu6050.calcGyroOffsets(true);

  Serial.println();
  
}

void loop()
{
   mpu6050.update();

   //pega todos os valores de eixo
   accX = mpu6050.getAccX();
   accY = mpu6050.getAccY();
   girX = mpu6050.getGyroX();
   girY = mpu6050.getGyroY();
   girZ = mpu6050.getGyroZ();
 
  // if there are incoming bytes available
  // from the server, read them and print them
  while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

  if(client.connect(server, 5000)){
    Serial.println("Conectado ao servidor");
    
    sendPostRequest();
  
    

    Serial.println("Dados enviados");

    }
    
}

void sendPostRequest(){
    Serial.println("Enviando dados...");
  
   // cria o json
    String content = "{\"sensor\":\"gir/acc\",\"petID\":\"tuco\",\"time\":\"1234\",\"girX\":"+ String(girX) +",\"girY\":"+ String(girY) + ",\"girZ\":"+ String(girZ) + ",\"accX\":"+ String(accX) + ",\"accY\":" + String(accY)+"}";

    //envia a requisição
    client.println("POST /rawData/ HTTP/1.1");
    client.println("Host: 192.168.100.187:5000");
    client.println("Accept: */*");
    //client.println("Connection: close"); comentado devido a bad requests
    client.println("Content-Length: " + String(content.length()));
    client.println("Content-Type: application/json; charset=utf-8;");
    client.println();
    client.println(content);
    client.stop();
 
}

void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength
  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
