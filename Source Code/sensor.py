import math
import time
import sys
import argparse
from datetime import datetime
import os

from bluepy import sensortag
import bluepy

def main():


	#add parse arguement
	parser = argparse.ArgumentParser()
	parser.add_argument('host', action='store',help='MAC of BT device')
	parser.add_argument('-f', '--filepath', action='store',help='path/to/output_csv_file', default='./')
	#parser.add_argument('-n', action='store', dest='count', default=0, type=int, help="Number of times to loop data")
	parser.add_argument('-t',action='store',type=float, default=1.0, help='time between polling')
	parser.add_argument('-T','--temperature', action="store_true",default=False)
	parser.add_argument('-A','--accelerometer', action='store_true', default=False)
	parser.add_argument('-H','--humidity', action='store_true', default=False)
	parser.add_argument('-M','--magnetometer', action='store_true', default=False)
	parser.add_argument('-B','--barometer', action='store_true', default=False)
	parser.add_argument('-G','--gyroscope', action='store_true', default=False)
	#parser.add_argument('-K','--keypress', action='store_true', default=False)
	#parser.add_argument('-L','--light', action='store_true', default=False)
	parser.add_argument('--all', action='store_true', default=False)

	#parse arguments
	arg = parser.parse_args(sys.argv[1:])

	#connect to sensor tag
	print('Connecting to ' + arg.host)
	tag = sensortag.SensorTag(arg.host)

	print ('Connection Successful')

	# Enabling selected sensors

	if arg.temperature or arg.all:
		tag.IRtemperature.enable()
		print ('IRtemperature Sensor Enabled')
	if arg.humidity or arg.all:
		tag.humidity.enable()
		print ('Humidity Sensor Enabled')
	if arg.barometer or arg.all:
		tag.barometer.enable()
		print ('Barometer Sensor Enabled')
	if arg.accelerometer or arg.all:
		tag.accelerometer.enable()
		print ('Accelerometer Sensor Enabled')
	if arg.magnetometer or arg.all:
		tag.magnetometer.enable()
		print ('Magnetometer Sensor Enabled')
	if arg.gyroscope or arg.all:
		tag.gyroscope.enable()
		print ('Gyroscope Sensor Enabled')

	#if arg.keypress or arg.all:
    #    tag.keypress.enable()
    #    tag.setDelegate(sensortag.KeypressDelegate())
    #if arg.light and tag.lightmeter is None:
    #    print("Warning: no lightmeter on this device")
    #if (arg.light or arg.all) and tag.lightmeter is not None:
    #    tag.lightmeter.enable()



	#wait for sensor initialization
	time.sleep(1.0)
	n=datetime.now()

	print('Start Measuring...')

	#store pid
	pid_filename=arg.filepath+str(n.year)+'-'+str(n.month)+'-'+str(n.day)+'_raw_data.pid'
	pid_file=open(pid_filename, 'w')
	pid_file.write(str(os.getpid()))
	pid_file.close()



	#create new csv file
	filename=arg.filepath+str(n.year)+'-'+str(n.month)+'-'+str(n.day)+'_raw_data.csv'
	file=open(filename, 'w')

	#write csv headers
	file.write('Time,')
	file.write('Ambient Temperature (degC),')
	file.write('Object Temperature (degC),')
	file.write('Humidity (RH),')
	file.write('Barometer (millibars),')
	file.write('Accelerometer-x (g),')
	file.write('Accelerometer-y (g),')
	file.write('Accelerometer-z (g),')
	file.write('Magnetometer-x (uT),')
	file.write('Magnetometer-y (uT),')
	file.write('Magnetometer-z (uT),')
	file.write('Gyroscope-x (deg/sec),')
	file.write('Gyroscope-y (deg/sec),')
	file.write('Gyroscope-z (deg/sec)\n')


	while True:
		file.write(str(datetime.now())+',')
		if arg.temperature or arg.all:
			file.write(str(tag.IRtemperature.read()[0])+',')
			file.write(str(tag.IRtemperature.read()[1])+',')

		if arg.humidity or arg.all:
			file.write(str(tag.humidity.read()[1])+',')
		if arg.barometer or arg.all:
			file.write(str(tag.barometer.read()[1])+',')
		if arg.accelerometer or arg.all:
			file.write(str(tag.accelerometer.read()[0])+',')
			file.write(str(tag.accelerometer.read()[1])+',')
			file.write(str(tag.accelerometer.read()[2])+',')
		if arg.magnetometer or arg.all:
			file.write(str(tag.magnetometer.read()[0])+',')
			file.write(str(tag.magnetometer.read()[1])+',')
			file.write(str(tag.magnetometer.read()[2])+',')
		if arg.gyroscope or arg.all:
			file.write(str(tag.gyroscope.read()[0])+',')
			file.write(str(tag.gyroscope.read()[1])+',')
			file.write(str(tag.gyroscope.read()[2])+'\n')

		file.flush()
		tag.waitForNotifications(arg.t)
	file.close()
	tag.disconnect()
	




if __name__ == '__main__':
	main()


    













