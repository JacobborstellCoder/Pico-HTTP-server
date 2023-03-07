from lan_mod import server_handeler, gtparam
from machine import Pin


led = Pin("LED", Pin.OUT)


def main(loc, params):
    if gtparam(params, 'led') == "on":
        led.value(1)
    
    elif gtparam(params, 'led') == "off":
        led.value(0)
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pico hosted webpage</title>
    <style>
        body {
            text-align: center;
        }
        h1 {
            font-family: "Times New Roman", Times, serif;
        }
        p, a {
            font-size: 200%;
        }
    </style>
</head>
<body>
    <h1>
        Pico hosted webpage
    </h1>
    <p>
        This webpage is hosted by an raspberry pi
    </p>
    <a href="/?led=on">
        Turn on led
    </a>
    <br>
    <br>
    <a href="/?led=off">
        Turn off led
    </a>
</body>
</html>
    """

server_handeler("<SSID>", "<Password>", main, debug=False)
