int led = 13;
int sensor = 2;
int state = LOW;
int val = 0;
bool movimento = false;

unsigned long timeMark;
unsigned long setupTime = 5000;
unsigned long setupStart;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(sensor, INPUT);
  Serial.begin(9600);
  //Setting up PIR sensor...
  setupStart = millis();
  while (millis() - setupStart < setupTime) {
  }
  // Setting complete!
}

void loop() {
  val = digitalRead(sensor);
  if (movimento == false) {
    if (val == HIGH) {
      timeMark = millis();
      movimento = true;
      //digitalWrite(led, HIGH);
      // Movement detected!
      Serial.write(0xFF);
      Serial.write(0xFA);
      Serial.write(0xFE);
      // Package sent!
    }
  }

  if (millis() - timeMark > 5000) {
    movimento = false;
    //digitalWrite(led, LOW);
    checkSerialPackets();
}
  }



void checkSerialPackets() {
  while (Serial.available() >= 3) {
    byte packet[3];
    for (int i = 0; i < 3; i++) {
      packet[i] = Serial.read();
    }
    if (packet[0] == 0xAA && packet[1] == 0xAB) {
      if (packet[2] == 0xAC && !digitalRead(led)) {
        digitalWrite(led, HIGH); // Accendi il LED solo se è spento
      } else if (packet[2] == 0xAD && digitalRead(led)) {
        digitalWrite(led, LOW); // Spegni il LED solo se è acceso
      }
    }
  }
}


