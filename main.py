#PURPOSE: to send each instruction from instructions.txt to the device that is responsible for executing it
#
#WORKFLOW EXAMPLE:  1) initiates all communication methods
#                   2) opens instructions.txt
#                   3) first istruction is 'G4'
#                   4) recognises that it is a G-code instruction; sends it to stepper arduino via serial
#                   5) waits until the instruction is executed
#                   6) next line is 'SERVO'
#                   7) recognises that this should be executed by main Arduino; sends it to main Arduino via serial
#                   8) and so on...
#

#TODO: test each communication method independently
#TODO: finish Arduino code for main Arduino and microPython code for Raspbery pico

from pymodbus.client import ModbusSerialClient
import configparser
import serial
import time

#creates and object from which settings can be accessed
config = configparser.ConfigParser()
config.read("settings.ini")

#opens instructions file
instructions = open(config['files']['instructions'], "r")

#defines a parrent class for general communication with devices
class communication:
    def __init__(self, name, port, baudrate):
        self.name = name
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(self.port, self.baudrate, timeout=1)

    def sendInstruction():
        raise NotImplementedError
    
    def receiveData():
        raise NotImplementedError

#TODO test progress: NOT PERFORMED
#defines a children class for communication with the main Arduino using serial
class mainCommunication(communication):
    def __init__(self, name, port, baudrate):
        super().__init__(name, port, baudrate)
        self.serial = serial.Serial(self.port, self.baudrate, timeout=1)

        def sendInstruction(self, instruction):
            self.serial.write((f'{instruction}\n').encode())
            time.sleep(10)

#TODO test progress: NOT PERFORMED
#defines a children class for communication with the stepper Arduino using serial
class stepperCommunication(communication):
    def __init__(self, name, port, baudrate):
        super().__init__(name, port, baudrate)
        self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
        
        __grblInit(self)

        def sendInstruction(self, instruction):
            self.serial.write((f'{instruction}\n').encode())
            time.sleep(10)

        def __grblInit(self):
	        #for debugging prints grbl settings
            self.serial.write(b'$$\n')
            time.sleep(1)
            response = self.serial.readline().decode().strip()
            print(f'Settings: {response}')
            
            #unlocks grbl
            self.serial.write(b'$X\n')
            time.sleep(1)
            response = self.serial.readline().decode().strip()
            print(f'Unlock response: {response}')

#TODO test progress: NOT PERFORMED
#defines a children class for communication with spectroscope's raspberry pico using UART
class spectromterCommunication(communication):
    def __init__(self, name, port, baudrate, pinRx, pinTx):
        super().__init__(name, port, baudrate)
        self.Rx = pinRx
        self.Tx = pinTx
        self.serial = serial.serial(self.port, self.baudrate)

        def getSpectrum(self):
            #PUROPOSE: to receive an array that contains spectrum data
            #WORKFLOW:  1) an activation command is sent to the pico
            #           2) the pico recieves the byte and executes readSpectrum() function
            #           3) in the meanwhile getSpectrum() function waits for response
            #           4) when finished measuring, pico sends spectrum data in the form of list
            #           5) getSpectrum() command receives answer

            self.serial.write(b'1')
            spectrum = self.serial.readline().decode().strip()  #in this response is spectrum list

            #TODO finish .getSpectrum function
            return spectrum

        def sendInstruction(self, instruction):
            self.serial.write((f'{instruction}\n').encode())
            time.sleep(10)

#TODO test progress: NOT PERFORMED
#defines a children class for communication with PEO using modbus
class peoCommunication(communication):
    def __init__(self, name, port, baudrate, parity, stopbits, bytesize, Upos, Ipos, Uneg, Ineg, Pulsepos, Pause1, Pulseneg, Pause2, Multiplier):
        super().__init__(self, name, port, baudrate)
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.Upos = Upos
        self.Ipos = Ipos
        self.Uneg = Uneg
        self.Ineg = Ineg
        self.Pulsepos = Pulsepos
        self.Pause1 = Pause1
        self.Pulseneg = Pulseneg
        self.Pause2 = Pause2
        self.Multiplier = Multiplier

        self.serial = ModbusSerialClient(self.port, self.baudrate, self.parity, self.stopbits, self.bytesize)
        self.serial.connect()

    def sendInstruction(self, instruction):
        #VARIABLES: what do they mean?
        #   Upos
        #   Ipos
        #   Uneg
        #   Ineg
        #   Pulsepos
        #   Pause1
        #   Pulseneg
        #   Pause2
        #   Multiplier
        #
        #COMMENT: for PEO datasheet go to peoDatasheet.txt; for original code go to peo.py
        
        #writing the values to the registers
        self.serial.write_register(address=0, value=self.Upos, slave=20)
        self.serial.write_register(address=1, value=self.Ipos, slave=20)
        self.serial.write_register(address=2, value=self.Uneg, slave=20)
        self.serial.write_register(address=3, value=self.Ineg, slave=20)
        self.serial.write_register(address=4, value=self.Pulsepos, slave=20)
        self.serial.write_register(address=5, value=self.Pause1, slave=20)
        self.serial.write_register(address=6, value=self.Pulseneg, slave=20)
        self.serial.write_register(address=7, value=self.Pause2, slave=20)
        self.serial.write_register(address=8, value=self.Multiplier, slave=20)
        
        #forcing coils to update the display
        serial.write_coil(2, True, slave=20)
        serial.write_coil(3, True, slave=20)

        time.sleep(1)


#initialises communication method with each device, at this point __init__() executes for each object
stepper = stepperCommunication('stepper', config['stepper arduino']['port'], config['stepper arduino']['baudrate'])
main = mainCommunication('main', config['main arduino']['port'], config['main arduino']['baudrate'])
PEO = peoCommunication('PEO',
                       config['PEO']['port'],
                       config['PEO']['baudrate'],
                       config['PEO']['parity'],
                       config['PEO']['stopbits'],
                       config['PEO']['bytesize'],
                       config['PEO']['Upos'],
                       config['PEO']['Ipos'],
                       config['PEO']['Uneg'],
                       config['PEO']['Ineg'],
                       config['PEO']['Pulsepos'],
                       config['PEO']['Pause1'],
                       config['PEO']['Pulseneg'],
                       config['PEO']['Pause2'],
                       config['PEO']['Multiplier'])
                        #TODO: place all PEO settings into a list
                        #TODO: update instructions.ini to include new variables

#goes through all of the instructions
line = 1
for instruction in instructions:
    print(f'Sending: {instruction}')
    
    #a check to see for which device the instruction is written; then the instruction is sent
    if instruction.startswith('WIRE' or 'SOLENOID'):
        #main.sendInstruction(instruction)
        pass

    elif instruction.startswith('G1' or 'G4' or 'M30' or 'F'):
        stepper.sendInstruction(instruction)

    elif instruction.startswith('PEO'):
        #PEO.sendInstruction(instruction)
        pass
    elif instruction.startswith('#'):
        pass

    else:
        print(f'{instruction} not recognised at line:{line}')

    line += 1