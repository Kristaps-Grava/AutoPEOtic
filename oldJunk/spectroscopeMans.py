from machine import Pin
from machine import ADC
from time import sleep_us

VIDEO = 27
TRIGGER = 12
CLK = 11
START = 13
CHANNELS = 288

clk = Pin(CLK, Pin.OUT)
start = Pin(START, Pin.OUT)
video = ADC(VIDEO)

clk.value(1)
start.value(0)

def readSpectrometer():
    spectrum = []
    
    delay = 10

    clk.value(0)
    sleep_us(delay)
    clk.value(1)
    sleep_us(delay)
    clk.value(0)
    start.value(1)
    sleep_us(delay)
    start.value(1)

    for i in range(0, 14):
        clk.value(1)
        sleep_us(14)
        clk.value(0)
        sleep_us(delay)
    
    start.value(0)

    for i in range(0,86):
        clk.value(1)
        sleep_us(delay)
        clk.value(0)
        sleep_us(delay)
    
    for i in range(0, CHANNELS-1):
        spectrum.append(ADC.read_u16(video))

        clk.value(1)
        sleep_us(delay)
        spectrum.append(ADC.read_u16(video))
        clk.value(0)
        sleep_us(delay)

    for i in range(0,6):
        spectrum.append(ADC.read_u16(video))
        clk.value(1)
        sleep_us(delay)
        spectrum.append(ADC.read_u16(video))
        clk.value(0)
        sleep_us(delay)
    
    print(spectrum)

readSpectrometer()