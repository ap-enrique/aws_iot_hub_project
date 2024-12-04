#ifndef ARDUINO_SECRETS_H
#define ARDUINO_SECRETS_H

// WiFi-konfiguration
#define SECRET_SSID "TP-Link_3C90"      // WiFi-namn
#define SECRET_PASS "97135302"         // WiFi-lösenord

// The MQTT topics that this device should publish/subscribe
#define AWS_IOT_PUBLISH_TOPIC "/telemetry"
#define AWS_IOT_SUBSCRIBE_TOPIC "/downlink"

// MQTT-konfiguration
const char* mqttServer = "192.168.0.129";        // MQTT-serverns IP-adress
const int mqttPort = 1883;                       // MQTT-port

#endif
