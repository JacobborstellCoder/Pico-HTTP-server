# Simple HTTP Server Module

import time
import network
import socket

def gtparam(par, keydat):
    if keydat in par:
        return par[keydat]
    return None

def server_handeler(ssid, password, con_handeler, connection_max_retries=10, debug=False, port=80):
    print("Starting server. DEBUG: " + {False: 'OFF', True: 'ON'}[debug])
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)


    # Try to connect to WiFi
    print('Connecting...')
    while connection_max_retries:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        connection_max_retries -= 1
        time.sleep(1)
    
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed.')
    else:
        status = wlan.ifconfig()
        print('Connection successful, Running on ip:', status[0], ', port:80')
        print(status[0])
        
        
    # Open socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)

    # Listen for connections
    while True:
        try:       
            cl, addr = s.accept()
            request = cl.recv(1024)
            if debug:
                print("Request:", '\n', request, '\n')
                print('Client connected from:', addr)
            request = str(request)
            if request[:18] == "b'GET /favicon.ico":
                response = 'favicon request, placeholder'
            else:
                location = ''
                params = {}
                url = request[6:request.find(" HTTP/")]
                if url.find("?") != -1:
                    location, param_inp = url.split("?")
                    paramslist = param_inp.split("&")
                    for prm in paramslist:
                        var, val = prm.split("=")
                        params[var] = val
                else:
                    location = url
                if debug:
                    print('Path:', location, 'Query:', params)
                response = con_handeler(location, params)
            
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            
        except OSError as e:
            cl.close()
            print('connection closed')

