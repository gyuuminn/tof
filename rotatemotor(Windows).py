import serial
import time
import threading

# Arduino와의 직렬 통신 설정
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)  # 포트 설정

time.sleep(2)  # 연결 초기화 대기

# Arduino로부터 데이터 읽기 함수
def read_from_arduino():
    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                if line:  # 비어 있지 않은 라인만 출력
                    print(f"\n{line}\n")  # Arduino 메시지를 출력
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            break
        time.sleep(0.1)

# 스레드로 Arduino 읽기 함수 실행
thread = threading.Thread(target=read_from_arduino, daemon=True)
thread.start()

try:
    while True:
        user_input = input("Enter an angle to rotate, 'R' to rotate half, 'S' to stop: ")

        if user_input.upper() == "S" or user_input.upper() == "R":
            user_input = user_input.upper()
            arduino.write(f"{user_input}\n".encode())  # 명령어 전송
            print(f"Sent to Arduino: {user_input}")
            
        else:
            try:
                target_angle = int(user_input)
                if target_angle > 360 or target_angle < -360:
                    print("각도는 -360도 ~ 360도 사이여야 합니다.")
                    continue
                else:
                    arduino.write(f"{target_angle}\n".encode())  # 각도 전송
                    print(f"Sent to Arduino: {target_angle}")
                    
            except ValueError:
                print("유효하지 않은 명령입니다. 'R', 'S' 또는 각도를 입력하세요.")
                
except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
finally:
    arduino.close()
