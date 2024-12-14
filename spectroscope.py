from machine import Pin
from machine import ADC
from time import sleep_us

VIDEO = 26
TRIGGER = 16
CLK = 15
START = 14
CHANNELS = 288

clk = Pin(CLK, Pin.OUT)
start = Pin(START, Pin.OUT)
video = ADC(VIDEO)

clk.value(1)
start.value(0)

#TODO: read spectrum 10 times and take output the average of all measurements

def readSpectrometer():
    
    spectrum = []
    
    delay = 1

    clk.value(0)
    sleep_us(delay)
    clk.value(1)
    sleep_us(delay)
    clk.value(0)
    start.value(1)
    sleep_us(delay)
    start.value(1)

    for i in range(0, 6):
        clk.value(1)
        sleep_us(delay)
        clk.value(0)
        sleep_us(delay)
    
    start.value(0)

    for i in range(0,87):
        clk.value(1)
        sleep_us(delay)
        clk.value(0)
        sleep_us(delay)
    
    for i in range(0, CHANNELS):
        spectrum.append(ADC.read_u16())

        clk.value(1)
        sleep_us(delay)
        clk.value(0)
        sleep_us(delay)

    for i in range(0,6):
        clk.value(1)
        sleep_us(delay)
        clk.value(0)
        sleep_us(delay)
    
    print(spectrum)

readSpectrometer()