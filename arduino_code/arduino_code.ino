#include <Servo.h>
Servo Esc0, Esc1,Esc2, Esc3, liftEsc_1, liftEsc_2;

#define ESC_SPEED_INIT 200
#define ESC_STOP 1500
#define ESC_SPEED_LIMIT 400
#define GRIPPER_SPEED 200
#define GRIPPER_STOP 0
#define GRIPPER_OPEN_STATE 1
#define GRIPPER_CLOSE_STATE 0


#define ESC0_PIN 6 // Back
#define ESC1_PIN 4 // Front
#define ESC2_PIN 7 // Front
#define ESC3_PIN 3 // Back
#define LIFT_ESC_PIN_1 2
#define LIFT_ESC_PIN_2 5
#define GRIPPER1_PWM_PIN 8
#define GRIPPER1_DIR_PIN 23
#define GRIPPER2_PWM_PIN 9
#define GRIPPER2_DIR_PIN 25
#define LED1 A8
#define LED2 A9
#define METAL_SENSOR 47
int rightAngle = ESC_STOP;
int leftAngle = ESC_STOP;
int liftAngle = ESC_STOP;

bool flash1State = LOW;
bool flash2State = LOW;

uint16_t _speed = 200;

void setup () {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Esc0.attach(ESC0_PIN);
  Esc1.attach(ESC1_PIN);
  Esc2.attach(ESC2_PIN);
  Esc3.attach(ESC3_PIN);
  liftEsc_1.attach(LIFT_ESC_PIN_1);
  liftEsc_2.attach(LIFT_ESC_PIN_2);
  pinMode(GRIPPER1_PWM_PIN, OUTPUT);
  pinMode(GRIPPER1_DIR_PIN, OUTPUT);
  pinMode(GRIPPER2_PWM_PIN, OUTPUT);
  pinMode(GRIPPER2_DIR_PIN, OUTPUT);
  analogWrite(GRIPPER1_PWM_PIN, GRIPPER_STOP);
  analogWrite(GRIPPER2_PWM_PIN, GRIPPER_STOP);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1,HIGH);
  digitalWrite(LED2,HIGH);
  pinMode(METAL_SENSOR, INPUT);
}

char i = 0;
char serial_data[5];

void loop() {
  if (millis() % 100 == 0) {
    if (digitalRead(METAL_SENSOR)) Serial.println("M1");
    else Serial.println("M0");
  }
  if (Serial.available()) {
    serial_data[i] = Serial.read(); i++;
  }
  if (i-1 > 4) {
    while(Serial.available()) Serial.read();
    i = 0;
  }
  if (serial_data[i-1] == '\n' && i-1 > 0) {
    serial_data[i-1] = '\0';
    Move(serial_data);
    i = 0;
  }
}

