import machine
import time
import ubinascii

led =  machine.Pin('LED', machine.Pin.OUT)

    
def blink_fast():
    while True:
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)

def blink_slow():
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

        

import network
import usocket as socket

# Function to start Access Point (AP) mode
def start_ap(ssid, password):
    print("start ap!!")
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    
    while ap.active() == False:
        pass
    print("Ap mode is active, IP:"+ ap.ifconfig()[0])
    print("MAC:"+ mac)


# Function to stop Access Point (AP) mode
def stop_ap():
    print("stop ap!")
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    blink_slow()

# Function to handle HTTP requests
def handle_request(client_socket):
    print("handle_request()")
    request = client_socket.recv(1024)
    request_str = str(request)
    
    print("request_str=")
    print(request_str)
    # Check if the request is a GET request
    # if request_str.find('GET /ssid_password') != -1:
    if request_str.find('GET / HTTP') != -1 :
        # Send HTML form to set SSID and password
        
        html = """<!DOCTYPE html>
                <html>
                <body>
                <h2>Set SSID and Password</h2>
                <form action="/save_settings" method="post">
                SSID:<br>
                <input type="text" name="ssid"><br>
                Password:<br>
                <input type="password" name="password"><br><br>
                <input type="submit" value="Save">
                </form> 
                </body>
                </html>"""
        
        '''
        html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body><h1>Hello World</h1></body></html>
        """
        '''
        client_socket.send(html)
    # Check if the request is a POST request to save settings
    elif request_str.find('POST /save_settings') != -1:
        print("===========save_settings=======")
        # Parse SSID and password from the request
        ssid_start = request_str.find('ssid=') + 5
        ssid_end = request_str.find('&', ssid_start)
        ssid = request_str[ssid_start:ssid_end]
        password_start = request_str.find('password=') + 9
        password = request_str[password_start:-1]
        
        # Start Access Point mode with new SSID and password
        print("ssid="+ssid)
        print("password="+password)
        #stop_ap()
        #start_ap(ssid, password)
        do_connect(ssid,password)
        # Send response indicating settings saved
        #response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
        #            <html><body><h2>Settings saved successfully. Rebooting...</h2></body></html>"""
        #client_socket.send(response)
        
        # Delay to allow response to be sent before rebooting
        #import time
        #time.sleep(2)
        
        # Reboot the device
        #import machine
        #machine.reset()
    else:
        # Send 404 Not Found response for any other requests
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        client_socket.send(response)

def do_connect(ssid, key):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid,key)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    blink_fast()

# Main function
def main():
    # Start Access Point mode
    start_ap("Pico_AP_TEST", "password123")

    # Create socket and start listening for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)

    # init led
    led.on()
    
    # Main loop to handle incoming connections
    while True:
        client_socket, addr = server_socket.accept()
        handle_request(client_socket)
        client_socket.close()

if __name__ == '__main__':
    main()


