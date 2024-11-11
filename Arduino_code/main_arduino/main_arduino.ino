String latestInstruction = ""; // A string to hold incoming data
bool stringComplete = false;   // Whether the string is complete

int solenoid_pin = 4
int servo_pwm_pin = 5

    void
    setup()
{
    Serial.begin(9600);
    pinMode(solenoid_pin, OUTPUT)
        pinMode(servo_pwm_pin, OUTPUT)
}

void loop()
{
    // Check if the string is complete
    if (stringComplete)
    {

        Serial.println(latestInstruction) // Print the received string for debugging

            if latestInstruction.startswith("SERVO")
        {
            // do servo things
        }
        if latestInstruction
            .startswith("SOLENOID")
            {
                // do solenoid things
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
