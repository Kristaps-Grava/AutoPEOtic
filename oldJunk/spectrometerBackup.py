from time import sleep_us, ticks_us, ticks_ms
import machine
from machine import Pin, I2C, PWM

class HAMA:
    def __init__(self):
        
        self.picoADC = machine.ADC(27)
        self.CLK = 11
        self.ST = 10

        self.pinST = Pin(self.ST, Pin.OUT, Pin.PULL_DOWN)
        
        sleep_us(10)
        
        self.spectra = list()
        self.delay = 1
        self.accum = 1
        self.exposure = 0.001
    
    def repeater(self, times, f, *args): 
        for i in range(times): f(*args)

    def sample_spec(self):
        starting_time = ticks_us()
        to_reach_exposure = starting_time + self.exposure*1e+6 #ja expo ir sekundēs
        while to_reach_exposure > ticks_us():
            continue
        
        self.PWMCLK.duty_u16(0)
        self.PWMCLK.deinit()
        
    def read_spec(self):
        self.pinCLK.high()
        sleep_us(self.delay)
        self.spectra.append(self.picoADC.read_u16())
        self.pinCLK.low()
        sleep_us(self.delay)
    
    def cycle_spec(self):
        self.pinCLK.high()
        self.pinCLK.low()
    
    def start(self):
        self.PWMCLK = PWM(Pin(self.CLK))
        self.PWMCLK.freq(125000000//2)
        self.PWMCLK.duty_u16(32768)
        sleep_us(self.delay)
        self.pinST.high()
        
        self.sample_spec()
        self.pinST.low()
        self.pinCLK = Pin(self.CLK, Pin.OUT, Pin.PULL_DOWN)
        self.repeater(48, self.cycle_spec)
        self.repeater(39, self.cycle_spec)
        self.repeater(288, self.read_spec)
        self.repeater(2, self.cycle_spec)
        sleep_us(self.delay)
        return self.spectra

    def addCount(self):
        self.counts += 1
        
    def acquisition(self):
        self.spectra = list()
        self.spectra.clear()
        self.spectra = self.start()
        return self.spectra

    def main(self, exposure, accum):
        self.accum = accum
        self.exposure = exposure
        if type(self.accum) == float:
            self.accum = round(self.accum)
        
        self.spectra = self.acquisition()
        
        if (self.accum > 1):
            self.accum_spectra = list()
            self.accum_spectra = self.spectra
            self.temp_spectra = list()
            for i in range(self.accum-1):
                self.temp_spectra.clear()
                self.temp_spectra = self.acquisition()
                self.accum_spectra = [sum(value) for value in zip(self.temp_spectra,self.accum_spectra)]
            return self.accum_spectra
        else:
            return self.spectra
    
    def autoexposure(self, exposure):
        self.exposure = exposure
        self.spectra = self.acquisition()
        thisisgood = False
        anditsalsobad = False
        while not thisisgood:
            if max(self.spectra) in range(40000,65530):
                thisisgood = True
            elif max(self.spectra) > 65530 and self.exposure<1:
                if self.exposure>1e-9:
                    self.exposure = self.exposure/2
                    self.spectra = self.acquisition()
                else:
                    thisisgood = True
                    anditsalsobad = True
            elif max(self.spectra) < 14000 and self.exposure<0.1:
                if self.exposure<0.01:
                    self.exposure = self.exposure*10
                else:
                    self.exposure = self.exposure*2
                self.spectra = self.acquisition()
            elif max(self.spectra) in range(14000,40000) and self.exposure<0.1:
                self.exposure = self.exposure*50000/max(self.spectra)
                self.spectra = self.acquisition()
            else:
                thisisgood = True
        return anditsalsobad, self.exposure, self.spectra
        
    
if __name__ == '__main__':
    overexposed = False
    defexposure = 0.01
    try:
        #import LED
        #led = LED.LED_control()
        #led.LEDstate(*[0.2,0,0,0,0,0,0,0,0,0])
        #led.cleanup()
        while 1:
            import sys
            spectra = list()
            hama = HAMA()
            xtime = ticks_ms()
            #spectra = hama.main(exposure=0.001, accum=1) #exp in seconds
            overexposed, defexposure, spectra = hama.autoexposure(defexposure)
            y = ticks_ms() - xtime
            print('Time:%.0fms'%(y),'wl@I_max:%.1f'%max(spectra))
            print(defexposure)
            print(spectra)
            if overexposed:
                print("Probably overexposed!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            sleep_us(1000000)
    except KeyboardInterrupt:
        hama.pinST.low()
        sys.exit(0)
        


          
