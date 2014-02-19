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

if [ ! -d "yoctolib_python" ]; then
	git clone https://github.com/yoctopuce/yoctolib_python.git yoctolib_python >&2
	pushd yoctolib_python                                                      >&2
	git checkout "v1.10.beta"                                                  >&2
	popd                                                                       >&2
fi

# temporary until pip sports the latest version (1.10)
export PYTHONPATH="$(pwd)/yoctolib_python/Sources"

$(pwd)/collectd-yoctopuce.py
