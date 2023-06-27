const int sensorPin1 = A0; // pinul analog pe care este conectat primul senzor - SUNET
const int sensorPin2 = A1; // pinul analog pe care este conectat al doilea senzor - GAZ
const int sensorPin3 = A2; // pinul analog pe care este conectat al treilea senzor - LUMINA

volatile int sensorValue1 = 0; // valoarea citita de la primul senzor
volatile int sensorValue2 = 0; // valoarea citita de la al doilea senzor
volatile int sensorValue3 = 0; // valoarea citita de la al treilea senzor

const int buzzPin =  2;     // pinul digital pe care este conectat buzzer-ul
bool buzz = false;

void setup() {
  Serial.begin(9600); // configureaza portul serial la o rata de transfer de 9600 de biti pe secunda
  pinMode(buzzPin, OUTPUT);
}

void loop() {
  sensorValue1 = analogRead(sensorPin1); 
  delay(10);
  sensorValue2 = analogRead(sensorPin2); 
  delay(10);
  sensorValue3 = analogRead(sensorPin3); 
  
  Serial.print(sensorValue1); 
  Serial.print(";");        
  Serial.print(sensorValue2); 
  Serial.print(";");
  Serial.println(sensorValue3); //new line

  int valoarePrag = 800; // Valoarea de prag pentru activarea buzzer-ului

  bool senzor1DepasestePrag = sensorValue1 > valoarePrag;
  bool senzor2DepasestePrag = sensorValue2 > valoarePrag;
  bool senzor3DepasestePrag = sensorValue3 > valoarePrag;

  if (senzor1DepasestePrag == false && senzor2DepasestePrag == false && senzor3DepasestePrag == false)
    buzz = true;

  if (senzor1DepasestePrag && buzz) {
    soundBuzzer(1);
    buzz = false;
  } else if (senzor2DepasestePrag && buzz) {
    soundBuzzer(2);
    buzz = false;
  } else if (senzor3DepasestePrag && buzz) {
    soundBuzzer(3);
    buzz = false;
  }

  delay(100);
}

void soundBuzzer(int numarBipe) {
  for (int i = 0; i < numarBipe; i++) {
    digitalWrite(buzzPin, HIGH);
    delay(100);
    digitalWrite(buzzPin, LOW);
    if (i < numarBipe - 1) {
      delay(100);
    }
  }
}