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


f = open("index.html","r")
html = f.read()
f.close()

onboard = Pin("LED", Pin.OUT, value=0)

billy = Billy()
stateis = ""

async def serve_client(reader, writer):
    global billy, stateis
    print("Client Connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line)
    head_out = request.find('/head/out')
    head_in = request.find('/head/in')
    mouth_open = request.find('/mouth/open')
    mouth_close = request.find('/mouth/close')
    tail_out = request.find('/tail/out')
    tail_in = request.find('/tail/in')
    
   
    if head_out == 6:
        billy.head_out()
        stateis = "Billy's Head is OUT"
        
    if head_in == 6:
        billy.head_in()
        stateis = "Billy's Head is IN"
        
    if mouth_open == 6:
        billy.mouth_open()
        stateis = "Billy's Mouth is OPEN"
    
    if mouth_close == 6:
        billy.mouth_close()
        stateis = "Billy's Mouth is CLOSED"

    if tail_out == 6:
        billy.tail_out()
        stateis = "Billy's Tail is OUT"
    
    if tail_in == 6:
        billy.tail_in()
        stateis = "Billy's Tail is IN"

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