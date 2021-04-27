#!/usr/bin/python3
# -*- coding: utf-8 -*-

from webapp.machine.piGPIO import piGPIO
from webapp.machine.logger import log_and_print
import time

class state_functions(object):

    pi_gpio = piGPIO()
    measure0 = 0
    measure1 = 0
    measure2 = 0

    def get_measures(self, measure0, measure1, measure2):

        self.measure0 = measure0
        self.measure1 = measure1
        self.measure2 = measure2        

    def verify_ingredients(self):
        
        water_result = pi_gpio.ultrasonic_sensor_distance_control()
        return water_result

    def request_reposition(self):

       log_and_print("Water level is low, reposition required ")

    def separate_ingredients(self):
        
        if measure0 > 0:
            pi_gpio.servo0_control(measure0)
            time.sleep(1)
            self.measure0 = 0
        if measure1 > 0:
            pi_gpio.servo1_control(measure1)
            time.sleep(1)
            self.measure1 = 0
        if measure2 > 0:
            pi_gpio.servo2_control(measure2)
            time.sleep(1)
            self.measure2 = 0
    
    def heat(self):
        
        pi_gpio.heater_control()
        time.sleep(1)

    def add_water(self):
        
        pi_gpio.water_pump0_control()
        time.sleep(1)

    def mix(self):
        
        pi.gpio.mixer_control()
        time.sleep(1)

    def wait_for_mug(self):
        
        mug_result = pi.gpio.light_sensor_control()
        while True:
            if mug_result == 1:
                log_and_print("Your drink will be released ")
                break
            elif mug_result == 0:
                log_and_print("Please, position your mug ")
                time.sleep(3)

    def release_drink(self):
        
        pi_gpio.water_pump1_control()
        time.sleep(1)
