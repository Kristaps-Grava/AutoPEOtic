#include <Servo.h>

Servo servo;

String latestInstruction = ""; // A string to hold incoming data
bool stringComplete = true;    // Whether the string is complete

int solenoid_pin = 8;
int servo_pwm_pin = 9;

int servo_state = 0;    // servo state is represented by its angle
int solenoid_state = 0; // solenoid state is represented by 0 or 1. SOLENOID OUT = 0; SOLENOID IN = 1

void setup()
{
  Serial.begin(115200);
  pinMode(solenoid_pin, OUTPUT);
  pinMode(servo_pwm_pin, OUTPUT);
  servo.attach(servo_pwm_pin);

  servo.write(180);
  delay(500);
  servo.write(90);
  delay(500);
  servo.write(180);
}

void loop()
{
  // Check if the string is complete

  if (stringComplete)
  {
    // Serial.println(latestInstruction); // Print the received string for debugging

    if (latestInstruction.startsWith("WIRE"))
    {
      servo.write(0);
      delay(1000);
      servo.write(180);
    }

    if (latestInstruction.startsWith("SOLENOID"))
    {
      if (latestInstruction.endsWith("OUT"))
      {
        digitalWrite(solenoid_pin, LOW);
      }
      if (latestInstruction.endsWith("IN"))
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