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

    # if open() is ok, read holding registers (modbus function 0x03)
    if c.is_open():
        # read "nmbr_of_regs" registers from addresses started with "initial_addr", store result in holding_regs list
        # for Siemens s7 1200 or 1500 PLC series create a holding register database that consist of array of word(or smt else) and connect it to the MB_Server_DB 
        # this code queries the value of the holding_reg_database.data[r]
        # for different PLCs think as same logic; use the holding regs database attended into the Modbus Server Function block of your main code block
        r = 0 # register number must be a non - negative number!
        if  r < 0:
            sys.stderr.write('Enter a positive register number!\n')
            sys.stderr.flush()
            time.sleep(3)
            sys.exit()
        nbr_of_regs = 13 # number of registers to be read  !!! MINIMUM = 1
        if nbr_of_regs < 1:
            sys.stderr.write('The number of registers to be read can not be a negative number!\n')
            sys.stderr.flush()
            time.sleep(3)
            sys.exit()
        
        initial_addr = r + 40001
        holding_regs = c.read_holding_registers(initial_addr - 40001, nbr_of_regs) # 40001 due to the offset
        #display input registers
        addr = r
        for i in range(nbr_of_regs):
            print("holding_regs.data[{}] = {}\n".format(r,holding_regs[i]))
            r += 1
    # sleep t seconds before next polling
    t = 60
    time.sleep(t)
