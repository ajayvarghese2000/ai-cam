#include <SoftwareSerial.h>

// software serial : TX = digital pin 10, RX = digital pin 11
SoftwareSerial portOne(10, 11);

void setup()
{
  // Start the hardware serial port
  Serial.begin(9600);

  // Start both software serial ports
  portOne.begin(9600);;

}

void loop()
{
  portOne.listen();

  if (portOne.isListening()) 
  {
    if (Serial.available() > 0) 
    {
      // read the incoming byte:
      incomingByte = Serial.readString()
  
      // say what you got:
      Serial.print("I received: ");
      Serial.println(incomingByte, DEC);
    }
  }
  else
  {
    Serial.println("Port One is not listening!");
  }

}
