# this code will be running on raspberry pi and will control 2 Arduinos

# from the instructions.txt, gcode instructions will be sent to stepper Arduino;
# servo and solenoid instructions will be sent to main Arduino

# IMPORTANT: stepper port needs to be connected before the main port!

import serial
import time

def send_instructions(main_port, main_baud_rate, stepper_port, stepper_baud_rate, instructions_file):
    # Open serial port with timeout
    main_serial = serial.Serial(main_port, main_baud_rate, timeout=1)
    stepper_serial = serial.Serial(stepper_port, stepper_baud_rate, timeout=1)

    time.sleep(2)  # Wait for connection to establish

    stepper_serial.write(b'$$\n')
    time.sleep(1)
    response = stepper_serial.readline().decode().strip()
    print('settings: {response}')

    # Unlock GRBL (clear any alarms)
    stepper_serial.write(b'$X\n')
    time.sleep(1)
    response = stepper_serial.readline().decode().strip()
    print(f'Unlock Response: {response}')

    # Open instruction file
    with open(instructions_file, 'r') as file:
        lines = file.readlines()

    print(lines) # debugging to check how the code sees instructions

    # Send instruction lines
    for line in lines:
        line = line.strip()  # Remove any whitespace
        
        if line.startswith("WIRE") or line.startswith("SOLENOID"):
            main_serial.write((line + '\n').encode()) # Send instructions to Main Arduino

        elif line.startswith("#"):
            pass

        elif line:
            stepper_serial.write((line + '\n').encode())  # Send G-code line
            print(f'Sent: {line}')
            
            if line.startswith('G4'): # Handle dwell (G4) command explicitly
                # Extract the dwell time in milliseconds
                try:
                    duration = int(line.split('P')[1]) / 1000.0
                    print(f'Dwelling for {duration} seconds')
                    time.sleep(duration)  # Perform the dwell

                except (IndexError, ValueError):
                    print("Error parsing G4 command. Skipping dwell.")
                    continue

            while True: # print the response from GRBL
                response = stepper_serial.readline().decode().strip()
                
                if response:
                    print(f'Response: {response}')
                if response == 'ok' or 'error' in response:
                    break

            time.sleep(10)  # Delay to allow GRBL to process

    # Close serial port
    stepper_serial.close()
    main_serial.close()

if __name__ == "__main__":
    main_port = '/dev/ttyUSB1' # for linux "/dev/ttyUSB1"
    main_baud_rate = 115200
    stepper_port = '/dev/ttyUSB0' # for linux "/dev/ttyUSB0"
    stepper_baud_rate = 115200  # 115200 is default for GRBL
    instructions_file = 'instructions.txt'

    send_instructions(main_port, main_baud_rate, stepper_port, stepper_baud_rate, instructions_file)
