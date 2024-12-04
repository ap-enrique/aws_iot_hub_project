import paho.mqtt.client as mqtt
import ssl
import json
from pi_secrets_test import (
    AWS_PRIVATE_KEY_PATH,
    AWS_DEVICE_CERT_PATH,
    AWS_ROOT_CA_PATH,
    AWS_ENDPOINT,
    AWS_PORT,
    ARDUINOR4_TOPIC_TELE,  # Device telemetry topic
    AWS_TOPIC_BASE,  # AWS base topic
    AWS_TOPIC_DOWNLINK
)

# Spåra senaste publicerade data för att undvika redundans
last_published_data = {}

def publish_to_aws(client, topic, payload):
    """
    Publicera data till AWS IoT Core utan att kontrollera för redundans.
    """
    try:
        result = client.publish(topic, payload, qos=0)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Publicerat till AWS IoT Core: Ämne: {topic}, Payload: {payload}")
        else:
            print(f"Misslyckades att publicera till AWS IoT Core: {topic}")
    except Exception as e:
        print(f"Fel vid publicering till AWS IoT Core: {str(e)}")


# Lokala MQTT-händelsehanterare
def on_local_broker_connect(client, userdata, flags, rc):
    print(f"Ansluten till lokal MQTT-broker: {rc}")
    client.subscribe([
        (ARDUINOR4_TOPIC_TELE, 0)  # We only care about telemetry topic
    ])

def on_local_broker_message(client, userdata, msg):
    print(f"Nytt meddelande från lokal MQTT-broker: Ämne: {msg.topic}, Payload: {msg.payload.decode()}")

    # Försök att publicera till AWS IoT Core
    if userdata and "aws_client" in userdata:
        aws_client = userdata["aws_client"]
        payload = msg.payload.decode()

        # Försök att parsa JSON-payload
        try:
            data = json.loads(payload)
            device_id = data.get("device_id")  # Extract device ID from payload
            if device_id:
                # Dynamically create topic using device-id
                aws_topic = f"{AWS_TOPIC_BASE}/{device_id}"

                # Debugging: Check the dynamically created topic
                print(f"Dynamically created AWS topic: {aws_topic}")

                # Publish telemetry data (whole payload)
                publish_to_aws(aws_client, aws_topic, payload)
            else:
                print("Ingen device_id i payload!")

        except json.JSONDecodeError as e:
            print(f"Fel vid parsning av JSON: {e}")
    else:
        print("AWS klient inte tillgänglig i userdata!")

# AWS MQTT-händelsehanterare
def on_aws_connect(client, userdata, flags, rc):
    print(f"Ansluten till AWS IoT Core: {rc}")
    client.user_data_set({"local_broker_client": userdata["local_broker_client"]})
    client.subscribe(AWS_TOPIC_DOWNLINK)


def on_aws_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Nytt meddelande från AWS IoT Core: Ämne: {topic}, Payload: {payload}")
    if topic == AWS_TOPIC_DOWNLINK:
        userdata["local_broker_client"].publish(ARDUINOR4_TOPIC_DOWNLINK, payload)
        print(f"Vidarebefordrade nedlänksmeddelande till Arduino R4: {payload}")

# Huvudfunktion
def main():
    # Skapa klient för lokal MQTT-broker
    local_broker_client = mqtt.Client()
    local_broker_client.on_connect = on_local_broker_connect
    local_broker_client.on_message = on_local_broker_message

    # Skapa klient för AWS IoT Core
    aws_client = mqtt.Client()
    aws_client.on_connect = on_aws_connect
    aws_client.on_message = on_aws_message

    # Sätt korrekt userdata för både AWS och lokal broker
    aws_client.user_data_set({"local_broker_client": local_broker_client})
    local_broker_client.user_data_set({"aws_client": aws_client})

    # Konfigurera TLS för AWS IoT Core
    aws_client.tls_set(
        AWS_ROOT_CA_PATH,
        AWS_DEVICE_CERT_PATH,
        AWS_PRIVATE_KEY_PATH,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

    # Anslut till AWS IoT Core
    print("Ansluter till AWS IoT Core...")
    aws_client.connect(AWS_ENDPOINT, AWS_PORT)

    # Anslut till lokal MQTT-broker
    print("Ansluter till lokal MQTT-broker...")
    local_broker_client.connect("192.168.0.129", 1883)

    # Starta loopar för båda klienterna
    aws_client.loop_start()  # AWS-klient körs i separat tråd
    local_broker_client.loop_forever()  # Lokal broker körs i huvudtråden

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stänger av...")

