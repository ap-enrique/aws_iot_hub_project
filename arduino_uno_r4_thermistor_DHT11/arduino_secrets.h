#ifndef ARDUINO_SECRETS_H
#define ARDUINO_SECRETS_H

// WiFi-konfiguration
#define SECRET_SSID "xxxxxxxxxx"      // WiFi-namn
#define SECRET_PASS "xxxxxxxxxxxx"         // WiFi-lösenord

// The MQTT topics that this device should publish/subscribe
#define AWS_IOT_PUBLISH_TOPIC "/telemetry"
#define AWS_IOT_SUBSCRIBE_TOPIC "/downlink"

// MQTT-konfiguration
const char* mqttServer = "192.168.xxx.xxx";        // MQTT-serverns IP-adress
const int mqttPort = 1883;                       // MQTT-port

#endif
