
yoctopuce-collectd
==================

Python Script that can be used with [Collectd](https://collectd.org/)'s
[Exec plugin](https://collectd.org/wiki/index.php/Plugin:Exec) to read out
values of your [yoctopuce](https://yoctopuce.com) devices.

Status
======

* this is still a work in progress
* DONE: enumerate and read all sensors, dump to map/json
* TODO: integrate with collectd

Instructions (yoctopuce)
========================

Set up your yoctopuce device as described in the
[yoctopuce docs](https://github.com/yoctopuce/yoctolib_python/tree/master/Documentation)
and make sure it works.

If you want, give your devices a pretty name (using the
[yoctopuce virtualhub](https://www.yoctopuce.com/EN/virtualhub.php)). The
name will be used in the graph's name. Also make sure you don't name multiple
sensors of the same type with the same name or else they will rival each other.

Install the yoctopuce library (as soon as the version in pip is at least
1.10).

	pip install yoctopuce

If the version in pip is still too old, install the python library as
instructed by yoctopuce and add the `Sources` directory to your `PYTHONPATH`.

Make sure the firmware on your yocto module(s) match the api version. You
can upgrade the firmware using their VirtualHub software. More information and
the downloads are available in their news post
[New features in Yoctopuce API](http://www.yoctopuce.com/EN/article/new-features-in-yoctopuce-api).

Instructions (collectd)
=======================

TODO
