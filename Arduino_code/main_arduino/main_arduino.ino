#include <Servo.h>

Servo servo;

String latestInstruction = ""; // A string to hold incoming data
bool stringComplete = false;   // Whether the string is complete

int solenoid_pin = 8;
int servo_pwm_pin = 9;

int servo_state = 0;    // servo state is represented by its angle
int solenoid_state = 0; // solenoid state is represented by 0 or 1. SOLENOID OUT = 0; SOLENOID IN = 1

void setup()
{
    Serial.begin(9600);
    pinMode(solenoid_pin, OUTPUT)
        pinMode(servo_pwm_pin, OUTPUT)

            servo.attach(servo_pwm_pin);
}

void loop()
{
    // Check if the string is complete
    if (stringComplete)
    {
        Serial.println(latestInstruction) // Print the received string for debugging

            if latestInstruction.startswith("SERVO");
        {
            instruction_array = splitString(latestInstruction, " ")
                servo_state = instruction_array[1]

                              myservo.write(servo_state)
        }
        if latestInstruction
            .startswith("SOLENOID");
        {
            if latestInstruction
                .endswith("OUT")
                {
                    digitalWrite(solenoid_pin, LOW);
                }
            if latestInstruction
                .endswith("IN")
                {
                    digitalWrite(solenoid_pin, HIGH);
                }
        }

        latestInstruction = ""; // Clear the string for the next input
        stringComplete = false; // Reset the flag
    }
}

void serialEvent()
{
    while (Serial.available())
    {
        // Get the new byte
        char inChar = (char)Serial.read();
        // Add it to the inputString
        latestInstruction += inChar;
        // If the incoming character is a newline, the string is complete
        if (inChar == '\n')
        {
            stringComplete = true;
        }
    }
}

void splitString(str data, char delimiter)
{
    while (startIndex < data.length())
    {
        endIndex = data.indexOf(delimiter, startIndex);

        // If the delimiter is found
        if (endIndex != -1)
        {
            part = data.substring(startIndex, endIndex);
            startIndex = endIndex + 1; // Move past the delimiter
        }
        else
        {
            // Last part with no delimiter
            part = data.substring(startIndex);
            startIndex = data.length(); // Exit loop
        }
    }
}