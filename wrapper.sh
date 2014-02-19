#!/bin/bash

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
# this script is a temporary hack until
# a) v 1.10 of the yoctolib is in pip
# b) i get around to write a collectd plugin in python
#

set -e

# get script dir (http://stackoverflow.com/a/246128/738323)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# script cannot output anything else besides the collectd text protocol so
# we write all other output into a log file
LOG="${DIR}/wrapper.log"

pushd "${DIR}" >>${LOG}

# make sure the log doesn't grow too large (10MB)
if [ $(stat -c%s "wrapper.log") -gt 10485760 ]; then
	> "${LOG}"
fi

if [ ! -d "yoctolib_python" ]; then
	git clone https://github.com/yoctopuce/yoctolib_python.git yoctolib_python >>${LOG}
	pushd yoctolib_python                                                      >>${LOG}
	git checkout "v1.10.beta"                                                  >>${LOG}
	popd                                                                       >>${LOG}
fi

# temporary until pip sports the latest version (1.10)
export PYTHONPATH="${DIR}/yoctolib_python/Sources"

${DIR}/collectd-yoctopuce.py
