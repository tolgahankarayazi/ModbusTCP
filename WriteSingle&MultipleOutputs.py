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

    # if open() is ok, write coil or coils (modbus function 0x05 or 0x15)
    if c.is_open():
        # write "length" bits at address starting from "initial_addr"
        # Q0.0 to Q1023.7 --> data address: 1 to 8192
        # Q0.0 to Q0.7 --> data address: 1 to 8      Q1.0 data address: 9 
        # Qm.n --> data address: m * 8 + (n+1)
        m = 1
        n = 5
        if  m < 0 or n < 0:
            sys.stderr.write('Do not enter a negative number!\n')
            sys.stderr.flush()
            time.sleep(3)
            sys.exit()
        data = [True, False, True, False, True, True, False, False, True, False, True]
        for i in data:
            if i != True and i != False:
                sys.stderr.write('The data must consist of boolean values: True or False\n')
                time.sleep(1)
                print('This window is closing....')
                time.sleep(2)
                std.close()

        initial_addr = m * 8 + (n+1)
        coils = c.write_multiple_coils(initial_addr - 1, data) # 1 due to the offset
        print("Data has been written to addresses starting from " + "Q" + str(m) + "." + str(n))
        time.sleep(1)
        print('This window is closing....')
        time.sleep(5)
        std.close()
   