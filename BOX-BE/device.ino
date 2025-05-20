#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define EEPROM_SIZE 512
#define MQTT_PORT 1883
#define AP_PASSWORD "cactus@123"
#define RESET_BUTTON D3

#define NUM_REASON_BUTTONS 6
const uint8_t REASON_BUTTON_PINS[NUM_REASON_BUTTONS] = {D0, D1, D2, D4, D5, D6}; // Update as per your wiring
bool buttonState[NUM_REASON_BUTTONS] = {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH};
unsigned long lastDebounceTime[NUM_REASON_BUTTONS] = {0};
const unsigned long debounceDelay = 50;

// RGB LED Pins
#define LED_RED D7
#define LED_GREEN D8
#define LED_BLUE D2

ESP8266WebServer server(80);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

String storedSSID = "";
String storedPassword = "";
String storedMQTT = "";
String storedOrgId = "";
bool isProvisioned = false;
String deviceUUID = "";

unsigned long previousMillis = 0;
const long interval = 10000; // 10 seconds

void setup()
{
    Serial.begin(115200);
    pinMode(RESET_BUTTON, INPUT_PULLUP);
    for (int i = 0; i < NUM_REASON_BUTTONS; i++)
    {
        pinMode(REASON_BUTTON_PINS[i], INPUT_PULLUP);
    }
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);

    EEPROM.begin(EEPROM_SIZE);
    readStoredData();
    String apSSID = "CAC_" + getMacID();
    deviceUUID = apSSID;

    if (isProvisioned)
    {
        Serial.println("📱 Connecting to stored WiFi: " + storedSSID);
        WiFi.mode(WIFI_STA);
        WiFi.begin(storedSSID.c_str(), storedPassword.c_str());

        int retryCount = 0;
        while (WiFi.status() != WL_CONNECTED && retryCount < 30)
        {
            Serial.print(".");
            delay(1000);
            retryCount++;
        }

        if (WiFi.status() == WL_CONNECTED)
        {
            Serial.println("\n✅ Connected to WiFi!");
            setLEDColor(0, 255, 0);
            connectToMQTT();
        }
        else
        {
            Serial.println("\n❌ WiFi Connection Failed! Switching to AP mode...");
            setLEDColor(255, 0, 0);
            startAPMode();
        }
    }
    else
    {
        setLEDColor(0, 0, 255);
        startAPMode();
    }

    setupServer();
    server.begin();
    Serial.println("✅ Server Started!");
}

void loop()
{
    server.handleClient();
    if (mqttClient.connected())
    {
        mqttClient.loop();
    }

    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval)
    {
        previousMillis = currentMillis;
        sendHealthStatus();
    }

    checkResetButton();
    checkReasonButtons();
}

void startAPMode()
{
    String apSSID = "CAC_" + getMacID();
    WiFi.softAP(apSSID.c_str(), AP_PASSWORD);
    Serial.println("📱 AP Mode Started! Connect to '" + apSSID + "' WiFi.");
    setLEDColor(0, 0, 255);
}

void connectToMQTT()
{
    mqttClient.setServer(storedMQTT.c_str(), MQTT_PORT);
    if (mqttClient.connect(deviceUUID.c_str()))
    {
        Serial.println("✅ Connected to MQTT Broker at: " + storedMQTT);
        setLEDColor(0, 255, 0);
        mqttClient.publish("test", "hello");
    }
    else
    {
        Serial.println("❌ MQTT Connection Failed!");
        setLEDColor(255, 0, 0);
    }
}

void checkReasonButtons()
{
    for (int i = 0; i < NUM_REASON_BUTTONS; i++)
    {
        int reading = digitalRead(REASON_BUTTON_PINS[i]);
        if (reading == LOW && buttonState[i] == HIGH && (millis() - lastDebounceTime[i]) > debounceDelay)
        {
            buttonState[i] = LOW;
            lastDebounceTime[i] = millis();
            sendReasonPressed(i + 1);
        }
        if (reading == HIGH)
        {
            buttonState[i] = HIGH;
        }
    }
}

void sendReasonPressed(int key_num)
{
    if (!mqttClient.connected())
    {
        connectToMQTT();
    }

    if (mqttClient.connected())
    {
        String topic = "cactus/" + deviceUUID + "/reason";
        DynamicJsonDocument doc(256);
        doc["key_num"] = key_num;
        doc["timestamp"] = millis();
        doc["orgId"] = storedOrgId;
        String message;
        serializeJson(doc, message);
        mqttClient.publish(topic.c_str(), message.c_str());
        Serial.println("📤 Sent MQTT Message: " + message);
    }
}

void sendHealthStatus()
{
    if (!mqttClient.connected())
    {
        connectToMQTT();
    }

    if (mqttClient.connected())
    {
        String topic = "cactus/" + deviceUUID + "/health";
        DynamicJsonDocument doc(256);
        doc["ping"] = 1;
        String message;
        serializeJson(doc, message);
        mqttClient.publish(topic.c_str(), message.c_str());
        Serial.println("📤 Sent MQTT Health Message: " + message);
    }
}

