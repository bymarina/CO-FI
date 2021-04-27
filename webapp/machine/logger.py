#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
from syscall import syscall

exceptions_log_file = "CO_FI_error_logs.txt"
log_file = "state.log"


def exception_logger(code, function, line_number, exc):
    '''
    Realiza log em arquivo externo no local ../CO_FI_error_logs.txt. Auxiliar de debug
    '''
    global v_macEth0
    exc = str(exc).replace(')', '\)').replace('(', '\(').replace('>', '\>').replace('<', '\<').replace(';', '\;').replace(
        '"', '\\"').replace("'", "\\'")
    time = datetime.now().strftime("%H:%M:%S")
    mes_dia_ano = datetime.now().strftime("%b %d %Y")
    command = "echo {0} {1} {2} {3} line:{4}: {5} >> /home/pi/GIT/CO-FI/{6}".format(mes_dia_ano, time, code,
                                                                                       function, line_number, exc,
                                                                                       exceptions_log_file)
    syscall(command)


def log_and_print(message):
    print(message)
    command = "echo {0} {1} >> /home/pi/GIT/CO-FI/{2}".format(datetime.now().strftime("%H:%M:%S"), message, log_file)
    syscall(command)
