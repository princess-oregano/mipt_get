import RPi.GPIO as gpio
import sys
from time import sleep
dac=[26, 19, 13, 6, 5, 11, 9, 10]
gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)
def perev(a, n):
    return [int (elem) for elem in bin(a)[2:].zfill(n)]

try:
    while (True):
        print('Input number:\n')
        T=input()
        if T=='q':
            sys.exit() 
        t=int(T)/195/2
        for i in range(195):
            gpio.output(dac, perev(i, 8))
            sleep(t)
        for i in range(194, -1, -1):
            gpio.output(dac, perev(i, 8))
            sleep(t)
finally:
    gpio.output(dac, 1)
    gpio.cleanup()
  
