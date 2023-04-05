import RPi.GPIO as gpio
import sys
from time import sleep

gpio.setmode(gpio.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

gpio.setup(dac, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)

def convert(a):
    return [int(elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(256):
        dacc = convert(i)
        gpio.output(dac, dacc)
        sleep(0.005)
        if gpio.input(comp) == 0:
            k = i
            return k
        else:
            k = 0
    return k
try:
    while True:
        i = adc()
        if i != 0:
            print(i, '{:.2f}v'.format(3.3*i/256))

finally:
    gpio.output(dac, 0)
    gpio.cleanup()


