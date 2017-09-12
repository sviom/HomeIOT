import serial, struct

# Serial Communication for PM 1001 dust sensor
port = serial.Serial(port = "/dev/ttyAMA0",baudrate=9600,timeout=10)
#port.open() not used. already port opend.
#send = [hex(0x11),hex(0x01),hex(0x01),hex(0xED)]
send = "\x11\x01\x01\xED"

while True:
        # Send to Sensor, Start Data
        res = port.write(send)
        print("Send value length : " + str(res))
                
        # Recieve from Sensor, Dust Data
        readResult = port.read(7)
        dustValue = 0	# Dust Data
        print("Return value " + str(readResult.encode('hex')))
        print(readResult[0].encode('hex'))
        print(struct.unpack('!f',readResult[3].encode('hex').decode('hex'))[0])
        # If ACK Value is 0x16, It is correct Data.
        if(readResult[0].encode('hex') == '16'):
        	pass
        	# Value check calculus is in PDF document.
        	#print(struct.unpack('!f',bytes.fromhex(readResult[3])))
        	#dustValue = (float(readResult[3].encode('hex'),16) * 256 * 256 * 256) + (float(readResult[4].encode('hex'),16) * 256*256) + (float(readResult[5].encode('hex'),16) * 256) + float(readResult[6].encode('hex'),16)
    	else:
    		print("non value")
    		
		print("dust value : " + str((dustValue*3.528)/100000))

        time.sleep(1)               # turn around 1 sec.
