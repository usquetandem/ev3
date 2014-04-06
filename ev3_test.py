# if failure, try  /etc/init.d/lms2012-driver.sh


import time
import ev3
from ev3.rawdevice import motordevice
from ev3.sensor.lego import EV3IRSensor
from ev3.sensor.lego import EV3ColorSensor
from ev3.sensor.lego import EV3TouchSensor
from argparse import ArgumentParser
from ev3.rawdevice import uartdevice
from ev3.rawdevice import sound

ev3.open_all_devices()

motordevice.open_device()
A = 0x01
B = 0x02
C = 0x04
D = 0x08

right = A
left = D
both = A+D

DEFAULT_SPEED = 50
MAX_VALUE=255

BEAT = .25
snowman = [
	(329,BEAT*1000,BEAT),(329,BEAT*1000,BEAT),(329,BEAT*1000,BEAT),(246,BEAT*1000,BEAT),
	(329,BEAT*1000,BEAT),(415,2*BEAT*1000,2*BEAT),(370,2*BEAT*1000,2*BEAT),
	(415,2*BEAT*1000,2*BEAT),
	(329,BEAT*1000,BEAT),(329,BEAT*1000,BEAT),(329,BEAT*1000,BEAT),
	(246,BEAT*1000,BEAT),(329,BEAT*1000,BEAT),(415,BEAT*1000,BEAT),
	(370,3*BEAT*1000,BEAT)
]

DEFAULT_MODE = 'ir_control'

def sound_test(volume=100):
	print "sound_test"
	sound.open_device()
	print "playing tone"
	for frequency, duration, sleep in snowman:
		print frequency, duration, sleep
		sound.play_tone(frequency, int(round(duration)), volume)
		time.sleep(sleep)
	print "closing sound device"
	sound.close_device

def touch_sensor_test():
	print "touch_sensor_test"
	touch_sensor = EV3TouchSensor(ev3.SENSOR_4)
	print "begin acquisition"
	while True:
		print touch_sensor.is_pressed()


def color_sensor_color_test_raw():
	print "color_sensor_color_test_raw"
	uartdevice.open_device()
	color_sensor = EV3ColorSensor(ev3.SENSOR_3)
	print "setting color mode"
	color_sensor.set_color_mode()
	color_sensor.set_ref_raw_mode()
	print "begin acquisition"
	while True:
		print color_sensor.get_value()

def color_sensor_color_test():
	print "color_sensor_color_test"
	color_sensor = EV3ColorSensor(ev3.SENSOR_3)
	print "setting color mode"
	color_sensor.set_color_mode()
	color_sensor.color_to_string()
	#color_sensor.set_ref_raw_mode()
	print "begin acquisition"
	while True:
		print color_sensor.color_to_string(), color_sensor.get_value()

def color_sensor_reflect_test():
	print "color_sensor_reflect_test"
	color_sensor = EV3ColorSensor(ev3.SENSOR_3)
	print "setting reflect mode"
	color_sensor.set_reflect_mode()
	#color.set_ref_raw_mode()
	print "begin acquisition"
	while True:
		print color_sensor.get_value()

def color_sensor_ambient_test():
	print "color_sensor_ambient_test"
	color_sensor = EV3ColorSensor(ev3.SENSOR_3)
	print "setting ambient mode"
	color_sensor.set_ambient_mode()
	#color.set_ref_raw_mode()
	print "begin acquisition"
	while True:
		print color_sensor.get_value()


def ir_test():
	print "ir_control test mode"
	ir_sensor = EV3IRSensor(ev3.SENSOR_2)
	print "setting remote control mode"
	ir_sensor.set_remote_control_mode()
	print "begin acquisition"
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
	print "begin acquisition"
	while True:
	    ir_sensor_command = ir_sensor.get_remote_control_command(channel=1)
	    ir_sensor_command_dict = remote_control_map.get(ir_sensor_command)

	    # modes 6 and 7 have different directions and speeds for motors,
	    # need to differently handle
	    if ir_sensor_command == 6:
	    	motordevice.speed(D, speed)
	    	motordevice.speed(A,MAX_VALUE-speed)
	    elif ir_sensor_command == 7:
	    	motordevice.speed(D, MAX_VALUE-speed)
	    	motordevice.speed(A,speed)
	    elif ir_sensor_command == 9:
	    	sound_test(100)
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
		help='motor speed (default {0}, max 100)'.format(DEFAULT_SPEED), 
		type=int, 
		default=DEFAULT_SPEED)
	parser.add_argument(
		'--mode',
		help='control mode (default ir_control, others color_sensor_test, ir_test',
		type=str,
		default=DEFAULT_MODE	
	)
	options = parser.parse_args()
	speed = options.speed
	mode = options.mode
	if mode == 'ir_control':
		ir_control(speed)
	elif mode == 'touch_sensor_test':
		touch_sensor_test()
	elif mode == 'color_sensor_reflect_test':	
		color_sensor_reflect_test()
	elif mode == 'color_sensor_ambient_test':	
		color_sensor_ambient_test()	
	elif mode == 'ir_test':
		ir_test()
	elif mode == 'color_sensor_color_test_raw':
		color_sensor_color_test_raw()
	elif mode == 'color_sensor_color_test':
		color_sensor_color_test()
	elif mode == 'sound_test':
		sound_test(100)
	else:
		print "Invalid mode '{0}', try again.".format(mode)

main()

