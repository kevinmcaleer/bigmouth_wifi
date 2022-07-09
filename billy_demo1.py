from billy import Billy
from time import sleep
import network
from secret import ssid, password
from machine import Pin
import uasyncio as asyncio
import socket

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    print(".", end="")
print(wlan.status())

html = """
<!DOCTYPE html>
<html>
    <head>
    <title>Billy Bass</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    </head>
        <body>
        <div class="container mt-3">
        <h1>Big Mouth Billy Bass</h1>
        <img class="w-50 mt-3" src="http://www.kevsrobots.com/assets/img/bigmouthbillybass/fish01.jpg">
    <p>%s</p>
        </div>
    </body>
</html>
"""
onboard = Pin("LED", Pin.OUT, value=0)

billy = Billy()

async def serve_client(reader, writer):
    global billy
    print("Client Connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line)
    led_on = request.find('/head/out')
    led_off = request.find('/head/in')
    
    stateis = ""
    if led_on ==6:
        print("Billy Says Hello")
#         led.va##lue(1)
        billy.head_out()
        stateis = "Billy's Head is OUT"
        
    if led_off == 6:
        print("Billy says Bye")
#         led_value(0)
        billy.head_in()
        stateis = "Billy's Head is IN"
        
    response = html % stateis
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')
    
async def main():
    print ("setting up webserver")
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        onboard.on()
        print("heartbeat")
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)
           



billy.reset()
sleep(1)

billy.head_out()
billy.tail_out()
sleep(0.5)
for _ in range(1, 1):
    billy.mouth_open()
    sleep(0.0001)
    billy.mouth_close()
    sleep(0.0001)
billy.tail_in()
billy.head_in()

billy.flap_tail(2)
# billy.head_out()
# sleep(2)
# billy.head_in()

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()