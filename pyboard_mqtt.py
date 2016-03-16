# -*- coding: utf-8 -*-
#===========================================================
# Send data to MQTT by DTU
#
# Designed by Aixi Wang  (aixi.wang@hotmail.com)
#===========================================================
import pyb
from pyb import UART
from pyb import LED

import time,sys
import os
import json
import binascii

led = LED(1)
#------------------------------
# uart_open
#------------------------------    
def uart_open(uart_port,uart_baud):
    #print 'uart_port:',uart_port,' uart_baud:',uart_baud
    ser = UART(uart_port, uart_baud)
    return ser

#------------------------------
# uart_read
#------------------------------
def uart_read():
    c = s.read()
    return c

#------------------------------
# uart_write
#------------------------------    
def uart_write(s,c):
    s.write(c)
    
#------------------------------
# uart_has
#------------------------------ 
def uart_has(s):
    return s.any()

#------------------------
# debug_print
#------------------------
def debug_print(s):
    f = open('debug.txt','ab+')
    f.write(s + '\r\n')
    f.flush()
    print(s)
    
#------------------------------
# mqtt_pyboard
#------------------------------  
class pyboard_mqtt:
    def __init__(self,ser):
        self.ser = ser

    #------------------------------
    # pkg_str
    #------------------------------    
    def pkg_str(self,s):
        return bytes([len(s) >> 8, len(s) & 255]) + s
        
    #------------------------------
    # pkg_cmd
    #------------------------------  
    def pkg_cmd(self,cmd,variable,payload):
        len_2 = len(variable) + len(payload)
        return cmd + bytes([len_2]) + variable + payload
            
    #------------------------------
    # pkg_connect
    #------------------------------  
    def pkg_connect(self,name):
        return self.pkg_cmd(
               b'\x10',
               self.pkg_str(b'MQIsdp') + # protocol name
               b'\x03' +       # protocol level
               b'\x00' +       # connect flag
               b'\xff\xff',    # keepalive, TODO
               self.pkg_str(name)
      )

    #------------------------------
    # pkg_disconnect
    #------------------------------   
    def pkg_disconnect(self):
        return b'\xe0\x00'

    #------------------------------
    # pkg_pub
    #------------------------------ 
    def pkg_pub(self,topic,data):
        return  self.pkg_cmd(b'\x31', self.pkg_str(topic), data)

    #------------------------------
    # pub
    #------------------------------ 
    def pub(self,name,topic,data):
        self.ser.write(self.pkg_connect(name))
        time.sleep(1)
        in_s = self.ser.read(1024)
        
        if in_s == b'\x20\x02\x00\x00':
            debug_print('connect ok')
        else:
            debug_print('connect failed')
        
        self.ser.write(self.pkg_pub(topic, data))
        time.sleep(1)
        in_s = self.ser.read(1024)

#----------------------
# pyboard_mqtt_test
#----------------------
def pyboard_mqtt_test():
    led.on()
    ser = uart_open(4, 9600)
    #ser.init(9600, bits=8, parity=None, stop=1,timeout=10)
    m = pyboard_mqtt(ser)

    id = pyb.unique_id()
    id_s = binascii.hexlify(id)
    debug_print('id:' + id_s.decode())   
    
    while True:
        m.pub(id_s, id_s + b'/C2D/',b'test mqtt pub string')      
        time.sleep(5)
      
#----------------------
# main
#----------------------
if __name__ == "__main__":
    pyboard_mqtt_test()
    