void setupServer()
{
    server.on("/scan", HTTP_GET, []()
              {
Serial.println("📡 Scanning WiFi...");
int n = WiFi.scanNetworks();
DynamicJsonDocument doc(1024);
JsonArray arr = doc.createNestedArray("networks");

for (int i = 0; i < n; i++) {
JsonObject net = arr.createNestedObject();
net["ssid"] = WiFi.SSID(i);
net["rssi"] = WiFi.RSSI(i);
}

String response;
serializeJson(doc, response);
server.send(200, "application/json", response); });

    server.on("/connect", HTTP_POST, []()
              {
if (!server.hasArg("plain")) {
server.send(400, "application/json", "{\"error\":\"Missing body\"}");
return;
}

DynamicJsonDocument doc(1024);
DeserializationError error = deserializeJson(doc, server.arg("plain"));
if (error) {
server.send(400, "application/json", "{\"error\":\"Invalid JSON\"}");
return;
}

String ssid = doc["ssid"];
String password = doc["password"];
String mqtt = doc["mqtt"];
String orgId = doc["orgId"];

if (ssid.isEmpty() || password.isEmpty() || mqtt.isEmpty() || orgId.isEmpty()) {
server.send(400, "application/json", "{\"error\":\"Missing ssid/password/mqtt/orgId\"}");
return;
}

Serial.println("📥 Received WiFi + MQTT + orgId:");
Serial.println("SSID: " + ssid);
Serial.println("MQTT: " + mqtt);
// Serial.println("OrgID: " + orgId);

WiFi.disconnect();
delay(2000);
WiFi.begin(ssid.c_str(), password.c_str());

int retries = 0;
while (WiFi.status() != WL_CONNECTED && retries < 20) {
delay(1000);
Serial.print(".");
retries++;
}

if (WiFi.status() == WL_CONNECTED) {
storedSSID = ssid;
storedPassword = password;
storedMQTT = mqtt;
storedOrgId = orgId;
Serial.println("💾 Saving Wi-Fi, MQTT, and OrgID.");
saveStoredData();
server.send(200, "application/json", "{\"status\":\"success\"}");
Serial.println("✅ Connection successful, restarting device...");
delay(1000);
ESP.restart();
} else {
Serial.println("❌ Wi-Fi connection failed after 20 retries");
server.send(500, "application/json", "{\"status\":\"wifi_failed\"}");
setLEDColor(255, 0, 0);
} });

    server.on("/info", HTTP_GET, []()
              {
DynamicJsonDocument doc(256);
doc["mac"] = WiFi.softAPmacAddress();
doc["orgId"] = storedOrgId;
String response;
serializeJson(doc, response);
server.send(200, "application/json", response); });

    server.begin();
    Serial.println("🌐 Server started");
}

void saveStoredData()
{
    char ssidBuf[32], passBuf[32], mqttBuf[32], orgIdBuf[32];
    storedSSID.toCharArray(ssidBuf, 32);
    storedPassword.toCharArray(passBuf, 32);
    storedMQTT.toCharArray(mqttBuf, 32);
    storedOrgId.toCharArray(orgIdBuf, 32);

    EEPROM.put(0, ssidBuf);
    EEPROM.put(32, passBuf);
    EEPROM.put(64, mqttBuf);
    EEPROM.put(96, orgIdBuf);
    EEPROM.put(128, true);
    EEPROM.commit();
}

void readStoredData()
{
    char ssidBuf[32], passBuf[32], mqttBuf[32], orgIdBuf[32];
    EEPROM.get(0, ssidBuf);
    EEPROM.get(32, passBuf);
    EEPROM.get(64, mqttBuf);
    EEPROM.get(96, orgIdBuf);
    EEPROM.get(128, isProvisioned);

    storedSSID = String(ssidBuf).c_str();
    storedPassword = String(passBuf).c_str();
    storedMQTT = String(mqttBuf).c_str();
    storedOrgId = String(orgIdBuf).c_str();

    storedSSID.trim();
    storedPassword.trim();
    storedMQTT.trim();
    storedOrgId.trim();
}

void checkResetButton()
{
    if (digitalRead(RESET_BUTTON) == LOW)
    {
        Serial.println("⏳ Reset Button Pressed! Holding...");
        delay(5000);
        if (digitalRead(RESET_BUTTON) == LOW)
        {
            Serial.println("🚀 Resetting device...");
            resetStoredData();
        }
    }
}

void resetStoredData()
{
    for (int i = 0; i < EEPROM_SIZE; i++)
    {
        EEPROM.write(i, 0);
    }
    EEPROM.commit();
    Serial.println("🧹 EEPROM Cleared! Restarting in AP mode...");
    delay(1000);
    ESP.restart();
}

String getMacID()
{
    uint8_t mac[6];
    WiFi.macAddress(mac);
    String macStr = "";
    for (int i = 0; i < 6; i++)
    {
        macStr += String(mac[i], HEX);
    }
    return macStr;
}

void setLEDColor(int red, int green, int blue)
{
    analogWrite(LED_RED, red);
    analogWrite(LED_GREEN, green);
    analogWrite(LED_BLUE, blue);
}