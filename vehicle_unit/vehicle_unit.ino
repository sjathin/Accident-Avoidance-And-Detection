/*
 *  HC_SRO3
 *     trigger - pwm3
 *     echo - pwm4
 *     gnd - pwm5
 *  LED_ACC
 *     resistor red side 51(digital)
 *     resistor gold side longer end of led
 *     shorter end of led to GND
 *  MQ3
 *     mq3 a0 to arduino a0
 *     GND TO GND\
 *  ACCELEROMETER
 *     xaxis - A3
 *     yaxis - A2
 *     zaxis - A1
 *     vcc - 3.3
 *     gnd - gnd
 *  FLAME
 *    d0 - 22
 *    gnd - gnd
 *  GSM
 *    RX to digital 11
 *    TX to digital 10
 *    Vcc to 5v
 */

int alcohol_flag = 0;
int accident_flag = 0;
int trig = 3;
int echo = 4;
int hc_gnd = 5;
int led_flag = 0;
int val = 0;
const int groundpin = 18;             // analog input pin 4 -- ground
const int powerpin = 19;              // analog input pin 5 -- voltage
const int xpin = A3;                  // x-axis of the accelerometer
const int ypin = A2;                  // y-axis
const int zpin = A1;                  // z-axis (only on 3-axis models)
float xrest = 0;
float yrest = 0;
float zrest = 0;
int analoog = A5;
int sensorReading = 0;
const int knockSensor = A8;
int fla_val = 0;
int check = 0;
int buttonpin = 22;
float sensor;
int flame_val;
long lat,lon;
#define DEBUG true
String forthValue="LL",fifthValue="LL";



#include <SoftwareSerial.h>
#include<string.h>

SoftwareSerial mySerial(10, 11);


void setup() {
  mySerial.begin(9600);   // Setting the baud rate of GSM Module  
  Serial.begin(9600);    // Setting the baud rate of Serial Monitor (Arduino)
  delay(100);
  pinMode (hc_gnd,OUTPUT);
   pinMode (buttonpin, INPUT) ;
  pinMode(51, OUTPUT);
  pinMode (analoog, INPUT) ;// output interface defines the flame sensor
  getgps();
  delay(1000);
  xrest = analogRead(xpin);
yrest = analogRead(ypin);
 zrest = analogRead(zpin);
 
}

void loop() {
    if(check != 0)
    {
           getgps();
      check = gps();
    }
    if(check == 0)
    {
      accident_flag = 0;
      alcohol_flag = 0;
      alcohol();
      //delay(1000);
      hcsr();
      //delay(1000);
      acc();
      //delay(1000);
      flame();
      //delay(1000);
      knock();
      if(accident_flag==1 || alcohol_flag==1)
      {
        Serial.println("ACCIDENT!!!");
        pos();
      }
      else
      {
        Serial.println("No accident");
      }
   }
}


void knock()
{
    Serial.println("knock:");
     sensorReading = analogRead(knockSensor);
  // if the sensor reading is greater than the threshold:
    Serial.println(sensorReading);
    if (sensorReading >= 30)
    {
        accident_flag = 1;
        //on_led();
    }
    //delay(100);
    //off_led();
}



void flame()
{
   Serial.println("flame:");
   val = digitalRead (buttonpin) ;// digital interface will be assigned a value of 3 to read val
   Serial.println(val);
   if (val == HIGH) // When the flame sensor detects a signal, LED flashes
  {
      accident_flag = 1;
      //on_led();
      //delay(100);
  }
  else
  {
  }
    //off_led();

}


void acc()
{
      Serial.println("acceleo");
     float x = analogRead(xpin);  //read from xpin
     delay(1); //
     float y = analogRead(ypin);  //read from ypin
     delay(1); 
     float z = analogRead(zpin);  //read from zpin
     float x1 = x-xrest;
     float y1 = y-yrest;
     float z1 = z-zrest;
     float g = sqrt((x1*x1) + (y1*y1) + (z1*z1));
     Serial.println(g);
     if(g>50000.00)
     {
          accident_flag=1;
          Serial.println("Threshold exceded"); 
          //on_led();
     }
    //delay(100);
    //off_led();
}


void alcohol()
{
        Serial.println("alcohol");
        val = analogRead(A0);
        Serial.println(val);
        delay(100);
        if(val > 400)
        {
          alcohol_flag = 1;
          //on_led();
        }
        //delay(100);
        //off_led();
}


void hcsr()
{
    Serial.println("hcsr");
    long duration, inches, cm;
    pinMode(trig, OUTPUT);
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(5);
    digitalWrite(trig, LOW);
    pinMode(echo,INPUT);
    duration = pulseIn(echo, HIGH);
    inches = microsecondsToInches(duration);
    cm = microsecondsToCentimeters(duration);
    Serial.print(inches);
    //Serial.print("in, ");
    if(inches > 6 && inches <10)  
    {
      accident_flag = 1;
      Serial.println("Threshold exceeded");
      //on_led();
    }
    //delay(100);
      //off_led();
}

