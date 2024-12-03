import time
import board
import neopixel
import touchio
import time
import supervisor
import math 
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
pixel_pin = board.D10
num_pixels = 16

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)

RED = (255, 0, 0)
GREEN = (0, 255, 0)

secret_code = "222222222"
reset_code = "11111"

secret_code_buffer = ""
reset_code_buffer = ""
won = False

while True:
    try:
        for count, connection in enumerate(ble.connections):  
                if UARTService not in connection:
                    continue
                uart = connection[UARTService]
                while uart.in_waiting > 0 and count == 0: #this is needed due to circuitpython's poor handling multiple UART connections 
                    one_byte = uart.read(1) 
                    if one_byte:
                        print(one_byte)
                        #add new characters
                        secret_code_buffer += one_byte.decode()
                        reset_code_buffer += one_byte.decode()
                        print(secret_code_buffer) 
                        print(reset_code_buffer)
                        #slice off old characters
                        secret_code_buffer =  secret_code_buffer[-len(secret_code):]
                        reset_code_buffer =  reset_code_buffer[-len(reset_code):] 
                        print(secret_code_buffer)
                        print(reset_code_buffer)
                        #check for a win or reset condition
                        if secret_code == secret_code_buffer:
                            print("secret code match")
                            won = True
                        if reset_code == reset_code_buffer:
                            print("reset code match")  
                            won = False 
    except:
        print("Exception") 
                
                    
    if (len(ble.connections) < 4): 
        print("scanning")
        pixels.fill(RED)  #this warns that there is a problem
        pixels.show()
        for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=1):
            if UARTService not in advertisement.services:
                continue
            ble.connect(advertisement)
            print("connected")
            break
        ble.stop_scan()
    else:
        if (won == True):
            pixels.fill(GREEN)
        else:
            val = (math.exp(math.sin(supervisor.ticks_ms() / 2000.0 * math.pi)) - 0.36787944) * 108.0;
            pixels.fill((val, val, val))
        pixels.show()    

    
