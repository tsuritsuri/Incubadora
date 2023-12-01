#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <HX711.h>

#define ONE_WIRE_BUS_2 2

OneWire oneWire2(ONE_WIRE_BUS_2);
DallasTemperature sensors2(&oneWire2);
HX711 balanza;

// Configuración del pin al que está conectado el bus OneWire
// Cambia esto al pin que estés utilizando
const int DOUT = A2;
const int CLK = A3;
const int pinRele = 3;
const int ventiladorPin = 4;
float Vin=5.0;     // [V]        
float Rt=10000;    // Resistor t [ohm]
float R0=10000;    // value of rct in T0 [ohm]
float T0=298.15;   // use T0 in Kelvin [K]
float Vout0=0.0;    // Vout in A0 
float Vout1=0.0;
float Rout0=0.0;    // Rout in A0
float Rout1=0.0;
// use the datasheet to get this data.
float T1=273.15;      // [K] in datasheet 0º C
float T2=373.15;      // [K] in datasheet 100° C
float RT1=27513;   // [ohms]  resistence in T1
float RT2=983;    // [ohms]   resistence in T2
float beta=0.0;    // initial parameters [K]
float Rinf=0.0;    // initial parameters [ohm]   
float TempK0=0.0;   // variable output
float TempC0=0.0;   // variable output
float TempK1=0.0;
float TempC1=0.0;
float targetTemperature = 30.0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  sensors2.begin();
  pinMode(ventiladorPin, OUTPUT);
    // Configurar el pin del relé como salida
  pinMode(pinRele, OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  // Desactivar el relé al inicio
  digitalWrite(pinRele, LOW);

  balanza.begin(DOUT, CLK);
  balanza.set_scale(102406); // Establecemos la escala
  balanza.tare();

  beta=(log(RT2/RT1))/((1/T1)-(1/T2));
  Rinf=R0*exp(-beta/T0);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Llamada para actualizar la información de los sensores
  Vout0=Vin*((float)(analogRead(0))/1024.0); // calc for ntc
  Rout0=(Rt*Vout0/(Vin-Vout0));

  TempK0=(beta/log(Rout0/Rinf)); // calc for temperature
  TempC0=TempK0-273.15;

  Vout1=Vin*((float)(analogRead(1))/1024.0); // calc for ntc
  Rout1=(Rt*Vout1/(Vin-Vout1));

  TempK1=(beta/log(Rout1/Rinf)); // calc for temperature
  TempC1=TempK1-273.15;
  
    // Imprimir la temperatura en el monitor serial
    Serial.print("Ambiente: ");
    Serial.print(TempC0);
    Serial.println(" °C");

    Serial.print("Calefactor: ");
    Serial.print(TempC1);
    Serial.println(" °C");

    sensors2.requestTemperatures();
    float ds18b20Temperature2 = sensors2.getTempCByIndex(0);
    Serial.print("Guagua: ");
    Serial.println(ds18b20Temperature2);

    Serial.print("Peso: ");
    Serial.print(balanza.get_units(20), 2);
    Serial.println(" kg");

    if (TempC0 < targetTemperature) {
      // Activar el relé
      digitalWrite(pinRele, HIGH);
      digitalWrite(ventiladorPin, LOW);
      }
    else {
      // Desactivar el relé
      digitalWrite(pinRele, LOW);
      digitalWrite(ventiladorPin, HIGH);
    }
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (!(input.startsWith("NEW"))) {   //probar startsWith("SET")
      targetTemperature = input.substring(4).toFloat();
    }
  }

  delay(1000);
}
