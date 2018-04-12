import serial
import time
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)		
GPIO.setup(3, GPIO.OUT)		
port1=serial.Serial("/dev/ttyUSB0",9600,timeout=3.0)
port=serial.Serial("/dev/ttyAMA0",9600,timeout=3.0)
#port2 = serial.Serial("/dev/tty1", 9600, timeout=3.0)
logvalfile=open('gpsvaluelog.txt','wb')
new=open('newgps.txt','wb')
logfile=open('gpslog.txt','wb')
port2 = serial.Serial("/dev/ttyAMA0", 9600, timeout=3.0)
port.flushInput()
port.flushOutput()
print"Smart Helmet"
count=0
accident=0
def call():
	print"GSM SIM900\n" 
	print"List of operating Commands" 
	print"Commands		functions" 
	print"AT	to check operations" 
	port.write('AT\r\n')		
	rcv = port.read(20) 
	print"GSM" + rcv
	while True: 
		rcv = port.read(20) 
		print rcv
		time.sleep(2) 
		keyin = "9560049824" 
		print keyin
		keyin2 = 'ATD '+keyin+';\r\n' 
		print"Dialing : " + keyin2 
		port.write(keyin2)
		x=1 
		for x in range(0,9): 
			rcv= port.read(50) 
			print rcv
			x+=1 
			
def message():
	
	rcvdfile=port.read(1200)
	pos1 = rcvdfile.find("$GPRMC")
	pos2 = rcvdfile.find("\n",pos1)
	loc = rcvdfile[pos1:pos2]
	logfile.write(rcvdfile)
	data = loc.split(',')
	print 'pppp'
	print data

	pos11 = rcvdfile.find("$GPGGA")
	pos22 = rcvdfile.find("\n",pos11)
	loc1 = rcvdfile[pos11:pos22]
	data1 = loc1.split(',')
	if data[2]=='V':
		print 'No location found'
	else:
		
		#print "UTC time="+data[1]+" UTC date=" + data[9]
		gps_time=float(data[1])
		gps_date=float(data[9])
		
		gps_hour=int(gps_time/10000.0)
		gps_min= gps_time%10000.0
		gps_sec=gps_min%100.0
		gps_min=int(gps_min/100.0)
		gps_sec=int(gps_sec)
		
		gps_dd=int(gps_date/10000.0)
		gps_mm= gps_date%10000.0
		gps_yy=gps_mm%100.0
		gps_mm=int(gps_mm/100.0)
		gps_yy=int(gps_yy)

		print 'time=',gps_hour,':',gps_min,':',gps_sec
		
		print 'date=',gps_dd,'/',gps_mm,'/',gps_yy
		
		print "Latitude = "+data[3]+data[4]
		print "Longitude = "+data[5]+data[6]
		latact=float(data[3])
		longact=float(data[5])
		
		print "Speed = "+data[7]
		print "Course = "+data[8]
		print "\n"

		gps_time_gga=float(data1[1])
		gps_hour_gga=int(gps_time_gga/10000.0)
		gps_min_gga= gps_time_gga%10000.0
		gps_sec_gga=gps_min_gga%100.0
		gps_min_gga=int(gps_min_gga/100.0)
		gps_sec_gga=int(gps_sec_gga)
		
		new.write(data[8])
		print 'time=',gps_hour_gga,':',gps_min_gga,':',gps_sec_gga
				
		print "Latitude = "+data1[2]+data1[3]
		print "Longitude = "+data1[4]+data1[5]
		print "Satellites used= "+data1[7]
		print "Altitude = "+data1[9]
		print "\n"
		
		logvalfile.write("\n"+'time='+str(gps_hour)+':'+str(gps_min)+':'+str(gps_sec)+"\n"+'date='+str(gps_dd)+'/'+str(gps_mm)+'/'+str(gps_yy)+"\n")
		logvalfile.write("\n"+"Latitude = "+data[3]+data[4]+"\n"
		+"Longitude = "+data[5]+data[6]+"\n"+"Speed = "+data[7]+"\n"
		+"Course = "+data[8]+"\n"+"Latitude = "+data1[2]+data1[3]+"\n"
		+ "Longitude = "+data1[4]+data1[5]+"\n"+ "Satellites used= "+data1[7]+"\n"
		+ "Altitude = "+data1[9])
	port.flushInput()
	port.flushOutput()		
	#os.system("gpsbabel -i NMEA -f gpslog.txt -o GPX -F gpslog.gpx")
	#os.system("gpsprune")

	
	print"Sending message"
	msgin="Latitude = "+data1[2]+data1[3]+"\nLongitude = "+data1[4]+data1[5]
	msgnum="8447733501"
	port.write('AT+CMGS="'+msgnum+'"\r\n')
	time.sleep(2)
	port.flushInput()
	port.flushOutput()
	port.write(msgin)
	time.sleep(2)
	port.write('\x1A\r\n')
	#print port.read(50)
	port.flushInput()
	port.flushOutput()
	print"Message send"			


while (count==0):
	time.sleep(5)
	rcv=port1.read(1)
	print"Recieved String:" + rcv
	a=str(rcv)
	print a
	#time.sleep(2)
	#bike=rcv
	#a="accident\n"
	if a=="1":
		GPIO.output(3, GPIO.HIGH)
		print"1"
	if a=="2":
		GPIO.output(3, GPIO.LOW)
		keyin="5"
		port1.write(keyin)
	if a=="3":
		count+=1
		print count
		GPIO.output(3, GPIO.LOW)
		accident=1
		print 'msg'	
		message()
		call()
	else:
		print "No Action"			
					