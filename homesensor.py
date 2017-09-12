import pymssql
import Adafruit_DHT as dht
import time
import serial, struct

# MSSQL
conn = pymssql.connect(server='vt2eq6avx8.database.windows.net',user='landlady@vt2eq6avx8',password='anfdpQkwlstkfka1',database='HomeInfo')
cursor = conn.cursor()

# Serial Communication for PM 1001 dust sensor
port = serial.Serial(port = "/dev/ttyAMA0",baudrate=9600,timeout=10)
#port.open() not used. already port opend.
#send = [hex(0x11),hex(0x01),hex(0x01),hex(0xED)]
send = "\x11\x01\x01\xED"

while True:
		# Temp, Humidity value Check
        #humidity , temperature = dht.read_retry(dht.DHT11,4)
        #print 'Temp = {0:0.1f}*C Humidity = {1:0.1f}%'.format(temperature,humidity)
        
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
        #now = time.localtime()
        #nowTime = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday) + " " + str(now.tm_hour) + ":" + str(now.tm_min) + ":" + str(now.tm_sec)
        #print(nowTime)
        
        # Insert to MSSQL Database.
        #result = cursor.callproc("P_CREATE_CHECKINFO",("Home",humidity,temperature,nowTime,0))
        #print(str(result[0]) + "/" + str(result[1]) + "/" + str(result[2]))
        #conn.commit()
        
        #time.sleep(300)           # turn around 5 min.
        time.sleep(1)               # turn around 1 sec.
