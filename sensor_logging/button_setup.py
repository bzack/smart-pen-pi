#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sensor_setup
import RPi.GPIO   as GPIO

# print('Button File Imported')
BtnPin = 11
Gpin   = 12
Rpin   = 13
queue  = None

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
	GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)

def quick_sensor_print():
    arr = queue.get()
    print('    Temperature: {}°F, Light: {}'.format(arr[0], arr[1]))
    print

def Led(x):
	if x == 0:
		GPIO.output(Rpin, 1)
		GPIO.output(Gpin, 0)
	if x == 1:
		GPIO.output(Rpin, 0)
		GPIO.output(Gpin, 1)

def Print(x):
	if x == 0:
		print '    ***********************'
		print '    *   Button Pressed!   *'
		print '    ***********************'
                quick_sensor_print()

def detect(chn):
	Led(GPIO.input(BtnPin))
	Print(GPIO.input(BtnPin))

def loop():
	while True:
		pass

def destroy():
	GPIO.output(Gpin, GPIO.HIGH)       # Green led off
	GPIO.output(Rpin, GPIO.HIGH)       # Red led off
	GPIO.cleanup()                     # Release resource

def button_main(shared_queue):
	try:
            global queue
            queue = shared_queue
            setup()
            loop()
	except KeyboardInterrupt:  
        # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            destroy()
            os._exit(2)
