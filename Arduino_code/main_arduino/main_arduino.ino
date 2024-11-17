#include <Servo.h>

Servo myservo;

String command = "";
String latestInstruction = ""; // A string to hold incoming data
bool stringComplete = true;   // Whether the string is complete

int solenoid_pin = 8;
int servo_pwm_pin = 9;

int servo_state = 0;    // servo state is represented by its angle
int solenoid_state = 0; // solenoid state is represented by 0 or 1. SOLENOID OUT = 0; SOLENOID IN = 1

void setup() {
  Serial.begin(9600);
  pinMode(solenoid_pin, OUTPUT);
  pinMode(servo_pwm_pin, OUTPUT);
  pinMode(13, OUTPUT); // used for debugging
  myservo.attach(servo_pwm_pin);
}

void loop() {
  // Check if the string is complete

  if (stringComplete) {
    Serial.println(latestInstruction); // Print the received string for debugging

    if (latestInstruction.startsWith("SERVO")) {
      int delimiterIndex = latestInstruction.indexOf(" ");

      if (delimiterIndex != -1) {
        command = latestInstruction.substring(0, delimiterIndex);
        delimiterIndex += 1; // Move past the space
        servo_state = latestInstruction.substring(delimiterIndex).toInt(); // Convert to int
      }

      Serial.println(servo_state);  // Print the servo state
      myservo.write(servo_state);   // Move the servo
      digitalWrite(13, HIGH);
      delay(1000);
      digitalWrite(13, LOW);
    }

    if (latestInstruction.startsWith("SOLENOID")) {
      if (latestInstruction.endsWith("OUT")) {
        digitalWrite(solenoid_pin, LOW);
      }
      if (latestInstruction.endsWith("IN")) {
        digitalWrite(solenoid_pin, HIGH);
      }
    }

    latestInstruction = ""; // Clear the string for the next input
    stringComplete = false;  // Reset the flag
  }
}

void serialEvent() {
  while (Serial.available()) {
    // Get the new byte
    char inChar = (char)Serial.read();
    // Add it to the inputString
    latestInstruction += inChar;
    // If the incoming character is a newline, the string is complete
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}





/*



#include <Servo.h>
#include <StringSplitter.h>

Servo myservo;

String command ="";
String latestInstruction = ""; // A string to hold incoming data
bool stringComplete = false;   // Whether the string is complete
int delimeterIndex;
int n;

int solenoid_pin = 8;
int servo_pwm_pin = 9;

int servo_state = 0;    // servo state is represented by its angle
int solenoid_state = 0; // solenoid state is represented by 0 or 1. SOLENOID OUT = 0; SOLENOID IN = 1

void setup()
{
  Serial.begin(9600);
  pinMode(solenoid_pin, OUTPUT);
  pinMode(servo_pwm_pin, OUTPUT);
  pinMode(13, OUTPUT); // used for debugging
  myservo.attach(servo_pwm_pin);
}

void loop()
{
  // Check if the string is complete
  latestInstruction="SERVO 100";
  if (stringComplete)
  {
    Serial.println(latestInstruction); // Print the received string for debugging

    if (latestInstruction.startsWith("SERVO"))
    {

      int delimiterIndex = latestInstruction.indexOf(" ");

      if (delimiterIndex != -1){
        command = latestInstruction.substring(0, delimeterIndex);
        delimeterIndex += 1;
        servo_state = latestInstruction.substring(delimeterIndex).toInt();
      }



      Serial.println(servo_state);
      myservo.write(servo_state);
      digitalWrite(13, HIGH);
	    delay(1000);
	    digitalWrite(13, LOW);
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
*/