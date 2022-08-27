from billy import Billy
from time import sleep
import network
from secret import ssid, password
from machine import Pin, WDT, reset
import uasyncio as asyncio
import socket
from time import gmtime
from phew import server, connect_to_wifi

connect_to_wifi(ssid, password)

f = open("index.html","r")
html = f.read()
f.close()

onboard = Pin("LED", Pin.OUT, value=0)

billy = Billy()
stateis = ""
page_views = 0


def what_time_is_it_mr_wolf()->list:
    time_list = gmtime()
    current_time = {'year': str(time_list[0]),
                    'month': str(time_list[1]),
                    'day': str(time_list[2]),
                    'hour': str(time_list[3]),
                    'minute': str(time_list[4]),
                    'second': str(time_list[5])}
    return str(current_time['hour'] + ":" + current_time['minute'] + ":" +  current_time['second'] + " " + current_time['day'] + "/" + current_time['month'] + "/" + current_time['year'] )

async def serve_client(reader, writer):
    global billy, stateis, page_views, boot_time

    page_views += 1
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
    
   
    if head_out == 6: billy.head_out()
    if head_in == 6: billy.head_in()
    if mouth_open == 6: billy.mouth_open()
    if mouth_close == 6: billy.mouth_close()
    if tail_out == 6: billy.tail_out()
    if tail_in == 6: billy.tail_in()
        
    print(f'billy: "{billy}"')
    response = html % (billy, billy.status, str(page_views), boot_time)
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')

async def main():
    print ("setting up webserver")
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    wdt = WDT(timeout=8000)
    while True:
        # check wifi is connected:
        if wlan.isconnected() == False:
            print("wifi disconnected")
            reset()
        onboard.on()
        print("heartbeat")
        wdt.feed()
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)
          
boot_time = what_time_is_it_mr_wolf()
billy.reset()
sleep(0.1)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()