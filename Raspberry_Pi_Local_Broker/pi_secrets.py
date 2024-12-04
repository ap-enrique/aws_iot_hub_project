# pi_secrets.py

# Paths to AWS certificates and keys
AWS_PRIVATE_KEY_PATH = "/home/admin/Nackademin/IoTcloud/mqtt_aws_connectivity/Aws_Certs_Keys_Perm/0136858dc4d2c51b43a6ac4457e7f0bd55707e098948de41ddf8e9e8ab1ff8db-private.pem.key"
AWS_DEVICE_CERT_PATH = "/home/admin/Nackademin/IoTcloud/mqtt_aws_connectivity/Aws_Certs_Keys_Perm/0136858dc4d2c51b43a6ac4457e7f0bd55707e098948de41ddf8e9e8ab1ff8db-certificate.pem.crt"
AWS_ROOT_CA_PATH = "/home/admin/Nackademin/IoTcloud/mqtt_aws_connectivity/Aws_Certs_Keys_Perm/AmazonRootCA1.pem"

# AWS IoT Core configurations
AWS_ENDPOINT = "a1ua6ksyseld-ats.iot.eu-north-1.amazonaws.com"
AWS_PORT = 8883

# Local MQTT topics
ARDUINOR4_TOPIC_TELE = "/telemetry/34B7DA62367C"  # Set dynamically based on device ID
ARDUINOR4_TOPIC_DOWNLINK = "/downlink"

# Placeholder AWS MQTT topics
AWS_TOPIC_DOWNLINK = "aws/downlink"  # AWS-kommandon

# AWS IoT Core topics
AWS_TOPIC_BASE = "aws/telemetry"
AWS_TOPIC_DOWNLINK = "command/downlink"


