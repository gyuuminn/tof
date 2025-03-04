from SDM15 import SDM15, BaudRate
import time
import csv

if __name__ == "__main__":
    lidar = SDM15("COM4", BaudRate.BAUD_460800) # change the port name to your own port
    
    version_info = lidar.obtain_version_info()
    print("get version info success")

    lidar.lidar_self_test()
    print("self test success")

    lidar.start_scan()
    with open('C:/Users/dlsdn/OneDrive/바탕 화면/스테이지/rotateandscan/SDM15lidar_data(distance, intensity).csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Distance", "Intensity"])
        while True:
            try:
                distance, intensity, _ = lidar.get_distance()
                print(f"distance: {distance}, intensity: {intensity}")
                writer.writerow([distance, intensity])
                file.flush()
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("Stopping data recording due to KeyboardInterrupt")
                break
# https://github.com/being24/YDLIDAR-SDM15_python