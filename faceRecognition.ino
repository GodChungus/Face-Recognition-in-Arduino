#include <Servo.h>

// Pin numbers for the components
const int greenLED = 8;
const int redLED = 9;
const int servoPin = 5;

Servo theServo;

void setup() {
  // We're gonna use the LEDs to output.
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  // Make sure the LEDs are off when starting.
  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);

  Serial.begin(9600); // Baud rate(number of signals sent per second)

  theServo.attach(servoPin);
  theServo.write(0);
}

void loop() {
  if (Serial.available() > 0) { // only does data checking if data is actually available
    char incoming = Serial.read();

    if (incoming == '1') { // if face is recognized
      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
      theServo.write(90); // set servo motor to a rotation of 90 degrees
    }
    else if (incoming == '0') {
      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);
      theServo.write(0); // set servo motor to a rotation of 0 degrees
    }
  }
}
