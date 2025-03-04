import serial
import time
import threading
# Arduino와의 직렬 통신 설정
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)  # 포트는 아두이노에 맞게 설정 (예: COM3 또는 /dev/ttyUSB0)

time.sleep(2)  # 연결 초기화 대기
def read_from_arduino():
    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                if line:  # Non-empty line
                    print(f"\n{line}\n")  # 실시간으로 Arduino 메시지 출력
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            break
        time.sleep(0.1)

# 별도의 스레드에서 Arduino로부터 데이터를 읽어들임
thread = threading.Thread(target=read_from_arduino, daemon=True)
thread.start()

try:
    while True:
        user_input = input("Enter an angle to rotate, 'R' to rotate once, 'S' to stop: ")
        
 # 입력 값 검증
        if user_input.upper() == "S" or user_input.upper() == "R":
            user_input = user_input.upper()
            arduino.write(f"{user_input}".encode())  # "R" 또는 "S" 명령 전송
            print(f"Sent to Arduino: {user_input}")
            
        else:
            try:
                # 사용자 입력을 정수로 변환
                target_angle = int(user_input)  
                if target_angle > 360 or target_angle < -360:
                    print("각도는 -360도 ~ 360도 사이여야 합니다.")
                    continue
                else:
                    arduino.write(f"{target_angle}".encode())  # 목표 각도 전송
                    print(f"Sent to Arduino: {target_angle}")
                    
            except ValueError:
                print("유효하지 않은 명령입니다. 'R', 'S' 또는 각도를 입력하세요.")
                
except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
finally:
    arduino.close()
    
#txt, 정지 method, 각 입력, 왼쪽, 오른쪽 제어
# 200스텝이 1회전 