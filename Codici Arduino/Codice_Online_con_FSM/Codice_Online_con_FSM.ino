int cS;  
int fS;
unsigned long controllo;
 /*
0 = lettura pir      
1 = accensione led di avviso operazione  /  Serialwrite per l'invio del pacchetto  /  spegnimento led  /  intervallo di tempo per lasciare al pc il tempo di scattare le foto
 */


//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 10;

//the time when the sensor outputs a low impulse
//long unsigned int lowIn;

//the amount of milliseconds the sensor has to be low 
//before we assume all motion has stopped


int pirPin = 2;    //the digital pin connected to the PIR sensor's output
//int ledPin = 4;
unsigned long start_time;




void setup() {
  Serial.begin(9600);
  pinMode(pirPin, INPUT);
  //pinMode(ledPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(pirPin, LOW);
  //digitalWrite(ledPin, LOW);
  digitalWrite(LED_BUILTIN, LOW);

  //give the sensor some time to calibrate
  Serial.print("calibrating sensor ");
  start_time = millis();
  for(int i = 0; i < calibrationTime;){
    if(millis() - start_time > 1000){
      i++;
      Serial.print(i);
      Serial.print(" ");
      start_time = millis();
    }
  }
  Serial.println(" done");
  Serial.println("SENSOR ACTIVE");
  for(;;){
    if(millis() - start_time >300) break;
  }
  Serial.print("ciao bel");
  cS = 0;
  fS = 0;
}

void stato0(){
  int val = digitalRead(pirPin);
  if (val == HIGH){
    Serial.print("Movement detected at: ");
    Serial.println(millis());
    fS = 1;
  }
}

void stato1(){
  //digitalWrite(ledPin, HIGH);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.write(0xFF);
  Serial.write(0xFA);
  Serial.write(0xFE);
  start_time = millis();
  // qui si dice all'arduino di aspettare un secondo per dare tempo al pc di scattare una colezione di immagini da far elaborare alla CNN
  for(;;){
    controllo = millis() - start_time;
    if(controllo % 500 == 0)Serial.println(controllo);
    if(millis() - start_time > 1000) break;
  }
  //digitalWrite(ledPin, LOW);
  digitalWrite(LED_BUILTIN, LOW);
  fS = 0;
}

void loop() {

  if(cS == 0 && fS == 0) stato0();
  if(cS == 0 && fS == 1) cS = fS;
  if(cS == 1 && fS == 1) stato1();
  if(cS == 1 && fS == 0) cS = fS;

}
