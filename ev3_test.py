import time
import ev3
from ev3.rawdevice import motordevice
from ev3.sensor.lego import EV3IRSensor
#from ev3.sensor.lego import EV3ColorSensor
from argparse import ArgumentParser

ev3.open_all_devices()

motordevice.open_device()
A = 0x01
B = 0x02
C = 0x04
D = 0x08

right = A
left = D
both = A+D

#SPEED = 50
MAX_VALUE=255



# def color_sensor_test():
# 	print "color_sensor_test"
# 	color_sensor = EV3ColorSensor(ev3.SENSOR_2)
# 	color_sensor.set_color_mode()
# 	while 1:
# 		print color_sensor.get_value()

def ir_test():
	print "ir_control test mode"
	ir_sensor = EV3IRSensor(ev3.SENSOR_2)
	print "setting remote control mode"
	ir_sensor.set_remote_control_mode()
	while True:
	    ir_sensor_command = ir_sensor.get_remote_control_command(channel=1)
	    print ir_sensor_command
	    time.sleep(.1)

def ir_control(speed):
	remote_control_map = {
		0: {'label': 'off', 'motor': both, 'value': 0},
		1: {'label': 'left_up', 'motor': D, 'value': speed},
		2: {'label': 'left_down', 'motor': D, 'value': MAX_VALUE-speed},
		3: {'label': 'right_up', 'motor': A, 'value': speed},
		4: {'label': 'right_down', 'motor': A, 'value': MAX_VALUE-speed},
		5: {'label': 'both_up', 'motor': both, 'value': speed},
		6: {'label': 'left_up_right_down', 'motor': both, 'value': 0},
		7: {'label': 'left_down_right_up', 'motor': both, 'value': 0},
		8: {'label': 'both_down', 'motor': both, 'value': MAX_VALUE-speed},
		9: {'label': 'top', 'motor': both, 'value': 0},
		10:{'label': 'both_left', 'motor': both, 'value': 0},
		11:{'label': 'both_right', 'motor': both, 'value': 0}
	}
	print "ir_control mode"
	ir_sensor = EV3IRSensor(ev3.SENSOR_2)
	print "setting remote control mode"
	ir_sensor.set_remote_control_mode()
	#motordevice.stop(both,brake=0)    	
	while True:
	    ir_sensor_command = ir_sensor.get_remote_control_command(channel=1)
	    ir_sensor_command_dict = remote_control_map.get(ir_sensor_command)
	    if ir_sensor_command == 6:
	    	motordevice.speed(D, speed)
	    	motordevice.speed(A,MAX_VALUE-speed)
	    elif ir_sensor_command == 7:
	    	motordevice.speed(D, MAX_VALUE-speed)
	    	motordevice.speed(A,speed)
	    elif ir_sensor_command != 0:
	        print "command: {0} - {1}".format(
	        	ir_sensor_command,
	        	ir_sensor_command_dict.get('label')
	        )
	        motordevice.speed(
	        	ir_sensor_command_dict.get('motor'),
	    		ir_sensor_command_dict.get('value')
	        )
	    else:
	    	motordevice.speed(both,0)
			#motordevice.stop(both,brake=1)    	
	    time.sleep(.1)

def main():

	parser = ArgumentParser()
	parser.add_argument(
		'--speed', 
		help='motor speed (max value 100)', 
		type=int, 
		default=30)
	options = parser.parse_args()
	speed = options.speed
	#color_sensor_test()
	ir_control(speed)
	#ir_test()

main()

