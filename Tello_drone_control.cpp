#include <WiFi.h>
#include <WiFiUdp.h>

// WiFi network name and password:
const char * networkName = "TELLO-XXXXX";
const char * networkPswd = "";

//IP address to send UDP data to:
// either use the ip address of the server or
// a network broadcast address
const char * udpAddress = "192.168.10.1";
const int udpPort = 8889;

//Are we currently connected?
boolean connected = false;

//The udp library class
WiFiUDP udp;

void setup() {
  // Initilize hardware serial:
  Serial.begin(115200);

  //Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);
}

boolean takeOff = false;

void loop() {
  if (takeOff) {
    TelloCommand("go 0 0 80 100"); delay(8000);
    TelloCommand("go 80 -30 0 100"); delay(8000);
    TelloCommand("go -40 -40 0 100"); delay(8000);
    TelloCommand("go -30 0 0 100"); delay(8000);
    TelloCommand("go 0 80 0 100"); delay(8000);
    TelloCommand("land"); delay(8000);
    TelloCommand("takeoff"); delay(8000);
    TelloCommand("go 0 110 0 100"); delay(8000);
    TelloCommand("go 30 0 0 100"); delay(8000);
    TelloCommand("go -30 -85 0 100"); delay(8000);
    TelloCommand("land"); delay(8000);
   
    takeOff = false;  // Reset takeOff flag
  }
}

void TelloCommand(char *cmd) {
  //only send data when connected
  if (connected) {
    //Send a packet
    udp.beginPacket(udpAddress, udpPort);
    udp.printf(cmd);
    udp.endPacket();
    Serial.printf("Send [%s] to Tello.\n", cmd);
  }
}

void connectToWiFi(const char * ssid, const char * pwd) {
  Serial.println("Connecting to WiFi network: " + String(ssid));
  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  //Initiate connection
  WiFi.begin(ssid, pwd);
  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event) {
  switch (event) {
    case SYSTEM_EVENT_STA_GOT_IP:
      //When connected set
      Serial.print("WiFi connected! IP address: ");
      Serial.println(WiFi.localIP());
      //initializes the UDP state
      //This initializes the transfer buffer
      udp.begin(WiFi.localIP(), udpPort);
      connected = true;
      TelloCommand("command");
      delay(2000);
      TelloCommand("speed 100");
      delay(5000);
      TelloCommand("takeoff");
      delay(8000);
      takeOff = true;
      break;
      
    case SYSTEM_EVENT_STA_DISCONNECTED:
      Serial.println("WiFi lost connection");
      connected = false;
      break;
  }
}