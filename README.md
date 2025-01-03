# Temperature and Humidity Monitoring with Arduino, Raspberry Pi, and AWS IoT Core

![IoT project overview](img/Portofolio.drawio.png)

## Table of Contents

1. [Overview](#overview)
2. [Introduction](#introduction)
3. [Project Components](#project-components)
4. [System Architecture](#system-architecture)
4. [Instructions](#instructions)
	- [Step 1: Installation and Configuration](#step-1-installation-and-configuration)
	- [Step 2: Wiring](#step-2-wiring)
	- [Step 3: Connectivity](#step-3-connectivity)
	- [Step 4: Data Transmission to AWS IoT Core](#step-4-data-transmission-to-aws-iot-core)
	- [Step 5: Data Storage](#step-5-data-storage)
	- [Step 6: Data Visualization](#step-6-data-visualization)
6. [Security](#security)
7. [Scalability](#scalability)
8. [Conclusion](#conclusion)
9. [Future Work](#future-work)


## Overview
This project uses an Arduino Uno R4 WiFi along with a DHT11 sensor to monitor temperature and humidity levels. The data collected by the sensor is transmitted via MQTT to a Raspberry Pi, which serves as the MQTT broker. The Raspberry Pi subsequently sends the data to AWS IoT Core, where it is stored in a DynamoDB table and displayed on a web page created with AWS Amplify. This configuration allows for remote monitoring of sensor and visualized using AWS Amplify and Grafana. The architecture is designed for scalability and secure operations, and lays a solid foundation for future enhancements.

## Introduction
### Purpose
- This IoT project focuses on real-time monitoring of temperature and humidity using an Arduino Uno R4 WiFi paired with a DHT11 sensor.
- The system utilizes MQTT for transmitting data to a Raspberry Pi, which subsequently sends the information to AWS IoT Core for storage and visualization.
- Build a scalable, secure, and user-friendly system for cloud-based visualization and analytics.

### Who Can Use This Project?
- Home Users: Keep track of indoor environments, including home climate, greenhouses, or server rooms.
- Industrial Users: Monitor conditions in warehouses, factories, or data centers to ensure quality control and safety compliance.
- Developers & Hobbyists: Explore and experiment with IoT concepts, data collection, and cloud integration.

### Potential Use Cases
- Home Automation: Control heating, cooling, or humidifiers based on real-time data.
- Industrial Monitoring: Maintain optimal environmental conditions for sensitive equipment or products.
- Data Analytics: Examine historical data for trends and predictive maintenance.
- Educational Purposes: Provide instruction on IoT, cloud integration, and data visualization techniques.

## Project Components
- Hardware
	- Arduino Uno R4 WiFi: A microcontroller designed for reading sensor, collects data and communicating through MQTT.
	- DHT11 Sensor: A device that measures temperature and humidity.
	- Raspberry Pi: Acts as the MQTT broker and serves as an intermediary to forward data to AWS IoT Core.
 - Software
 	- Arduino IDE for programming the Arduino.
 	- Mosquitto MQTT Broker on Raspberry Pi for data relay.
  	- AWS service
		- AWS IoT Core: A cloud communication service that manages IoT devices and their data.
		- AWS DynamoDB: A database used for storing sensor readings.
		- AWS Lambda: A serverless function that processes data by sending over to other applications.
		- AWS Amplify: A tool for creating a frontend web interface to visualize sensor data.
		- Grafana för advanced dashboard capabilities.

## System Architecture
### Data Flow
- DHT11 Sensor → Arduino Uno R4 Wifi
- Arduino → MQTT Broker (Raspberry Pi)
- Raspberry Pi → AWS IoT Core
- AWS IoT Core → DynamoDB and Amplify

### Visualization Options
1. Grafana: Real-time, multi-sensor dashboards for industrial use.
2. AWS Amplify: A user-friendly web portal for home monitoring.

## Instructions
### Step 1: Installation and Configuration
- Install Arduino IDE:
	- Download and install the latest version of the Arduino IDE.
- Install Libraries:
	- In Arduino IDE, go to Sketch > Include Library > Manage Libraries and search for the following libraries:
		- DHT sensor library (for reading from the DHT11 sensor).
		- PubSubClient (for MQTT communication).
  		- ArduinoJson
- Install MQTT Broker on Raspberry Pi:
	- Install an MQTT broker such as Mosquitto on your Raspberry Pi.
	```
 	sudo apt-get update
 	sudo apt-get install mosquitto mosquitto-clients
 	``` 

### Step 2: Wiring

![Arduino and DHT11 Setup](img/Arduino_DHT11_Setup.png)
Connect to the DHT11 to the Arduino Uno R4 WiFi as follow:
- VCC → 5V on Arduino
- SDA → Pin 2 on Arduino
- GND → GND on Arduino
  
### Step 3: Connectivity
1. Configure MQTT in Arduino Code:
	- In main.ino, configure your MQTT server (Raspberry Pi’s IP address) and Wi-Fi settings (SSID and password) at (`arduino_secrets.h`). 
	- Use the PubSubClient library to connect to the MQTT server and publish temperature and humidity data.
	- Ensure data is sent in JSON format

	```
 	{
 		"device": "MAC_ADDRESS",
  		"temperature": 24.2,
  		"humidity": 34
 	}
	```

![Raspberry Pi](img/Raspberry_pi.png)

2. Configure MQTT Broker on Raspberry Pi:
	- Install Mosquitto and configure it to listen for incoming MQTT messages from the Arduino.
    	```
     	sudo apt-get update
     	sudo apt-get install mosquitto mosquitto-clients
     	```
	- Configure the MQTT broker for the local network.
 	- Use the following configuration in main.ino
    	```
     	mqtt_server = "192.168.x.x"; // Replace with Raspberry Pi IP address 
     	```
	- Create subscriptions for the specific topics published by the Arduino.

### Step 4: Data Transmission to AWS IoT Core
- AWS IoT Core Setup:
	- Configure the Raspberry Pi to forward MQTT messages to AWS
	- Register your device (Raspberry Pi) in AWS IoT Core.
 	- Download the device certificates.
	- Establish a secure connection using policies and certificates.
 	- Attach an IoT policy that allows publishing to a specific topic.
 	- Send data in JSON format with the following structure:
    	```
     	{
  		"device": "MAC_ADDRESS",
  		"temperature": 24.2,
  		"humidity": 34
     	}
     	```
- AWS Service:
	- Set up AWS IoT Core
	- Create an IoT thing and obtain the necessary certificates and keys.
	- Create a DynamoDB Table to store the data
 		- Create a table with `device_id` (Partition Key) and `timestamp` (Sort Key).
	- Use AWS IoT Core to create a rule that allow writing publishes sensor data to DynamoDB when MQTT messages are received.
	- Configure a Lambda function for data handling
 		- Create an AWS Lambda function to handle incoming MQTT messages.
   		- Write a Node.js function to handle data insertion into DynamoDB table
     		- Create an AWS Lambda function to handle http get requet.

## Step 5: Data Storage
- DynamoDB is used in this project for storing real-time sensor data.
	- Dynamo is good for the project because of the low-latency for reads and writes.
	- Automatically scales to handle spikes in traffic.
	- Works well for unstructured or semi-structured data like JSON
	- DynamoDB integrates seamlessly with AWS IoT Core rules, allowing automatic data insertion without additional infrastructure.
- Amazon S3 can also be employed as a supplementary or alternative storage option.
	- Long-term storage of historical data or logs.
	- Central repository for structured and unstructured data for analytics.
	- Hosting static files like HTML, CSS, and JavaScript.
	- Storing connect/disconnect events or debugging logs for IoT devices.
 	- Storing images, videos, or other multimedia content.
- Although S3 is not implemented in this project, it remains a viable option for future enhancements where long-term storage or event logging is required.
- Other Storage Options
	- AWS Options
		- Amazon RDS
		- Amazon Redshift
		- Amazon Timestream
		- Amazon Elasticsearch/OpenSearch
		- AWS Glue Data Catalog
  	- Others
		- InfluxDB
  		- MongoDB
  	 	- Google Cloud Storage
  	  	- SQLite or Local File Storage

### Step 6: Data Visualization
- You can visualize the collected data for both industrial and home users
- Grafana is ideal for industrial use cases due to its real-time monitoring capabilities and ability to handle complex dashboards with multiple data sources.
	- Configure Grafana to pull data from AWS IoT Core or DynamoDB using a infinity plugin or custom integration.
	- Create dashboards to visualize temperature and humidity trends over time.
 	- Usage:
		- Industrial users can monitor multiple sensors and locations with alerts for critical conditions

![Grafana Humidity](img/Grafana_Humidity.png)
![Grafana Temperature](img/Grafana_Tempereture.png)
![Grafana Dashboard](img/Grafana_Dashboard.png)

- Amplify provides a simple, user-friendly web interface, making it perfect for home users who need easy access to data from any device.
	- Deploy a frontend web application using AWS Amplify.
	- Use GraphQL or REST APIs to fetch data from DynamoDB.
	- Customize the UI to show real-time temperature and humidity updates.
 	- Usage:
		- Home users can log in to a web portal and view current conditions, historical data, and basic analytics.
![Wepage visualization on PC webbrowser with React app and Amplify](img/Webbrowser_screenshoot.png)
![Mobile phone visualization on Phone webbrowser with React app and Amplify](img/Mobile_screenshoot.jpg)

### Security
- Protect sensitive data: Use `arduino_secrets.h` and `pi_secrets.py`.
- Secure MQTT connections using TLS certificates.
- Use AWS IoT Core to manage authentication and authorization between all devices (Arduino, Raspberry Pi, and AWS services).

### Scalability
- The project can be easily scaled by adding more sensors and devices to the system.
- Use AWS IoT Core rules to handle larger data volumes from multiple devices.

### Conclusion
This project demostrate how basic IoT components such as the Arduino and Raspberry Pi can be utilized to develop a scalable and secure system for monitoring environmental data. By using MQTT, AWS IoT Core, DynamoDB, and AWS Amplify, a comprehensive solution is established to gather, store, and visualize sensor data in real-time. The project is designed to be easily expandable and customizable, allowing for the inclusion of more sensors and devices.

### Future Work
1. Mobile App Development: Build an app for easier monitoring on the go.
2. Machine Learning: Use historical data for predictive analytics.
3. Extended Sensor Network: Add sensors for air quality or light levels.
