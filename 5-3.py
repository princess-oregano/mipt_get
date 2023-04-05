import RPi.GPIO as gpio
from time import sleep
gpio.setmode(gpio.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

gpio.setup(dac, gpio.OUT)
gpio.setup(leds, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)

def convert(a):
    return [int(elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k+=2**i
        gpio.output(dac, convert(k))
        sleep(0.005)
        if gpio.input(comp) == 0:
            k-=2**i
    return k

def volume(n):
    n = int(n/256*10*4)
    arr = [0] * 8
    for i in range(0, n-1):
        arr[i] = 1
    return arr

try:
    while True:
        k = adc()
        if k != 0:
            print(int(k/256*10*4))
            gpio.output(leds, volume(k))
            

finally:
    gpio.output(dac, 0)
    gpio.cleanup()
