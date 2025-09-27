#include <esp_now.h>
#include <WiFi.h>

 int channel1command = 0;
 int channel2command = 0;
 int channel3command = 0;
 int channel4command = 0;
 int channel5command = 0;
 int channel6command = 0;

 int centerXval1 = 2000;
 int centerYval1 = 1915;
 int centerXval2 = 1871;
 int centerYval2 = 1935;

 int xVal1 = 0;
 int yVal1 = 0;
 int zVal1 = 0;
 int xVal2 = 0;
 int yVal2 = 0;
 int zVal2 = 0;

// REPLACE WITH YOUR RECEIVER MAC Address
uint8_t broadcastAddress[] = {0xEC,0x62,0x60,0x9A,0x16,0xE8};

// Structure example to send data
// Must match the receiver structure
typedef struct struct_message {
  int channel1;
  int channel2;
  int channel3;
  int channel4;
  int channel5;
  int channel6; 
} struct_message;

// Create a struct_message called myData
struct_message myData;

esp_now_peer_info_t peerInfo;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {

Serial.begin(115200);

 pinMode(33, INPUT_PULLUP); //z axis is a button.
 pinMode(14, INPUT_PULLUP); //z axis is a button.
 
  // Init Serial Monitor
  Serial.begin(115200);
 
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}
 
void loop() {
 xVal1 = analogRead(32);
 yVal1 = analogRead(35);
 zVal1 = digitalRead(33);
 xVal2 = analogRead(12);
 yVal2 = analogRead(13);
 zVal2 = digitalRead(14);

 //later use the center values to correctly measure how much the joystick has went up
 //squish the values to 1000 to 2000 like a rc transimitter
 
 if(centerXval1 - 50 < xVal1 && xVal1 < centerXval1 + 50){
  channel1command = 1500;
  }
 else{
 channel1command = (xVal1 - centerXval1)*0.25 + 1500;
 }

 if(centerXval2 - 50 < xVal2 && xVal2 < centerXval2 + 50){
  channel2command = 1500;
  }
 else{
 channel2command = (xVal2 - centerXval2)*0.25 + 1500;
 }

 if(centerYval1 - 50 < yVal1 && yVal1 < centerYval1 + 50){
  channel3command = 1500;
  }
 else{
 channel3command = (yVal1 - centerYval1)*0.25 + 1500;
 }

 if(centerYval2 - 50 < yVal2 && yVal2 < centerYval2 + 50){
  channel4command = 1500;
  }
 else{
 channel4command = (yVal2 - centerYval2)*0.25 + 1500;
 }

// Corrections in input validation
if (channel1command > 2000) {
  channel1command = 2000;
}
if (channel1command < 1000) {
  channel1command = 1000;
}

if (channel2command > 2000) {
  channel2command = 2000;
}
if (channel2command < 1000) {
  channel2command = 1000;
}

if (channel3command > 2000) {
  channel3command = 2000;
}
if (channel3command < 1000) {
  channel3command = 1000;
}

if (channel4command > 2000) {
  channel4command = 2000;
}
if (channel4command < 1000) {
  channel4command = 1000;
}

 channel5command = zVal1;
 channel6command = zVal2;

  // Set values to send
  myData.channel1 = channel1command;
  myData.channel2 = channel2command;
  myData.channel3 = channel3command;
  myData.channel4 = channel4command;
  myData.channel5 = channel5command;
  myData.channel6 = channel6command;
 
  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }

  Serial.print("channel1:");
  Serial.print(xVal1);
  Serial.print("\t"); 
  Serial.print("channel2");
  Serial.print(yVal1);
  Serial.print("\t"); 
  Serial.print("channel3");
  Serial.print(zVal1);
  Serial.print("\t"); 
  Serial.print("channel4");
  Serial.print(xVal2);
  Serial.print("\t"); 
  Serial.print("channel5");
  Serial.print(yVal2);
  Serial.print("\t"); 
  Serial.print("channel6");
  Serial.println(zVal2);
  delay(100);
}