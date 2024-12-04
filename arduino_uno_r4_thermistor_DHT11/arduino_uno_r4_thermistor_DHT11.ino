#include <DHT.h>
#include <WiFi.h>
#include <MQTT.h>
#include <ArduinoJson.h>
#include "arduino_secrets.h" // För WiFi- och MQTT-uppgifter

// Konstanter och inställningar
#define DHTPIN 2           // Pin var sensorn är ansluten
#define DHTTYPE DHT11      // Typ av sensor
#define SENSOR_READ_INTERVAL 10000 // Delay mellan avläsningar i millisekunder

String THINGNAME = "";

// Skapa MQTT-klienten
WiFiClient net;
MQTTClient mqttClient(256); // Skapar en MQTT-klient med buffert på 256 byte

// Skapa DHT-objekt
DHT dht(DHTPIN, DHTTYPE);

// Funktioner
void printMacAddress(byte mac[]) {
    for (int i = 0; i < 6; i++) {
        if (i > 0) Serial.print(":");
        Serial.print(mac[i], HEX); // Skriv ut varje byte i hex
    }
    Serial.println();
}

void connectToWiFi() {
    char ssid[] = SECRET_SSID;
    char pass[] = SECRET_PASS;

    Serial.println("Försöker ansluta till WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        WiFi.begin(ssid, pass);
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\nWiFi anslutet!");
    Serial.print("IP-adress: ");
    Serial.println(WiFi.localIP());

    byte mac[6];
    WiFi.macAddress(mac);  // Get MAC address

    // Convert MAC address to String (without colons)
    THINGNAME = "";
    for (int i = 0; i < 6; i++) {
        THINGNAME += String(mac[i], HEX);
    }

    Serial.print("MAC-adress: ");
    printMacAddress(mac); // This function still takes byte array as argument
}

void setupMQTT(MQTTClient& client, WiFiClient& net) {
    client.begin(mqttServer, mqttPort, net);

    while (!client.connect("ArduinoR4Client")) {
        Serial.println("Ansluter till MQTT-broker...");
        delay(1000);
    }
    Serial.println("Ansluten till MQTT!");
}

void mqttLoop(MQTTClient& client) {
    if (!client.connected()) {
        Serial.println("MQTT-anslutning tappad, försöker återansluta...");
        while (!client.connect("ArduinoR4Client")) {
            Serial.println("Återansluter...");
            delay(1000);
        }
        Serial.println("MQTT återanslutet!");
    }
    client.loop();
}

void sendToMQTT(MQTTClient& client, float temperature, float humidity, String status) {
    // Skicka temperatur
    StaticJsonDocument<256> tempDoc;
    tempDoc["device_id"] = THINGNAME;  // Use device's MAC address as ID
    tempDoc["temperature"] = temperature;
    char tempBuffer[256];
    serializeJson(tempDoc, tempBuffer);
    client.publish(AWS_IOT_PUBLISH_TOPIC, tempBuffer);

    // Skicka luftfuktighet
    StaticJsonDocument<256> humDoc;
    humDoc["device_id"] = THINGNAME;
    humDoc["humidity"] = humidity;
    char humBuffer[256];
    serializeJson(humDoc, humBuffer);
    client.publish(AWS_IOT_PUBLISH_TOPIC, humBuffer);

    // Skicka status
    StaticJsonDocument<256> statusDoc;
    statusDoc["device_id"] = THINGNAME;
    statusDoc["status"] = status;
    char statusBuffer[256];
    serializeJson(statusDoc, statusBuffer);
    client.publish(AWS_IOT_PUBLISH_TOPIC, statusBuffer);

    // Skicka sammanställd data till "telemetry"
    StaticJsonDocument<512> telemetryDoc;
    telemetryDoc["device_id"] = THINGNAME;
    telemetryDoc["temperature"] = temperature;
    telemetryDoc["humidity"] = humidity;
    telemetryDoc["status"] = status;
    char telemetryBuffer[512];
    serializeJson(telemetryDoc, telemetryBuffer);
    client.publish(AWS_IOT_PUBLISH_TOPIC, telemetryBuffer);
}

void messageReceived(String &topic, String &payload) {
    Serial.println("Meddelande mottaget:");
    Serial.print("Ämne: ");
    Serial.println(topic);
    Serial.print("Payload: ");
    Serial.println(payload);
}

void setupSubscriptions(MQTTClient &client) {
    if (client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC)) {
        Serial.println("Prenumererar på: " AWS_IOT_SUBSCRIBE_TOPIC);
    }
}

bool readSensorData(DHT& dht, float& temperature, float& humidity) {
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("Fel: Kunde inte läsa från DHT-sensorn.");
        return false;
    }
    return true;
}

void printDataToSerial(float temperature, float humidity, String status) {
    Serial.print("Temperatur: ");
    Serial.print(temperature);
    Serial.print(" °C, Luftfuktighet: ");
    Serial.print(humidity);
    Serial.print(" %, Status: ");
    Serial.println(status);
}

// Setup och loop
void setup() {
    Serial.begin(115200);
    dht.begin();
    connectToWiFi();
    setupMQTT(mqttClient, net);
    mqttClient.onMessage(messageReceived);
    setupSubscriptions(mqttClient);
}

void loop() {
    if (!mqttClient.connected()) {
        setupMQTT(mqttClient, net);
        setupSubscriptions(mqttClient);
    }

    mqttLoop(mqttClient);

    float temperature, humidity;
    String status = "on"; // För test kan vi låta status vara "on" som standard

    if (readSensorData(dht, temperature, humidity)) {
        printDataToSerial(temperature, humidity, status);
        sendToMQTT(mqttClient, temperature, humidity, status);
    }

    delay(SENSOR_READ_INTERVAL);
}
