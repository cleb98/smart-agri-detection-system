int fS = 0;
unsigned long lastMillis;
unsigned long packetSentMillis;
const unsigned long SERIAL_INTERVAL = 1000;
const unsigned long DEBOUNCE_TIME = 200;
const int PIR_PIN = 2;
const int LED_PIN = LED_BUILTIN;

void setup() {
  Serial.begin(9600);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - lastMillis >= SERIAL_INTERVAL) {
    Serial.println("Sensor active");
    lastMillis = currentMillis;
  }
  if (fS == 0) {
    int pirValue = digitalRead(PIR_PIN);
    if (pirValue == HIGH && (currentMillis - packetSentMillis) > 5000) {
      Serial.print("Movement detected at: ");
      Serial.println(millis());
      digitalWrite(LED_PIN, HIGH);
      Serial.write(0xFF);
      Serial.write(0xFA);
      Serial.write(0xFE);
      Serial.println("Packet sent");
      packetSentMillis = currentMillis;
      fS = 1;
    }
  } else {
    unsigned long elapsedTime = currentMillis - lastMillis;
    if (elapsedTime >= DEBOUNCE_TIME) {
      digitalWrite(LED_PIN, LOW);
      lastMillis = currentMillis;
      fS = 0;
    }
  }
}
