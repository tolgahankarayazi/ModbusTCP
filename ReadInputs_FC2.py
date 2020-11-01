#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyModbusTCP.client import ModbusClient
import time

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

    # if open() is ok, read inputs (modbus function 0x02)
    if c.is_open():
        # read "length" bits at address "initial_adr", store result in inputs list
        # I0.0 to I1023.7 --> data adress: 10001 to 18192
        # I0.0 to I0.7 --> data adress: 10001 to 10008      I1.0 data adress: 10009 
        # Im.n --> data adress: m * 8 + (n+10001)
        m = 2
        n = 0
        length = 10 # number of discrite inputs to be read  !!! MINIMUM = 1
        if length < 0 or m < 0 or n < 0:
            sys.stderr.write('Do not enter a negative number!\n')
            sys.stderr.flush()
            time.sleep(10)
            sys.exit()

        initial_adr = m * 8 + (n+10001)
        print("Input Coil " + str(initial_adr) + " corresponds to " + "I" + str(m) + "." + str(n)+ "\n")
        print("\n********************\n")
        inputs = c.read_discrete_inputs(initial_adr - 10001, length) # 10001 due to the offset
        
        # display coils
        addr = initial_adr
        counter = n
    for i in range(length):
        print("Input Coil {} --> {}\n".format(addr,inputs[i]))
        addr += 1
        counter += 1
        if counter == 8:
            print("\n********************\n")
            counter = 0
    
    # sleep t seconds before next polling
    t = 60
    time.sleep(t)