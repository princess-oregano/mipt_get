import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# Setting up GPIO
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
# 

def dec2bin(value):
    return [int(bit) for bit in bin(int(value))[2:].zfill(8)]

def bin2dec(list):
    weight = 128
    val = 0
    for i in range(0, 8):
        val += weight * list[i]
        weight /= 2
    
    return val

def adc_sar():
    step    = 2**7
    voltage = step
    while step:
        GPIO.output(dac, dec2bin(voltage))
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            voltage -= step 
        
        step   >>= 1
        voltage += step

    return voltage


try:
    data = []
    start_time = time.time()
    GPIO.output(troyka, 1)
    
    volt = 0
    while(volt <= 255 * 0.6):
        volt = adc_sar()
        data.append(volt * 3.3 / 256)
        print("Voltage: {:.2f} V".format(volt * 3.3 / 256))
        GPIO.output(leds, dec2bin(volt))
    
    charge_time = time.time() - start_time
    
    GPIO.output(troyka, 0)

    volt = 255
    while(volt >= 255 * 0.05):
        volt = adc_sar()
        data.append(volt * 3.3 / 256)
        print("Voltage: {:.2f} V".format(volt * 3.3 / 256))
        GPIO.output(leds, dec2bin(volt))
    
    finish_time = time.time() - start_time
        
finally:
    print("Finishing")
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()


plt.plot(data)
plt.show()

data_str = [str(item) for item in data]

with open("7-1_data.txt", "w") as outfile:
    outfile.write("\n".join(data_str))

with open("7-1_settings.txt", "w") as outfile:
    outfile.write("{:.3f}\n".format(charge_time))
    outfile.write("{:.3f}\n".format(finish_time))
    outfile.write("{} \n{:.5f}\n".format(finish_time / len(data), 3.3 / 256))