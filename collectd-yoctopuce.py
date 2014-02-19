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
# this script is a collectd plugin and uses the yoctodump.py script to read
# measurements from all your yoctopuce and feed them into collectd. you can
# connect or unplug yoctopuce devices at any time and they will be removed or
# added automatically
#

#
# TODO for now this must be called via the Exec plugin. It would be nice to use
# the Python plugin.
#
# TODO find out how this plain text protocol works, how to make the graphs
# have pretty names and have a unit description along the y-axis.
#

import os
import yoctodump

host = os.getenv('COLLECTD_HOSTNAME', 'localhost')
ival = os.getenv('COLLECTD_INTERVAL', '60')
data = yoctodump.GetMeasurements()

for moduleData in data.values():

	modName = moduleData['logicalName']
	if modName == '':
		modName = moduleData['serialNumber']

	for sensor in moduleData['sensors'].values():

		senName = sensor['functionId']
		senVal  = sensor['advertisedValue']
		print 'PUTVAL %s/yoctopuce-%s/gauge-%s interval=%s N:%s' % (host, modName, senName, ival, senVal)

