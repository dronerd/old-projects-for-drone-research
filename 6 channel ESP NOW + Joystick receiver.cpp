#include <esp_now.h>
#include <WiFi.h>

// Structure example to receive data
// Must match the sender structure
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

// callback function that will be executed when data is received
//this part automatically sets the new values such as myData.channel1 whenever new data is received via ESP32
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
}
 
void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
}
 
void loop() {
//changed the serial output to make it easier to see
  Serial.print("channel1:");
  Serial.print(myData.channel1);
  Serial.print("\t"); 
  Serial.print("channel2");
  Serial.print(myData.channel2);
  Serial.print("\t"); 
  Serial.print("channel3");
  Serial.print(myData.channel3);
  Serial.print("\t"); 
  Serial.print("channel4");
  Serial.print(myData.channel4);
  Serial.print("\t"); 
  Serial.print("channel5");
  Serial.print(myData.channel5);
  Serial.print("\t"); 
  Serial.print("channel6");
  Serial.println(myData.channel6);

//now we can use the values myData.channel1 for many other functions inside the loop
  delay(100);
}