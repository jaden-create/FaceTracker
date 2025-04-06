#include <Servo.h>
Servo Base;
Servo Top;

int dx = 0;
int dy = 0;
int lastDx = 0;
int lastDy = 0;
float x = 1500;
float y = 1750;
float KPx = 1 / 20.0;
float KPy = 1 / 20.0;
float KDx = 10;
float KDy = 10;

int loopTime = 20;

float KIx = 0;
float sumErrorX = 0;
float KIy = 0;
float sumErrorY = 0;
int IcapX =0;//cycles of loop time
int countX = 0;
int IcapY = 0;
int countY = 0;


unsigned long time = 0;
unsigned long time2 = 0;

void BaseTurn() {


  // Base
  x += dx * KPx;
  x += ((dx - lastDx) / loopTime) * KDx;

  sumErrorX += dx;
  x += sumErrorX * KIx;



  x = constrain(x, 700, 2300);
  Base.writeMicroseconds(int(x));

  lastDx = dx;
  countX ++;
  if (countX >IcapX){
    sumErrorX = 0;
    countX=0;
  }
}

void TopTurn() {
  // Top
  y += dy * KPy;
  y += ((dy - lastDy) / loopTime) * KDy;

  sumErrorY += dy;
  y += sumErrorY * KIy;

  y = constrain(y, 1500, 2000);
  Top.writeMicroseconds(int(y));
  lastDy = dy;

  countY ++;
  if (countY >IcapY){
    sumErrorY = 0;
    countY=0;
  }

}



void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  Base.attach(3);
  Top.attach(5);
  Base.write(x);
  Top.write(y);
}



void loop() {


  if (Serial.available() > 0) {
    dx = -1*Serial.parseInt();  // Read first integer
    dy = -1*Serial.parseInt();  // Read first integer
    Serial.read();
  }

  BaseTurn();
  TopTurn();


  delay(loopTime);
  


}

/*Serial.print("Angle Command");
  Serial.print(x);
  Serial.print(" dX");
  Serial.print(dx);
  Serial.print(" dY");
  Serial.print(dy);
  Serial.print(" y");
  Serial.println(y);*/
