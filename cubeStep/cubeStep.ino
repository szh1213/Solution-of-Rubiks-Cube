int dir[]={2,4,6,8,10,12};
int pul[]={3,5,7,9,11,13};
int mic[]={2,2,2,2,2,2};
int steps[]={6400,6400,6400,6400,6400,6400};
void setup() {
  for(int i=0;i<6;i++){
    pinMode(dir[i],OUTPUT);
    pinMode(pul[i],OUTPUT);
  }
  Serial.begin(115200);
  while (!Serial);
}

void loop() {
  char ord = Serial.read();
  switch(ord){
    case 'F': rotate(0,0);Serial.print('F');break;
    case 'B': rotate(1,0);Serial.print('B');break;
    case 'L': rotate(2,0);Serial.print('L');break;
    case 'R': rotate(3,0);Serial.print('R');break;
    case 'U': rotate(4,0);Serial.print('U');break;
    case 'D': rotate(5,0);Serial.print('D');break;
    case 'f': rotate(0,1);Serial.print('f');break;
    case 'b': rotate(1,1);Serial.print('b');break;
    case 'l': rotate(2,1);Serial.print('l');break;
    case 'r': rotate(3,1);Serial.print('r');break;
    case 'u': rotate(4,1);Serial.print('u');break;
    case 'd': rotate(5,1);Serial.print('d');break;
  }
  delay(100);
}
void rotate(int face,int turn){
  digitalWrite(dir[face],turn);
  for(int i=0;i<steps[face];i++){
    digitalWrite(pul[face],HIGH);
    delayMicroseconds(mic[face]);
    digitalWrite(pul[face],LOW);
    delayMicroseconds(mic[face]);
  }
}

