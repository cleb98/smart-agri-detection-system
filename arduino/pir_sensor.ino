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
  if(movimento == false){
    if(val == HIGH){
      timeMark = millis();
      movimento = true;
      digitalWrite(led, HIGH);
      // Movement detected!
      Serial.write(0xFF);
      Serial.write(0xFA);
      Serial.write(0xFE);
      // Package sent!
    }
  }
  else{
    if(millis() - timeMark > 5000){
      movimento = false;
      digitalWrite(led, LOW);
    }
  }
}