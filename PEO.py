# For modbus register addresses and settings see PEO.txt documentation

from pymodbus.client import ModbusSerialClient
from time import sleep

serial = ModbusSerialClient(port='COM10', baudrate=19200, parity='E', stopbits=1, bytesize=8)
serial.connect()

# Values for the next experiment. In comments you see the allowed range.
Upos = 300 # 30-700 V
Ipos = 100 # 100-500 A
Uneg = 10 # 10-300 V
Ineg = 100 # 100-500 A
Pulsepos = 100 # 0-9999
Pause1 = 100 # 2-9999
Pulseneg = 100 # 0-9999
Pause2 = 100 # 2-9999
Multiplier = 3 # 3-6 (n*10-3 - n*10-6)

# Printing values from the previous experiment
v=[]
print("VALUES FROM THE PREVIOUS EXPERIMENT")
for register in range(0,9):
    v.append(str(serial.read_holding_registers(address=register, count=1, slave=20).registers[0]))
print(f"U+ {v[0]}V\nI+ {v[1]}\nU- {v[2]}\nI- {v[3]}\nPulse+ {v[4]}\nPause1 {v[5]}\nPulse- {v[6]}\nPause2 {v[7]}\nMultiplier {v[8]}\n")

# Writing new values to registers
print(serial.write_register(address=0, value=Upos, slave=20))
print(serial.write_register(address=1, value=Ipos, slave=20))
print(serial.write_register(address=2, value=Uneg, slave=20))
print(serial.write_register(address=3, value=Ineg, slave=20))
print(serial.write_register(address=4, value=Pulsepos, slave=20))
print(serial.write_register(address=5, value=Pause1, slave=20))
print(serial.write_register(address=6, value=Pulseneg, slave=20))
print(serial.write_register(address=7, value=Pause2, slave=20))
print(serial.write_register(address=8, value=Multiplier, slave=20))

# Forcing coils to update the display
serial.write_coil(2,True,slave=20) # coil command, turning on coil, slave address
serial.write_coil(3,True,slave=20) # coil command, turning on coil, slave address

sleep(1)

# Printing new values from modbus registers
v=[]
print("NEW VALUES FROM MODBUS REGISTERS")
for register in range(0,9):
    v.append(str(serial.read_holding_registers(address=register, count=1, slave=20).registers[0]))
print(f"\nU+ {v[0]}\nI+ {v[1]}\nU- {v[2]}\nI- {v[3]}\nPulse+ {v[4]}\nPause1 {v[5]}\nPulse- {v[6]}\nPause2 {v[7]}\nMultiplier {v[8]}\n")


'''
print(serial.read_holding_registers(address=0, count=1, slave=20).registers[0])
print(serial.write_register(address=0, value=700, slave=20))

serial.write_coil(2,True,slave=20) # coil command, turning on coil, slave address
serial.write_coil(3,True,slave=20) # coil command, turning on coil, slave address
print(serial.read_holding_registers(address=15, count=1, slave=20).registers[0])



# Values for the next experiment. In comments you see the allowed range.
Upos = 30 # 30-700 V
Ipos = 100 # 100-500 A
Uneg = 10 # 10-300 V
Ineg = 100 # 100-500 A
Pulsepos = 100 # 0-9999
Pause1 = 100 # 2-9999
Pulseneg = 100 # 0-9999
Pause2 = 100 # 2-9999
Multiplier = 6e-3 # 3-6 (n*10-3 - n*10-6)

# Printing values from the previous experiment
a,b,c,d,e,f,g,h,i = serial.read_holding_registers(24, 32)
print("VALUES FROM THE PREVIOUS EXPERIMENT")
print(f"U+ {a}\nI+ {b}\nU- {c}\nI- {d}\nPulse+ {e}\nPause1 {f}\nPulse- {g}\nPause2 {h}\nMultiplier {i}\n")

# Writing new experiment values
serial.write_register(24, Upos)
serial.write_register(25, Ipos)
serial.write_register(26, Uneg)
serial.write_register(27, Ineg)
serial.write_register(28, Pulsepos)
serial.write_register(29, Pause1)
serial.write_register(30, Pulseneg)
serial.write_register(31, Pause2)
serial.write_register(32, Multiplier)

# Printing new values from modbus registers
a,b,c,d,e,f,g,h,i = serial.read_holding_registers(24, 32)
print("VALUES FOR THE CURRENT EXPERIMENT")
print(f"U+ {a}\nI+ {b}\nU- {c}\nI- {d}\nPulse+ {e}\nPause1 {f}\nPulse- {g}\nPause2 {h}\nMultiplier {i}\n")

sleep(2000)

# Printing measured values every second
while True:
    a,b,c,d,e,f = serial.read_holding_registers(9, 14)
    print("MEASURED VALUES")
    print(f"U+ {a}\nI+ {b}\nU- {c}\nI- {d}\nUin+ {e}\nUin- {f}\n")
    sleep(1000)
'''