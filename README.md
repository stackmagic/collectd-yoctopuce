THIS IS A WORK IN PROGRESS!!

yoctopuce-collectd
==================

Python Script that can be used with [Collectd](https://collectd.org/)'s
[Exec plugin](https://collectd.org/wiki/index.php/Plugin:Exec) to read out
values of your [yoctopuce](https://yoctopuce.com) devices.

Instructions
============

Set up your yoctopuce device as described in the
[yoctopuce docs](https://github.com/yoctopuce/yoctolib_python/tree/master/Documentation)
and make sure it works.

If you want, give your devices a pretty name (using the
[yoctopuce virtualhub](https://www.yoctopuce.com/EN/virtualhub.php)). The
name will be used in the graph's name. Also make sure you don't name multiple
sensors of the same type with the same name or else they will rival each other.

Install the yoctopuce library

	pip install yoctopuce
