#define PUL_PIN 2         // 모터 펄스 핀
#define DIR_PIN 4         // 모터 방향 핀
#define ORIGIN_SENSOR_PIN 7  // 원점 센서 핀

bool rotate = true;
int AngleToMove = 0;
String inputStr;

void setup() {
    pinMode(PUL_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);
    pinMode(ORIGIN_SENSOR_PIN, INPUT_PULLUP);  // 원점 센서 풀업 설정

    Serial.begin(9600);
    
    // 초기 모터 설정
    digitalWrite(DIR_PIN, HIGH);  // 초기 방향 설정
    delay(500);                   // 초기화 대기
}

void generatePulse() { // 펄스 생성 함수
    if(rotate){
        digitalWrite(PUL_PIN, HIGH);
        delayMicroseconds(2);        // 펄스 폭
        digitalWrite(PUL_PIN, LOW);
        delayMicroseconds(2);        // 로우 레벨 폭
        delay(2);                    // 스텝 간격 조정
    }
}

void stop(){
    rotate = false;
}

void rotateonce(){
  digitalWrite(DIR_PIN, HIGH);  // 초기 방향 설정
  for(int j = 0; j< 120; j++) // 1회전 3도이므로 3*120 = 360
    for(int i = 0; i < 200; i++) {// 200펄스로 1회전 
        generatePulse();
    }
}

void rotateAngle() {
    if(AngleToMove > 0 && AngleToMove <= 360){
        digitalWrite(DIR_PIN, HIGH);  // 초기 방향 설정
        for (int j = 0; j < AngleToMove; j++) {
            for(int i = 0; i < 200/3; i++) {// 200펄스로 1회전 = 3도, 따라서 200/3 = 1도
                generatePulse();
            }
        }
    }
    else if(AngleToMove < 0 && AngleToMove >= -360){
        digitalWrite(DIR_PIN, LOW);  // 초기 방향 설정
        AngleToMove = -AngleToMove;
        for (int j = 0; j < AngleToMove; j++) {
            for(int i = 0; i < 200/3; i++) {// 200펄스로 1회전 = 3도, 따라서 200/3 = 1도
                generatePulse();
            }
        }
    }
}

void loop() {
    if (Serial.available() > 0) {
        inputStr = Serial.readStringUntil('\n');
        inputStr.trim();  // 입력 문자열의 앞뒤 공백 제거

        if(inputStr == "R"){rotateonce();}
        else if(inputStr == "S"){stop();}
        else {
            int angle = inputStr.toInt();
            AngleToMove = angle;
            rotateAngle();
        }
    }
}