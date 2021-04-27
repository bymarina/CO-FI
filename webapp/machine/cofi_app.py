#!/usr/bin/python3
# -*- coding: utf-8 -*-

from inspect import getframeinfo, currentframe
from webapp.machine.logger import exception_logger, log_and_print
from webapp.machine.piGPIO import piGPIO
from webapp.machine.stateMachineFunctions import state_functions
import smbus
import time

def coffee(send, receive):
    log_and_print("")
    log_and_print("Starting CO-FI...")    
    pi_gpio = piGPIO()
    pi_gpio.gpio_config()
    functions = state_functions()

    while True:
        order = receive.get()
        user = order['user']
        print("Received order")
        
        functions.get_measures(order['chocolate'], order['coffee'], order['milk'])  
        ingredients_ok = functions.verify_ingredients()    
        if not ingredients_ok:
            functions.request_reposition()
            result = {'user':user, 'status': False}
            send.put(result)
        elif ingredients_ok:
            result = {'user':user, 'status': True}
            send.put(result)
            functions.separate_ingredients()
            functions.heat()
            functions.add_water()
            functions.mix()
            functions.wait_for_mug()
            functions.release_drink()

    log_and_print("Turning CO-FI off.")

    
try:
    main()
except Exception as exc:
    log_and_print("Exception: {0}".format(exc))
    exception_logger("cofi_app.py", "main", getframeinfo(currentframe()).lineno, exc)