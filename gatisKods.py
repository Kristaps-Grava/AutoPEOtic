from time import sleep, time #time related functions
import RPi.GPIO as GPIO #Raspberry Pi GPIO interfacing library

#ADS1115 control library
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

class pi4_hama:
    #Initialize parameters
    def __init__(self):
        GPIO.setwarnings(False)			#Removes some clutter from shell
        GPIO.setmode(GPIO.BCM)			#GPIO numbering mode
        self.CLK = 18					#C12880MA CLK pin GPIO nr
        self.ST = 17					#C12880MA ST pin GPIO nr
        GPIO.setup(self.CLK, GPIO.OUT)	#Set CLK pin as output
        GPIO.setup(self.ST, GPIO.OUT)	#Set ST pin as output
        GPIO.output(self.CLK, 1)		#init CLK HIGH
        GPIO.output(self.ST, 0)			#init ST LOW
        
        self.ADC_CHAN = 0		#Corresponding ADS1115 channel
        self.spectra = list()
        self.adc_delay = 2e-3	#Delay between ADC reads, ADS1115 max SPS is 860, so a rounded up 2ms delay is used
        self.exposition = 1e-4	#init exposition time
        self.delay = 1e-6		#delay between CLK pulse shifts
        self.accum = 1			#init number of spectra accumulations
        
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.mode = Mode.SINGLE
        self.ads.data_rate = 860
        self.chan = AnalogIn(self.ads, ADS.P0)

    #C12880MA wavelength calibration (device specific, each device gets shipped with this information)
    def wavelength(self):
        self.nm = list()
        for i in range (0, 288):
            self.nm.append(i)
            koef = (3.11487118*1e2+2.704770136*i-1.198161774*1e-3*i**2-\
                7.333264294*1e-6*i**3+8.195191046*1e-9*i**4+6.104509768*1e-12*i**5)
            self.nm[i]=koef
            
        return self.nm

    #Repeat function *f* certain amount of *times*
    def repeater(self, times, f, *args):
        for _ in range(times):
            f(*args)
    
    #Exposition
    def exposition_control(self):
        starting_time = time()
        to_reach_exposition = starting_time + self.exposition
        while to_reach_exposition > time():
            GPIO.output(self.CLK, 1)
            sleep(self.delay)
            GPIO.output(self.CLK, 0)
            sleep(self.delay)
    #One CLK cycle
    def cycle_spectrometer(self):
        GPIO.output(self.CLK, 1)
        sleep(self.delay)
        GPIO.output(self.CLK, 0)
        sleep(self.delay)
        
    #One read cycle
    def read_spectrometer(self):
        GPIO.output(self.CLK, 1)
        #read value from ADS1115 and append to list. Read Adafruit_Python_ADS1x15 source for more information
        #self.spectra.append(Adafruit_ADS1x15.ADS1115().read_adc(self.ADC_CHAN, gain=1, data_rate=860))
        self.spectra.append(self.chan.value)
        GPIO.output(self.CLK, 0)
        return self.spectra
    
    #Spectrometer control
    def start(self):
        #initialization
        GPIO.output(self.CLK, 0)
        self.cycle_spectrometer()
        GPIO.output(self.ST, 1) 
        sleep(self.delay)
        self.repeater(3, self.cycle_spectrometer)
        
        #---Integration time start
        self.exposition_control()
        GPIO.output(self.ST, 0)
        self.repeater(48, self.cycle_spectrometer)
        #---Integration time end
        
        #Cycle 48 times before reading resulting spectra
        self.repeater(39, self.cycle_spectrometer)
        
        #Read spectrometer
        self.repeater(288, self.read_spectrometer)
        
        #Finishing pulses
        self.repeater(8, self.cycle_spectrometer)
        GPIO.output(self.CLK, 1)
        sleep(self.delay)
        
        return self.spectra
    
    #If no accumulation is used
    def acquisition(self):
        self.spectra = list()
        self.spectra.clear()
        self.spectra = self.start()
        
        return self.spectra
    
    def cleanup(self):
        GPIO.cleanup()
    
    #Main
    def measure(self, exposition, accum):
        self.exposition = exposition
        self.accum = accum
        if type(accum) == float:
            self.accum = round(self.accum)
        
        self.spectra = self.acquisition()
        if (self.accum > 1):
            self.accum_spectra = list()
            self.accum_spectra = self.spectra
            self.temp_spectra = list()
            for _ in range(self.accum-1):
                self.temp_spectra.clear()
                self.temp_spectra = self.acquisition()
                self.accum_spectra = [sum(value) for value in zip(self.temp_spectra,self.accum_spectra)]
            return self.accum_spectra
        else:
            return self.spectra


print(pi4_hama.measure(1,1))