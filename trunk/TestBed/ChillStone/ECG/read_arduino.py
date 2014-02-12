import serial

ser = serial.Serial()
ser.port="/dev/tty.usbmodem1421"

#ser.port = "/dev/ttyACM0" # may be called something different

ser.baudrate =300  # may be different
ser.open()
if ser.isOpen():
    while True:
        # ser.inWaiting()
        response = ser.readline()
        #print response
        v=int(response)
        print v
        
        
        
        