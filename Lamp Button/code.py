import time
import board
import neopixel
import touchio
import supervisor
import math 

from adafruit_debouncer import Debouncer

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

touch_pad = board.A0

touch = touchio.TouchIn(touch_pad)
touch_debounced = Debouncer(touch, interval=0.05)

pixel_pin = board.D10
num_pixels = 16
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

val = 0
direction = 1

while True:
    ble.start_advertising(advertisement)
    pixels.fill(RED) 
    pixels.show()
    
    while not ble.connected:
        pass
    while ble.connected:
        touch_debounced.update()
        
        if not touch_debounced.value:
            val = (math.exp(math.sin(supervisor.ticks_ms() / 2000.0 * math.pi)) - 0.36787944) * 108.0;
            pixels.fill((val, val, val))
            pixels.show()    

        
        if touch_debounced.rose:
            pixels.fill(YELLOW) 
            pixels.show()
            uart.write(b"2")


