from billy import Billy
from time import sleep

from machine import Pin

billy = Billy()
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