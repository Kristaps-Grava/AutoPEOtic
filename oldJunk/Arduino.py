# this code will be running on raspberry pi and will control 2 Arduinos

# from the instructions.txt, gcode instructions will be sent to stepper Arduino;
# servo and solenoid instructions will be sent to main Arduino

# IMPORTANT: stepper port needs to be connected before the main port!

import serial
import time

def executeInstructions(main_port, stepper_port, main_baud_rate, stepper_baud_rate, instructions_file):

    main_serial = serial.Serial(main_port, main_baud_rate, timeout=1)
    stepper_serial = serial.Serial(stepper_port, stepper_baud_rate, timeout=1)
    time.sleep(2)

    # print grbl settings and & unlock grbl
    grbl_init(stepper_serial)

    # Open instruction file
    with open(instructions_file, 'r') as file:
        lines = file.readlines()
    n = 0
    

    print(f"Sent: {lines[n]}")
    for line in lines:
        line = line.strip() # Remove any whitespace

        if line.startswith("WIRE") or line.startswith("SOLENOID"):
            main_serial.write((f'{line}\n').encode()) # Send instructions to Main Arduino

        elif line:
            stepper_serial.write((line + '\n').encode())  # Send G-code line

            # Handle dwell (G4) command explicitly
            if line.startswith('G4'):
                duration = int(line.split('P')[1]) / 1000.0
                print(f'Dwelling for {duration} seconds')
                time.sleep(duration)  # Perform the dwell

        elif line.startswith("#"):
            pass

        while True: # print the response from GRBL
            response = stepper_serial.readline().decode().strip()

            if response:
                print(f'Response: {response}')
            if response == 'ok' or 'error' in response:
                break

            time.sleep(10) # Delay to allow GRBL to process

    # Close serial port
    stepper_serial.close()
    main_serial.close()

def grbl_init(stepper_serial):
    stepper_serial.write(b'$$\n')
    time.sleep(1)
    response = stepper_serial.readline().decode().strip()
    print('settings: {response}')

    # Unlock GRBL (clear any alarms)
    stepper_serial.write(b'$X\n')
    time.sleep(1)
    response = stepper_serial.readline().decode().strip()
    print(f'Unlock Response: {response}')

if __name__ == "__main__":
    main_port = '/dev/ttyUSB1' # for linux "/dev/ttyUSB1"
    stepper_port = '/dev/ttyUSB0' # for linux "/dev/ttyUSB0"
    main_baud_rate= 115200
    stepper_baud_rate= 115200
    instructions_file = "instructions.txt"

    configparser = 

    executeInstructions(main_port, stepper_port, main_baud_rate, stepper_baud_rate, instructions_file)
