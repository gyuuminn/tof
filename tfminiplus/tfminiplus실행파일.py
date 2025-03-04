'''=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# File Name: tfmp_test.py
# Inception: 14 MAR 2021
# Developer: Bud Ryerson
 # v0.0.18 - 21 MAY 2021
 # v0.1.0  - 06 SEP 2021 - Corrected (reversed) Enable/Disable commands.
             Changed three command names
               OBTAIN_FIRMWARE_VERSION is now GET_FIRMWARE_VERSION
               RESTORE_FACTORY_SETTINGS is now HARD_RESET
               SYSTEM_RESET is now SOFT_RESET
#
# Description: A Python script for the Raspberry Pi to test the
# Benewake TFMini Plus time-of-flight Lidar ranging sensor in
# Serial (UART) mode using the 'tfmplus' module in development.

# Default settings for the TFMini-Plus device are a 115200 serial baud rate
# and a 100Hz measurement frame rate. The device begins returning serial data
# immediately and asynchronously.  The data frame includes three measurments:
#   Distance in centimeters,
#   Signal strength in arbitrary units and
#   Temperature encoded for degrees centigrade

# Use the 'sendCommand()' to send commands and a parameters.
# The function returns a boolean result and sets a one byte status code.
# Command strings are defined in the module's list of commands.
# Parameters can be entered directly (115200, 250, etc) but for safety,
# they should be chosen from the module's string definitions.

# NOTE:
#   GPIO15 (RPi Rx pin) connects to the TFMPlus Tx pin and
#   GPIO14 (RPi Tx pin) connects to the TFMPlus Rx pin
#
# Press Ctrl-C to break the loop
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'''

# Skip a line and say 'Hello!'
print( "\n\rTFMPlus Module Example - 06SEP2021")

import time
import sys
import tfmini as tfmP   # Import the `tfmplus` module v0.1.0
from tfmini import *    # and command and paramter defintions

serialPort = "COM3"  ############ 시리얼 포트 번호 확인 ############
serialRate = 115200          # TFMini-Plus default baud rate

# - - - Set and Test serial communication - - - -
print( "Serial port: ", end= '')
if( tfmP.begin( serialPort, serialRate)):
    print( "ready.")
else:
    print( "not ready")
    sys.exit()   #  quit the program if serial not ready

# - - Perform a system reset - - - - - - - -
print( "Soft reset: ", end= '')
if( tfmP.sendCommand( SOFT_RESET, 0)):
    print( "passed.")
else:
    tfmP.printReply()
# - - - - - - - - - - - - - - - - - - - - - - - -
time.sleep(0.5)  # allow 500ms for reset to complete

# - - Get and Display the firmware version - - - - - - -
print( "Firmware version: ", end= '')
if( tfmP.sendCommand( GET_FIRMWARE_VERSION, 0)):
    print( str( tfmP.version[ 0]) + '.', end= '') # print three numbers
    print( str( tfmP.version[ 1]) + '.', end= '') # separated by a dot
    print( str( tfmP.version[ 2]))
else:
    tfmP.printReply()
# - - - - - - - - - - - - - - - - - - - - - - - -

# - - Set the data-frame rate to 20Hz - - - - - - - -
print( "Data-Frame rate: ", end= '')
if( tfmP.sendCommand( SET_FRAME_RATE, FRAME_10)):
    print( str(FRAME_10) + 'Hz')
else:
    tfmP.printReply()
# - - - - - - - - - - - - - - - - - - - - - - - -
time.sleep(0.5)     # Wait half a second.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - -  the main program loop begins here  - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
try:
    while True:
        time.sleep(0.1)   # Loop delay 50ms to match the 20Hz data frame rate
        # Use the 'getData' function to get data from device
        if( tfmP.getData()):
            print( f" Distance: {tfmP.dist:{3}}cm ", end= ' ')   # display distance,
            print( f"Signal strength: {tfmP.flux:{4}d} ",   end= ' ')   # display signal strength/quality,
            print( f"Temperature: {tfmP.temp:{2}}°C",  )   # display temperature,
        else:                  # If the command fails...
          tfmP.printFrame()    # display the error and HEX data
#
except KeyboardInterrupt:
    print( 'Keyboard Interrupt')
#    
except: # catch all other exceptions
    eType = sys.exc_info()[0]  # return exception type
    print( eType)
#
finally:
    sys.exit()                   # clean up the OS and exit
#
# - - - - - -  the main program sequence ends here  - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#https://github.com/budryerson/TFMini-Plus_python 참고