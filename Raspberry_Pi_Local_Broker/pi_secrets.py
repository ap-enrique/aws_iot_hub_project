# pi_secrets.py

# Paths to AWS certificates and keys
AWS_PRIVATE_KEY_PATH = "/FULLPATH/xxxxxx.pem.key"
AWS_DEVICE_CERT_PATH = "/FULLPATH/xxxxxx.crt"
AWS_ROOT_CA_PATH = "/FULLPATH/xxxxxxxxxx.pem"

# AWS IoT Core configurations
AWS_ENDPOINT = "END_POINT_FROM_AMAZON"
AWS_PORT = 8883

# Local MQTT topics
ARDUINOR4_TOPIC_TELE = "/telemetry/34B7DA62367C"  # Set manuallt based on device ID
ARDUINOR4_TOPIC_DOWNLINK = "/downlink"

# Placeholder AWS MQTT topics
AWS_TOPIC_DOWNLINK = "aws/downlink"  # for AWS-kommandon

# AWS IoT Core topics
AWS_TOPIC_BASE = "aws/telemetry"
AWS_TOPIC_DOWNLINK = "command/downlink"


