#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyModbusTCP.client import ModbusClient
import time
import sys

SERVER_HOST = "192.168.0.1"
SERVER_PORT = 502 
SERVER_U_ID = 1 # Modbus Slave ID

c = ModbusClient()
# uncomment this line to see debug message
# c.debug(True)
# define modbus server host, port and unit_id
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(SERVER_U_ID)

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

    # if open() is ok, read holding registers (modbus function 0x10)
    if c.is_open():
        # for Siemens s7 1200 or 1500 PLC series create a holding register database that consist of array of word(or smt else) and connect it to the MB_Server_DB 
        # this code writes a specified value to the holding_reg_database.data[r]
        # for different PLCs think as same logic; use the holding regs database attended into the Modbus Server Function block of your main code block
        r = 0 # register number must be a non-negative number!n
        if  r < 0:
            sys.stderr.write('Enter a positive register number!\n')
            sys.stderr.flush()
            time.sleep(3)
            sys.exit()

        nbr_of_regs = 13 # number of registers to be written  !!! MINIMUM = 1
        if nbr_of_regs < 1:
            sys.stderr.write('The number of registers to be read can not be a negative number!\n')
            sys.stderr.flush()
            time.sleep(3)
            sys.exit()
        
        initial_addr = r + 40001
        data = [1881,18,3,1915,19,5,1919,23,4,1920,29,10,1923]
        if len(data) != nbr_of_regs:
            sys.stderr.write('There are not ' + str(nbr_of_regs) + ' elements in the data list.')
            sys.stderr.flush()
            time.sleep(1)
            print('\nThis window is closing....')
            time.sleep(2)
            sys.exit()
        holding_regs = c.write_multiple_registers(initial_addr - 40001, data) # 40001 due to the offset

        if holding_regs != True:
            print("An error occurred, hasn't been written!")
        else:
            print('Writing process finished succesfully.')
        time.sleep(1)
        print('This window is closing....')
        time.sleep(10)
        std.close()
