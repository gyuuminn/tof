######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# TF-Luna Mini LiDAR wired to a Raspberry Pi via UART
# --- Real-time ranging with signal strength indicator
#
#
######################################################
#
import serial,time
import numpy as np
#
############################
# Serial Functions
############################
#
def read_tfluna_data():
    while True:
        counter = ser.in_waiting # count the number of bytes waiting to be read
        bytes_to_read = 9
        if counter > bytes_to_read-1:
            bytes_serial = ser.read(bytes_to_read) # read 9 bytes
            ser.reset_input_buffer() # reset buffer

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                temperature = (temperature/8) - 256 # temp scaling and offset
                return distance,strength,temperature

def set_samp_rate(samp_rate=100):
    ##########################
    # change the sample rate
    samp_rate_packet = [0x5a,0x06,0x03,samp_rate,00,00] # sample rate byte array
    ser.write(samp_rate_packet) # send sample rate instruction
    return
            
def get_version():
    ##########################
    # get version info
    info_packet = [0x5a,0x04,0x14,0x00]

    ser.write(info_packet) # write packet
    time.sleep(0.1) # wait to read
    bytes_to_read = 30 # prescribed in the product manual
    t0 = time.time()
    while (time.time()-t0)<5:
        counter = ser.in_waiting
        if counter > bytes_to_read:
            bytes_data = ser.read(bytes_to_read)
            ser.reset_input_buffer()
            if bytes_data[0] == 0x5a:
                version = bytes_data[3:-1].decode('utf-8')
                print('Version -'+version) # print version details
                return
            else:
                ser.write(info_packet) # if fails, re-write packet
                time.sleep(0.1) # wait

def set_baudrate(baud_indx=4):
    ##########################
    # get version info
    baud_hex = [[0x80,0x25,0x00], # 9600
                [0x00,0x4b,0x00], # 19200
                [0x00,0x96,0x00], # 38400
                [0x00,0xe1,0x00], # 57600
                [0x00,0xc2,0x01], # 115200
                [0x00,0x84,0x03], # 230400
                [0x00,0x08,0x07], # 460800
                [0x00,0x10,0x0e]]  # 921600
    info_packet = [0x5a,0x08,0x06,baud_hex[baud_indx][0],baud_hex[baud_indx][1],
                   baud_hex[baud_indx][2],0x00,0x00] # instruction packet 

    prev_ser.write(info_packet) # change the baud rate
    time.sleep(0.1) # wait to settle
    prev_ser.close() # close old serial port
    time.sleep(0.1) # wait to settle
    ser_new =serial.Serial("COM8", baudrates[baud_indx],timeout=0) # 포트 번호 확인
    if ser_new.isOpen() == False:
        ser_new.open() # open serial port if not open
    bytes_to_read = 8
    t0 = time.time()
    while (time.time()-t0)<5:
        counter = ser_new.in_waiting
        if counter > bytes_to_read:
            bytes_data = ser_new.read(bytes_to_read)
            ser_new.reset_input_buffer()
            if bytes_data[0] == 0x5a:
                indx = [ii for ii in range(0,len(baud_hex)) if \
                        baud_hex[ii][0]==bytes_data[3] and
                        baud_hex[ii][1]==bytes_data[4] and
                        baud_hex[ii][2]==bytes_data[5]]
                print('Set Baud Rate = {0:1d}'.format(baudrates[indx[0]]))
                time.sleep(0.1) 
                return ser_new
            else:
                ser_new.write(info_packet) # try again if wrong data received
                time.sleep(0.1) # wait 100ms
                continue

#
############################
# Configurations
############################
#
baudrates = [9600,19200,38400,57600,115200,230400,460800,921600] # baud rates
prev_indx = 4 # previous baud rate index (current TF-Luna baudrate)
prev_ser = serial.Serial("COM8", baudrates[prev_indx],timeout=0) # 포트 번호 확인
if prev_ser.isOpen() == False:
    prev_ser.open() # open serial port if not open
baud_indx = 4 # baud rate to be changed to (new baudrate for TF-Luna)
ser = set_baudrate(baud_indx) # set baudrate, get new serial at new baudrate
set_samp_rate(100) # set sample rate 1-250
get_version() # print version info for TF-Luna


print('Starting Ranging...')
try:
    while True:
        try:
            distance, strength, temperature = read_tfluna_data()  # read values
            print(f"Distance: {distance:.2f} cm, Strength: {strength}, Temperature: {temperature:.2f} °C")
            time.sleep(0.1)  # Add a delay for readability
        except Exception as e:
            print("Error reading data:", e)
            continue
except KeyboardInterrupt:
    print("Stopping measurement...")
finally:
    ser.close()
