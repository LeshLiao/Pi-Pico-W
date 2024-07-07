import network
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
import ussl

# MQTT Configuration
BROKER = '"37184674a10f4f9293052a4bbd9a4f13.s1.eu.hivemq.cloud"'  # Replace with your MQTT broker's IP or hostname
PORT = 8883
#CLIENT_ID = ubinascii.hexlify(machine.unique_id())
CLIENT_ID = "myPicoClientId0707"
TOPIC = b'encyclopedia/temperature'

# Function to connect to WiFi
def connect_wifi():
    with open('data.json') as f:
        data = json.load(f)
        ssid = data['WIFI_SSID']
        password = data['WIFI_PASSWORD']

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to network...')
        time.sleep(1)
    print('Connected to WiFi')
    print('IP address:', wlan.ifconfig()[0])

# Function to publish a message
def publish_message(client, msg):
    client.publish(TOPIC, msg)
    print(f'Published: {msg}')

try:
    # Connect to WiFi
    connect_wifi()

    # Connect to MQTT Broker
    #client = MQTTClient(CLIENT_ID, BROKER, PORT)
    client = MQTTClient(client_id=b"myPicoClientId0707",
    server=b"37184674a10f4f9293052a4bbd9a4f13.s1.eu.hivemq.cloud",
    port=8883,
    user=b"myUser",
    password=b"!!Aa12345678",
    keepalive=0,
    ssl=True
    )
    
    client.connect()
    print('Connected to MQTT Broker')

    while True:
        publish_message(client, b'Hello World from pico')
        time.sleep(3)

except KeyboardInterrupt:
    print('Disconnected from MQTT Broker')
    client.disconnect()