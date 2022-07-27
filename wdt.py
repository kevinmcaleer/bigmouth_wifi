# Watch Dog Timer

from machine import WDT

wdt = WDT(timeout=8000)

while True:
    sleep(1)
    wdt.feed()