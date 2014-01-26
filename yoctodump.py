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

try:
	from yocto_api import *
	sys.stderr.write('imported from yocto_api directly - you seem to have the yoctopuce lib installed manually\n')
except ImportError:
	from yoctopuce.yocto_api import *
	sys.stderr.write('imported from yocto_api directly - you seem to have the yoctopuce lib from pip\n')

def __walk_function(module, functionNumber):
	serialNumber = module.get_serialNumber()
	functionId   = module.functionId(functionNumber)
	target       = '%s.%s' % (serialNumber, functionId)

	sensor = None
	if functionId == 'humidity':
		sensor = YHumidity.FindHumidity(target)
	if functionId == 'pressure':
		sensor = YPressure.FindPressure(target)
	if functionId == 'temperature':
		sensor = YTemperature.FindTemperature(target)

	result = {}
	result['functionId'] = functionId

	if sensor != None:
		result['advertisedValue'] = sensor.get_advertisedValue()
		result['currentRawValue'] = sensor.get_currentRawValue()
		result['currentValue']    = sensor.get_currentValue()
		result['errorMessage']    = sensor.get_errorMessage()
		result['highestValue']    = sensor.get_highestValue()
		result['logicalName']     = sensor.get_logicalName()
		result['lowestValue']     = sensor.get_lowestValue()
		result['resolution']      = sensor.get_resolution()
		result['unit']            = sensor.get_unit()

	return result

def __walk_module(module):
	result = {}
	result['beacon']          = module.get_beacon()
	result['errorMessage']    = module.get_errorMessage()
	result['firmwareRelease'] = module.get_firmwareRelease()
	result['logicalName']     = module.get_logicalName()
	result['luminosity']      = module.get_luminosity()
	result['productId']       = module.get_productId()
	result['productName']     = module.get_productName()
	result['productRelease']  = module.get_productRelease()
	result['rebootCountdown'] = module.get_rebootCountdown()
	result['serialNumber']    = module.get_serialNumber()
	result['upTime']          = module.get_upTime()
	result['usbBandwidth']    = module.get_usbBandwidth()
	result['usbCurrent']      = module.get_usbCurrent()
	result['userData']        = module.get_userData()

	measurements = {}
	fnCount = module.functionCount()
	for functionNumber in range(0, fnCount):
		functionId               = module.functionId(functionNumber)
		measurements[functionId] = __walk_function(module, functionNumber)

	result['measurements'] = measurements
	return result

def __walk_modules(modules):
	result = {}
	for module in modules:
		serial         = module.get_serialNumber()
		result[serial] = __walk_module(module)

	return result

def __get_modules():
	modules = []
	mod = YModule.FirstModule()
	while mod != None:
		if mod.isOnline():
			modules.append(mod)
		mod = mod.nextModule()
	return modules

def __check_api_version():
	"""Check api version - we use some of the new features and at the time of
	writing this, that version isn't available from pip yet."""
	version = YAPI.GetAPIVersion()
	(major, minor, build) = version.split()[0].split('.')

	if int(major) != 1:
		sys.exit('init error: Major Version mismatch, need "1", full version is "%s"' % version)
	if int(minor) < 10:
		sys.exit('init error: Minor Version mismatch, need "10", full version is "%s"' % version)

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

	modules = __get_modules()
	result  = __walk_modules(modules)
	return result

def main():
	"""Main method. Gets all measurements and dumps them as json to stdout."""
	result  = GetMeasurements()
	print json.dumps(result, ensure_ascii=True, indent=4)

if __name__ == '__main__':
	sys.exit(main())
