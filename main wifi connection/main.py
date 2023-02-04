import network
import socket
import select
import json
import time

from machine import Pin
led = machine.Pin("LED", machine.Pin.OUT)
relay = Pin(18, Pin.OUT)    # 14 number in is Output

ssid = "TEST======================="
password = "TEST========================="

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
        led.toggle()
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    led.value(1)
    return ip

def ledblink():
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)
    
try:
    ip = connect()
    addr_info = socket.getaddrinfo(ip, 5005)
    addr = addr_info[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    
    while True:
        time.sleep(0.01)
        data, addr=s.recvfrom(2048)
        #print('recvfrom ' + str(addr) + ': ' + data.decode())
        print('recvfrom ' + str(addr) + ': ' + data.decode())
        print('recvfrom length:' + str(len(data)))
        listTestByte = list(data)
        print(listTestByte)
        if data[12] == 65:
            relay.value(1)
            ledblink()
        if data[12] == 66:
            relay.value(0)
            ledblink()
              
except KeyboardInterrupt:
    machine.reset()


'''
  while True:
    client.send_message("/AAA", "ABB")
    time.sleep(1)
    client.send_message("/AAA", "BBB")
    time.sleep(1)
    
    
[47, 65, 65, 65, 0, 0, 0, 0, 44, 115, 0, 0, 65, 66, 66, 0]
recvfrom ('192.168.1.102', 64255): /AAA
recvfrom length:16
[47, 65, 65, 65, 0, 0, 0, 0, 44, 115, 0, 0, 66, 66, 66, 0]
recvfrom ('192.168.1.102', 64255): /AAA
'''
