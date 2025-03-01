import network
import socket

from machine import Pin
from time import sleep, sleep_ms
from microdot import Microdot, Response

import json
import _thread  # For running the reconnection logic in a separate thread

pressed_times = 0

ssid = 'your-ssid-name'
password = 'your-wifi-password'
hostname = "your-preferred-hostname"

relayPin = Pin(2, Pin.OUT)
relayPin.value(1)

network.hostname(hostname)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect():
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print('Waiting for connection...')
            sleep(1)
        print(f'Connected to Wi-Fi on {wlan.ifconfig()[0]}')

def reconnect_loop():
    while True:
        if not wlan.isconnected():
            print('Wi-Fi disconnected. Reconnecting...')
            connect()
        sleep(5)  # Check every 5 seconds

# Start Wi-Fi connection
try:
    connect()
except KeyboardInterrupt:
    machine.reset()

# Start the reconnection loop in a separate thread
_thread.start_new_thread(reconnect_loop, ())

network.hostname(hostname)

app = Microdot()

@app.route('/')
def index(request):
    try:
        with open('index.html', 'r') as f:
            html = f.read()
        return Response(html, headers={'Content-Type': 'text/html'})
    except Exception as e:
        return Response(f"Error loading index.html: {e}", status_code=500)

# Serve script.js
@app.route('/script.js')
def serve_script(request):
    try:
        with open('script.js', 'r') as f:
            content = f.read()
        return Response(content, headers={'Content-Type': 'application/javascript'})
    except Exception as e:
        return Response(f"Error loading script.js: {e}", status_code=404)

# Serve styles.css
@app.route('/styles.css')
def serve_styles(request):
    try:
        with open('styles.css', 'r') as f:
            content = f.read()
        return Response(content, headers={'Content-Type': 'text/css'})
    except Exception as e:
        return Response(f"Error loading styles.css: {e}", status_code=404)

@app.route('/press_button', methods=['GET'])
def press_button(request):
    relayPin.value(0)  
    sleep(0.5)  
    relayPin.value(1)  
    return Response(json.dumps({'status': 'success', 'message': 'Button Pressed'}), 
                    headers={'Content-Type': 'application/json'}, status_code=200)

@app.route('/hold_button', methods=['GET'])
def hold_button(request):
    relayPin.value(0)
    return Response(json.dumps({'status': 'success', 'message': 'holding...'}), 
                    headers={'Content-Type': 'application/json'}, status_code=200)

@app.route('/release_button', methods=['GET'])
def release_button(request):
    relayPin.value(1)
    return Response(json.dumps({'status': 'success', 'message': 'Button released.'}), 
                    headers={'Content-Type': 'application/json'}, status_code=200)

print('hostname=', network.hostname())

app.run(debug=True, host='0.0.0.0', port=80)

