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

    # if open() is ok, read input registers (modbus function 0x04)
    if c.is_open():
        # read "nmbr_of_regs" registers from address started with "initial_addr", store result in input_regs list
        # IW0 to IW1022 --> data adress: 30001 to 30512
        # IW0 --> data address: 30001           IW2 --> data adress: 30003        IW1 --> data adress: 30002        
        # IWr --> data adress: r + 30001
        r = 20 # register number must be a non - negative number!
        if r % 2 != 0 or r < 0:
            sys.stderr.write('Enter an even register number!\n')
            sys.stderr.flush()
            time.sleep(1)
            print('This window is closing....')
            time.sleep(2)
            sys.exit()
        nbr_of_regs = 15 # number of registers to be read  !!! MINIMUM = 1
        if nbr_of_regs < 0:
            sys.stderr.write('The number of registers to be read can not be a negative number!\n')
            sys.stderr.flush()
            time.sleep(1)
            print('This window is closing....')
            time.sleep(2)
            sys.exit()

        initial_addr = r + 30001
        input_regs = c.read_input_registers(int(initial_addr - 30001 - (r/2)), nbr_of_regs) # 1 due to the offset

        #display input registers
        addr = initial_addr
        for i in range(nbr_of_regs):
            print("Input register {} (IW{}) --> {}\n".format(addr, addr - 30001, input_regs[i]))
            addr += 2
  
    # sleep t seconds before next polling
    t = 60
    time.sleep(t)