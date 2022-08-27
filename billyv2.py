import network
import upip
from secret import ssid, password
from billy import Billy
import uos
from time import sleep, gmtime
from machine import RTC, reset

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    print(".",end="")
    sleep(0.5)
    
print(f"connected with ip {wlan.config}")

# check if phew installed
installed_libs = uos.listdir('lib')
if "phew" not in installed_libs:
    print("Phew not installed, installing now")
    upip.install("micropython-phew")
else:
    print("phew already installed")
from phew import logging, server, template

logging.info("Starting up Billy")
billy = Billy()

page_views = 1
status = ""

from phew import server, connect_to_wifi

connect_to_wifi(ssid, password)

# if the clock isn't set then we need to fetch the time from an NTP
# server. this requires connecting to WiFi

# set clock
billy.update_rtc_from_ntp()

if not billy.clock_set():
  logging.info("> clock not set, synchronise from ntp server")
  if not billy.sync_clock_from_ntp():    
    # if we failed to synchronise the clock then turn on the warning
    # led and go back to sleep for another cycle
    logging.error("! failed to synchronise clock")

uptime = billy.what_time_is_it_mr_wolf()

if billy.low_disk_space():
  # there is less than 10% of the filesystem available, time to truncate the log file
  logging.error("! low disk space")
  logging.truncate(8192)

@server.route("/", methods=["GET"])
def index(request):
    global page_views
    response = (template.render_template('index.html',page_views=page_views, uptime=uptime, status=status, fish_image=billy))
    page_views += 1
    return response

@server.route("/about", methods=["GET"])
def about(request):
    global page_views
    response = (template.render_template('about.html',page_views=page_views, uptime=uptime, status=status, fish_image=billy))
    page_views += 1
    return response

def redirect_and_respond(request):
    global page_views
    response = (template.render_template('index.html',page_views=page_views, uptime=uptime, status=billy.status, fish_image=billy))
    page_views += 1
    logging.info("redirecting")
    return response

@server.route("/head/out", methods=["GET"])
def head_out(request):
    billy.head_out()
    return redirect_and_respond(request)

@server.route("/head/in", methods=["GET"])
def head_in(request):
    billy.head_in()
    return redirect_and_respond(request)

@server.route("/tail/out", methods=["GET"])
def tail_out(request):
    billy.tail_out()
    return redirect_and_respond(request)

@server.route("/tail/in", methods=["GET"])
def tail_in(request):
    billy.tail_in()
    return redirect_and_respond(request)

@server.route("/mouth/open", methods=["GET"])
def mouth_open(request):
    billy.mouth_open()
    return redirect_and_respond(request)

@server.route("/mouth/close", methods=["GET"])
def mouth_close(request):
    billy.mouth_close()
    return redirect_and_respond(request)

@server.catchall()
def catchall(request):
  return "Not found", 404

server.run(host="0.0.0.0", port=80)
wdt = WDT(timeout=8000)
while True:
    # check wifi is connected:
    if wlan.isconnected() == False:
        print("wifi disconnected")
        log.error("wifi disconnected")
        log.info("Resetting device")
        reset()
    onboard.on()
    wdt.feed()
    sleep(0.25)
    onboard.off()
    sleep(5)
