#---------------------------------------------------------------------------------------
# data_viewer
#
# BSD 3-clause license is applied to this code
# Copyright(c) 2015 by Aixi Wang <aixi.wang@hotmail.com>
#----------------------------------------------------------------------------------------
#!/usr/bin/python

import socket
import threading               # Import socket module
import time
import os,sys

import mqtt.publish as publish
import mqtt.client as mqtt

#-------------------
# global variable
#-------------------

#-------------------
# global setting
#-------------------

#MQTT_SERVER = 'test.mosquitto.org'
MQTT_SERVER = '115.29.178.81'
MQTT_PORT = 1883



#----------------------
# mqtt my_mqtt_mainloop
#----------------------
def my_mqtt_mainloop(mqttc):
    mqttc.loop_forever()
    
#----------------------
# mqtt on_message
#----------------------
def on_message(mosq, obj, msg):
    global TCP_ID_PAIR
    print("MESSAGE: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    
    
#----------------------
# main
#----------------------
if __name__ == "__main__":
    print 'step 1. create mqtt'
    mqttc = mqtt.Client()

    # Add message callbacks that will only trigger on a specific subscription match.
    mqttc.on_message = on_message
    mqttc.connect(MQTT_SERVER, MQTT_PORT, 60)
    mqttc.subscribe('400037001647333138333632/#',0)

    print 'step 2. create mqtt mainloop'
    threading.Thread(target=my_mqtt_mainloop, args=(mqttc,)).start()
    
