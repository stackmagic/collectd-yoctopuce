#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2014 Patrick Huber <stackmagic@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# mosquitto QOS levels:
# - 0: The broker/client will deliver the message once, with no confirmation.
# - 1: The broker/client will deliver the message at least once, with confirmation required.
# - 2: The broker/client will deliver the message exactly once by using a four step handshake.
#

# pip install RPi.GPIO
# pip install paho-mqtt

import paho.mqtt.client as paho
import time
import yoctodump

host     = 'localhost'
port     = 1883
clientId = 'mqtt_yoctopuce'

client = paho.Client(client_id = clientId, protocol = paho.MQTTv31)
client.connect(host, port)
client.loop_start()

data = yoctodump.GetMeasurements()

for moduleData in data.values():

    modName = moduleData['logicalName']

    if modName == '':
        modName = moduleData['serialNumber'].replace('-', '_')

    for sensor in moduleData['sensors'].values():

        senName = sensor['functionId']
        senVal  = sensor['advertisedValue']
        topic = 'yoctopuce/%s/%s' % (modName, senName)

        (result, mid) = client.publish(topic, senVal)
        print '>>> %s = %s' % (topic, senVal)

# need to sleep so messages get through
# all attempts at using on_publish and recording
# whats pending and whats been sent have failed
time.sleep(0.1)

# done
client.disconnect()


