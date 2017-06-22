#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Program that runs all the sensors and prints out diagnostic information 
# every two seconds.
import RPi.GPIO as GPIO
import PCF8591 as ADC
import smbus
import time

# Read information from the temperature file.
temperature_filename = '/sys/bus/w1/devices/28-03167489f3ff/w1_slave'
temperature          = None

# Set the time delay between print statements in seconds.
time_delay = 2

# Function to convert from celcius to temperature.
def Celcius_To_Fahreinheit(temperature):
    return 9.0/5.0 * (temperature/1000) + 32

# Setting up the light sensor.
def light_sensor_setup():
    DO = 17
    light_sensor_address = 0x48
    GPIO.setmode(GPIO.BCM)

    ADC.setup(light_sensor_address)
    GPIO.setup(DO, GPIO.IN)

# Read temperature from file and print it out.
def print_temperature():
    with open(temperature_filename) as f:
        f.readline()
        temperature_line = f.readline()
        temp_index       = temperature_line.find('=') + 1
        value_str        = temperature_line[temp_index:]
        # print('value_str', value_str)
        # print('temp_index', temp_index)
        # print('temperature_line', temperature_line)

        temperature      = int(value_str)
        temperature      = Celcius_To_Fahreinheit(temperature)
        print('Temperature {}°F'.format(temperature))

def print_info():
    light_value = ADC.read(0)
    print_temperature()
    print('Light Value: {}'.format(light_value))
    print
    time.sleep(time_delay)

# Prints out the light and temperature values
def loop():
    status = 1
    while True:
        print_info()

if __name__ == '__main__':
    # button.main()
    try:
        light_sensor_setup()
        loop()
    except KeyboardInterrupt:
        pass

