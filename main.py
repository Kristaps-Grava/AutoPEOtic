import PEO
import serial
from pymodbus.client import ModbusSerialClient
import configparser
import time

config = configparser.ConfigParser()
config.read("settings.ini")

instructions = open('instructions.txt', "r")


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

class mainCommunication(communication):
    def __init__(self, name, port, baudrate):
        super().__init__(name, port, baudrate)
        self.serial = serial.Serial(self.port, self.baudrate, timeout=1)

        def sendInstruction(self, instruction):
            self.serial.write((f'{instruction}\n').encode())
            time.sleep(10)

class stepperCommunication(communication):
    def __init__(self, name, port, baudrate):
        super().__init__(name, port, baudrate)
        self.serial = serial.Serial(self.port, self.baudrate, timeout=1)

        #TODO: implement startup sequence for grbl, including, unlocking and prinitng settings

        def sendInstruction(self, instruction):
            self.serial.write((f'{instruction}\n').encode())
            time.sleep(10)

class uartCommunication(communication):
    def __init__(self, name, pinRx, pinTx):
        super().__init__(name)
        self.Rx = pinRx
        self.Tx = pinTx

        def spectrum(self):
            
            return spectrum

        def sendInstruction(self, instruction):
            self.serial.write((f'{instruction}\n').encode())
            time.sleep(10)


class peoCommunication(communication):
    def __init__(self, name, port, baudrate, parity, stopbits, bytesize):
        super().__init__(self, name, port, baudrate)
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.serial = ModbusSerialClient(self.port, self.baudrate, self.parity, self.stopbits, self.bytesize)

    def sendInstruction(self, instruction):
        raise NotImplementedError


stepper = stepperCommunication('stepper', config['SETTINGS']['stepperPort'], config['SETTINGS']['stepperBaudrate'])
main = mainCommunication('main', config['SETTINGS']['mainPort'], config['SETTINGS']['mainBaudrate'])
PEO = peoCommunication('PEO', config['SETTINGS']['peoPort'], config['SETTINGS']['peoBaudrate'])



for instruction in instructions:
    print(f'Sending: {instruction}')
    
    if instruction.startswith('WIRE' or 'SOLENOID'):
        main.sendInstruction(instruction)

    elif instruction.startswith('G1' or 'G4' or 'M30' or 'F'):
        stepper.sendInstruction(instruction)

    elif instruction.startswith('#'):
        pass

    else:
        print(f'{instruction} instruction not found')