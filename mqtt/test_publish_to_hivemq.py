import network
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json

# Update MicroPython: Tools-> Options -> Interpreter -> Install or update Micropython
# Choosing this Pico W (with Pimoroni libraries) version to support ussl

# MQTT Parameters
ssid = ""
password = ""
mqtt_server = ""
mqtt_port = 0
mqtt_user = ""
mqtt_password = ""
mqtt_client_id = ""

MQTT_KEEPALIVE = 7200
MQTT_SSL = True   # set to False if using local Mosquitto MQTT broker
#MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

MQTT_TOPIC_TEMPERATURE = 'encyclopedia/temperature'

def load_secret_data():
    global ssid, password, mqtt_server, mqtt_port, mqtt_user, mqtt_password, mqtt_client_id
    
    with open('data.json') as f:
        data = json.load(f)
        ssid = data['WIFI_SSID']
        password = data['WIFI_PASSWORD']
        mqtt_server = data['MQTT_SERVER']
        mqtt_port = int(data['MQTT_PORT'])
        mqtt_user = data['MQTT_USER']
        mqtt_password = data['MQTT_PASSWORD']
        mqtt_client_id = data['MQTT_CLIENT_ID']
        
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("ssid="+ssid)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to network...')
        time.sleep(1)
    print('Connected to WiFi')
    print('IP address:', wlan.ifconfig()[0])






# Function to publish a message
def publish_message(client, msg):
    client.publish(MQTT_TOPIC_TEMPERATURE, msg)
    print(f'Published: {msg}')

def connect_mqtt():
    try:
        client = MQTTClient(client_id=mqtt_client_id,
                            server=mqtt_server,
                            port=mqtt_port,
                            user=mqtt_user,
                            password=mqtt_password,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params={'server_hostname': mqtt_server})
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback


try:
    load_secret_data()
    connect_wifi()
    myClient = connect_mqtt()
    print('Connected to MQTT Broker')
    i = 0
    while True:
        publish_message(myClient, b'Hello World from pico ' + str(i))
        i = i + 1
        time.sleep(3)

except KeyboardInterrupt:
    print('Disconnected from MQTT Broker')
    client.disconnect()
