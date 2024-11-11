# the g-code instructions from "gcode.txt" are sent to Arduino that has GRBL uploaded

# X axis represents left-right movement
# Y axis represents up-down movement
# Z axis represents extrusion of wire

import serial
import time

def send_gcode(port, baud_rate, gcode_file):
    # Open serial port with timeout
    ser = serial.Serial(port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for connection to establish


    ser.write(b'$$\n')
    time.sleep(1)
    response = ser.readline().decode().strip()
    print('settings: {response}')

    # Unlock GRBL (clear any alarms)
    ser.write(b'$X\n')
    time.sleep(1)
    response = ser.readline().decode().strip()
    print(f'Unlock Response: {response}')

    # Open G-code file
    with open(gcode_file, 'r') as file:
        lines = file.readlines()

    # Send G-code lines
    for line in lines:
        line = line.strip()  # Remove any whitespace
        if line:
            ser.write((line + '\n').encode())  # Send G-code line
            print(f'Sent: {line}')
            
            # Handle dwell (G4) command explicitly
            if line.startswith('G4'):
                # Extract the dwell time in milliseconds
                try:
                    duration = int(line.split('P')[1]) / 1000.0  # Convert milliseconds to seconds
                    print(f'Dwelling for {duration} seconds')
                    time.sleep(duration)  # Perform the dwell
                except (IndexError, ValueError):
                    print("Error parsing G4 command. Skipping dwell.")
                    continue

            # Read the response from GRBL
            while True:
                response = ser.readline().decode().strip()
                if response:
                    print(f'Response: {response}')
                if response == 'ok' or 'error' in response:
                    break

            time.sleep(0.1)  # Delay to allow GRBL to process

    # Close serial port
    ser.close()

if __name__ == "__main__":
    port = 'COM5'  # Windows example: 'COM3', Linux example: '/dev/ttyUSB0'
    baud_rate = 115200  # Default baud rate for GRBL
    gcode_file = 'gcode.txt'  # Path to your G-code file

    send_gcode(port, baud_rate, gcode_file)
