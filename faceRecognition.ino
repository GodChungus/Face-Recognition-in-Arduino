const int greenLED = 8;
const int redLED = 9;

void setup() {
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char incoming = Serial.read();

    if (incoming == '1') {
      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
    }
    else if (incoming == '0') {
      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);
    }
  }
}