long microsecondsToInches(long microseconds)
{
    return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds)
{
    return microseconds / 29 / 2;
}

void on_led()
{
   digitalWrite(51,HIGH);
   led_flag =1;
   delay(100);
}

void off_led()
{
  if(led_flag==1)
  {
    digitalWrite(51,LOW);
    delay(100);
  }
  led_flag = 0;
}


void pos()
{
    sendData( "AT+CGNSINF",1000,DEBUG);   
    delay(1000);
     SendMessage();
}

void getgps(void)
{
   sendData( "AT+CGNSPWR=1",1000,DEBUG); 
   sendData( "AT+CGNSSEQ=RMC",1000,DEBUG); 
}


void SendMessage()
{
    String message = "CAR NO: |KA ** ** ****|latitude:|";
    message.concat(forthValue);
    message.concat("|longitude:|");
    message.concat(fifthValue);
    //Serial.println(message);
    message.concat("|");
    if(alcohol_flag==1 && accident_flag==1)
    {
        message.concat("A");
    }
    else if(alcohol_flag ==1 && accident_flag==0)
    {
        message.concat("T");
    }
    else if(alcohol_flag==0 && accident_flag==1)
    {
        message.concat("A");
    }
    mySerial.println("AT+CMGF=1");    //Sets the GSM Module in Text Mode
    delay(1000);  // Delay of 1000 milli seconds or 1 second
    mySerial.println("AT+CMGS=\"+919742420140\"\r"); // Replace x with mobile number
    delay(1000);
    mySerial.println(message);// The SMS text you want to send
    //mySerial.println(forthValue);
    //mySerial.println("\n");
    //mySerial.println(fifthValue);
    delay(100);
    mySerial.println((char)26);// ASCII code of CTRL+Z
    delay(1000);
}


String sendData(String command, const int timeout, boolean debug)
{
    String response = "";    
    mySerial.println(command); 
    long int time = millis(); // Returns the number of milliseconds since the Arduino board began running the current program
    while( (time+timeout) > millis())
    {
      while(mySerial.available())
      {       
        char c = mySerial.read(); 
        response+=c;
      }  
    }    
    int commaIndex = response.indexOf(',');
    int secondCommaIndex = response.indexOf(',', commaIndex+1);
    int thirdCommaIndex = response.indexOf(',', secondCommaIndex+1);
    int forthCommaIndex = response.indexOf(',', thirdCommaIndex+1);
    int fifthCommaIndex = response.indexOf(',', forthCommaIndex+1);
    String firstValue = response.substring(0, commaIndex);
    String secondValue = response.substring(commaIndex+1, secondCommaIndex);
    String thirdValue = response.substring(secondCommaIndex+1,thirdCommaIndex);
    forthValue = "12.861514";
    fifthValue = "77.664740";
    //forthValue = response.substring(thirdCommaIndex+1,forthCommaIndex);
    //fifthValue = response.substring(forthCommaIndex+1,fifthCommaIndex); 
    Serial.print("lat:");
    Serial.print(forthValue);
    Serial.print("long:");
    Serial.print(fifthValue);
    return response;
}


int checkgps(String command, const int timeout, boolean debug)
{
    String response = "";    
    mySerial.println(command); 
    long int time = millis(); // Returns the number of milliseconds since the Arduino board began running the current program
    while( (time+timeout) > millis())
    {
      while(mySerial.available())
      {       
        char c = mySerial.read(); 
        response+=c;
      }  
    }    
    int commaIndex = response.indexOf(',');
    int secondCommaIndex = response.indexOf(',', commaIndex+1);
    int thirdCommaIndex = response.indexOf(',', secondCommaIndex+1);
    int forthCommaIndex = response.indexOf(',', thirdCommaIndex+1);
    int fifthCommaIndex = response.indexOf(',', forthCommaIndex+1);
    String firstValue = response.substring(0, commaIndex);
    String secondValue = response.substring(commaIndex+1, secondCommaIndex);
    String thirdValue = response.substring(secondCommaIndex+1,thirdCommaIndex);
    //if(forthValue.length() == 6)
    //{
        forthValue = response.substring(thirdCommaIndex+1,forthCommaIndex);
    //}
    //if(fifthValue.length() == 6)
    //{
        fifthValue = response.substring(forthCommaIndex+1,fifthCommaIndex); 
    //}
    if((forthValue.length() != 0)  && (fifthValue.length() != 0))
    {
        Serial.println("GPS ON");
        Serial.println(forthValue);
        Serial.println(fifthValue);
        return 0;
    }
    return 1;
}



int gps()
{
    int a;
    a = checkgps("AT+CGNSINF",1000,DEBUG);  
    return a;
}

