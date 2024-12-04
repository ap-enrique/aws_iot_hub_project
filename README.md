# Temperature and Humidity Monitoring with Arduino, Raspberry Pi, and AWS IoT Core

![IoT project overview](img/Portofolio.drawio.png)

## Table of Contents

1. Overview
2. Introduction
3. Project Components
4. System Architecture
4. Instructions
	- Step 1: Installation adn Configuration
	- Step 2: Wiring
	- Step 3: MQTT Setup
	- Step 4: Data Transmission to AWS IoT Core
6. Security
7. Scalability
8. Conclusion and Future Work


## Overview
This project uses an Arduino Uno R4 WiFi along with a DHT11 sensor to monitor temperature and humidity levels. The data collected by the sensor is transmitted via MQTT to a Raspberry Pi, which serves as the MQTT broker. The Raspberry Pi subsequently sends the data to AWS IoT Core, where it is stored in a DynamoDB table and displayed on a web page created with AWS Amplify. This configuration allows for remote monitoring of sensor data and lays a solid foundation for future enhancements.

## Introduction
The aim of this project is to showcase the use of IoT devices for gathering and analyzing environmental data. By utilizing a DHT11 sensor, an Arduino Uno R4 WiFi, and the MQTT protocol, the Arduino transmits sensor readings to a Raspberry Pi, which serves as an MQTT broker. The Raspberry Pi then relays this data to AWS IoT Core for storage and visualization.

This solution is scalable and can be enhanced with more sensors and devices to develop a complete IoT system.

## Project Components
- Hardware
	- Arduino Uno R4 WiFi: A microcontroller designed for reading sensor data and communicating through MQTT.
	- DHT11 Sensor: A device that measures temperature and humidity.
	- Raspberry Pi: Acts as the MQTT broker and serves as an intermediary to forward data to AWS IoT Core.
 - Software
 	- Arduino IDE
 	- MQTT Libraries
  	- AWS service
		- AWS IoT Core: A service that manages IoT devices and their data.
		- AWS DynamoDB: A database used for storing sensor readings.
		- AWS Lambda: A serverless function that processes data by sending over to other applications..
		- AWS Amplify: A tool for creating a web interface to visualize sensor data.

## System Architecture
- DHT11 Sensor → Arduino → MQTT Broker (Raspberry Pi) → AWS IoT Core → DynamoDB
- Visualization happens via AWS Amplify and a Lambda function to build a simple web interface.

## Instructions
### Steg 1: Downloads
1. Install Arduino IDE:
	- Download and install the latest version of the Arduino IDE.
2. Install Libraries:
	- In Arduino IDE, go to Sketch > Include Library > Manage Libraries and search for the following libraries:
		- DHT sensor library (for reading from the DHT11 sensor).
		- PubSubClient (for MQTT communication).
3. Install MQTT Broker on Raspberry Pi:
	- Install an MQTT broker such as Mosquitto on your Raspberry Pi.
4. Install AWS CLI and IoT Core SDK:
	- Follow the AWS IoT Core documentation to configure and install the AWS CLI.

### Steg 2: Connectivity

![Arduino and DHT11 Setup](img/Arduino_DHT11_Setup.png)

1. Koppla DHT11 till Arduino Uno R4 WiFi:
	- VCC to 5V.
	- SDA to pin 2.
	- GND to GND.
2. Configure MQTT in Arduino Code:
	- In main.ino, configure your MQTT server (Raspberry Pi’s IP address) and Wi-Fi settings (SSID and password).
	- Use the PubSubClient library to connect to the MQTT server and publish temperature and humidity data.

![Raspberry Pi](img/Raspberry_pi.png)

3. Configure MQTT Broker on Raspberry Pi:
	- Install Mosquitto and configure it to listen for incoming MQTT messages from the Arduino.
	- Create subscriptions for the specific topics published by the Arduino.
4. AWS IoT Core Configuration:
	- Create an IoT thing and obtain the necessary certificates and keys.
	- Use AWS IoT Core to create a rule that publishes sensor data to DynamoDB when MQTT messages are received.

### Steg 3: Statistik och Dataanalys
1. Lambda and DynamoDB:
	- Create an AWS Lambda function to handle incoming MQTT messages and write them to a DynamoDB table.
2. Visualization with AWS Amplify:
	- Build a web interface with AWS Amplify to visualize temperature and humidity data from DynamoDB.
### Security and Scalability
Use AWS IoT Core to manage authentication and authorization between all devices (Arduino, Raspberry Pi, and AWS services).

### Scalability
The project can be easily scaled by adding more sensors and devices to the system. Use AWS IoT Core rules to handle larger data volumes from multiple devices.

## Conclusion
This project showcases how basic IoT components such as the Arduino and Raspberry Pi can be utilized to develop a scalable and secure system for monitoring environmental data. By using MQTT, AWS IoT Core, DynamoDB, and AWS Amplify, a comprehensive solution is established to gather, store, and visualize sensor data in real-time. The project is designed to be easily expandable and customizable, allowing for the inclusion of more sensors and devices.
