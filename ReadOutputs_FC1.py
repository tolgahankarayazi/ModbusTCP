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

    # if open() is ok, read coils (modbus function 0x01)
    if c.is_open():
        # read "length" bits at address "initial_addr", store result in coils list
        # Q0.0 to Q1023.7 --> data address: 1 to 8192
        # Q0.0 to Q0.7 --> data address: 1 to 8      Q1.0 data address: 9 
        # Qm.n --> data address: m * 8 + (n+1)
        m = 1
        n = 1
        length = 3 # number of coils to be read  !!! MINIMUM = 1
        if length < 0 or m < 0 or n < 0:
            sys.stderr.write('Do not enter a negative number!\n')
            sys.stderr.flush()
            time.sleep(3)
            sys.exit()

        initial_addr = m * 8 + (n+1)
        print("Output Coil " + str(initial_addr) + " corresponds to " + "Q" + str(m) + "." + str(n)+ "\n")
        print("\n********************\n")
        
        coils = c.read_coils(initial_addr - 1, length) # 1 due to the offset
        
        # display coils
        addr = initial_addr
        counter = n
    for i in range(length):
        print("Output Coil {} --> {}\n".format(addr,coils[i]))
        addr += 1
        counter += 1
        if counter == 8:
            print("\n********************\n")
            counter = 0

    # sleep t seconds before next polling
    t = 60
    time.sleep(t)