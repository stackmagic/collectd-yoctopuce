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
# this script enumerates all yoctopuce modules, reads their measurement values
# and returns them in a map/list structure when called from another script or
# dumps the same information as formatted json to stdout if called from a cli.
#

#
# NOTE: this script only supports the humidity/pressure/temperature, that's
# what the yoctopuce-meteo module sports - my attempts to find the other
# sensor's functionId's. If you have other modules, please find out the
# functionId's and extend the script so it supports more yoctopuce sensors.
#

import sys
import json

isMain = __name__ == '__main__'

from yoctopuce.yocto_api import *

def __walk_module(module):
	result = {}

	result['beacon']          = module.get_beacon()
	result['errorMessage']    = module.get_errorMessage()
	result['description']     = module.describe()
	result['firmwareRelease'] = module.get_firmwareRelease()
	result['hardwareId']      = module.get_hardwareId()
	result['logicalName']     = module.get_logicalName()
	result['luminosity']      = module.get_luminosity()
	result['productId']       = module.get_productId()
	result['productName']     = module.get_productName()
	result['productRelease']  = module.get_productRelease()
	result['rebootCountdown'] = module.get_rebootCountdown()
	result['serialNumber']    = module.get_serialNumber()
	result['upTime']          = module.get_upTime()
	result['usbCurrent']      = module.get_usbCurrent()
	result['userData']        = module.get_userData()
	result['sensors']         = {}

	return result

def __walk_sensor(sensor):
	result = {}
	result['advertisedValue'] = sensor.get_advertisedValue()
	result['currentRawValue'] = sensor.get_currentRawValue()
	result['currentValue']    = sensor.get_currentValue()
	result['description']     = sensor.describe()
	result['errorMessage']    = sensor.get_errorMessage()
	result['friendlyName']    = sensor.get_friendlyName()
	result['functionId']      = sensor.get_functionId()
	result['hardwareId']      = sensor.get_hardwareId()
	result['highestValue']    = sensor.get_highestValue()
	result['logicalName']     = sensor.get_logicalName()
	result['lowestValue']     = sensor.get_lowestValue()
	result['resolution']      = sensor.get_resolution()
	result['unit']            = sensor.get_unit()
	result['userData']        = sensor.get_userData()

	return result

def __walk_sensors():
	"""Enumerate all sensors but store them in a hierarchical structure where
	the module is the parent for the sensor and measurement information."""
	result = {}

	sensor = YSensor.FirstSensor()
	while sensor != None:
		if sensor.isOnline():

			module = sensor.get_module()
			serial = module.get_serialNumber()

			if not serial in result:
				result[serial] = __walk_module(module)

			functionId = sensor.get_functionId();
			result[serial]['sensors'][functionId] = __walk_sensor(sensor)

		sensor = sensor.nextSensor()

	return result

def __check_api_version():
	"""Check api version - we use some of the new features and at the time of
	writing this, that version isn't available from pip yet."""
	version = YAPI.GetAPIVersion()
	(major, minor, build) = version.split()[0].split('.')

	if int(major) != 1:
		sys.exit('init error: Major Version mismatch, need major version "1" for "1.10+", your current version is "%s"' % version)
	if int(minor) < 10:
		sys.exit('init error: Minor Version mismatch, need minor version "10" for "1.10+", your current version is "%s"' % version)

def __init_api():
	"""Setup the API to use local USB devices."""
	errmsg = YRefParam()
	if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
		sys.exit("init error: %s" % errmsg.value)

def GetMeasurements():
	"""Enumerates all modules and sensors, reads their current measurements and
	returns everything as a simple map/list structure. Call this method when you
	want to use this script from your own python code."""

	__check_api_version()
	__init_api()
	return __walk_sensors()

def main():
	"""Main method. Gets all measurements and dumps them as json to stdout."""
	result  = GetMeasurements()
	print json.dumps(result, ensure_ascii=True, indent=4)

if isMain:
	sys.exit(main())
