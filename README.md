
yoctopuce-collectd
==================

Python Script that can be used with [Collectd](https://collectd.org/)'s
[Exec plugin](https://collectd.org/wiki/index.php/Plugin:Exec) to read out
values of your [yoctopuce](https://yoctopuce.com) devices.

Status/Features
===============

* this is still a work in progress
* DONE: enumerate and read all sensors, dump to map/json
  Have a look at `example_output.json` to see what kind of data you can expect.
* TODO: integrate with collectd

Instructions (yoctopuce)
========================

Set up your yoctopuce device as described in the
[yoctopuce docs](https://www.yoctopuce.com/EN/products/virtualhub/doc/VIRTHUB0.usermanual.html)
and make sure it works.

If you want, give your devices a pretty name (using the
[yoctopuce virtualhub](https://www.yoctopuce.com/EN/virtualhub.php)). The
name will be used in the graph's name. Also make sure you don't name multiple
sensors of the same type with the same name or else they will rival each other.

Install the yoctopuce library (as soon as the version in pip is at least
1.10).

	pip install yoctopuce

Right now, the version in pip is still too old. Therefore the wrapper script
will automatically pull the latest dev version from the yoctopuce github repo,
add it to the `PYTHONPATH` and you're set to go. Just use the `wrapper.sh`
script.

Make sure the firmware on your yocto module(s) match the api version. You
can upgrade the firmware using their VirtualHub software. More information and
the downloads are available in their news post
[New features in Yoctopuce API](http://www.yoctopuce.com/EN/article/new-features-in-yoctopuce-api).

Instructions (collectd)
=======================

In the collectd config, you'll need to reference the yoctopuce types, like so:

    TypesDB "/usr/share/collectd/types.db" "/home/SOMEUSER/collectd-yoctopuce/yoctopuce_collectd_types.db"

Add the Exec plugin:

    LoadPlugin exec

Make sure the wrapper script is called:

    <Plugin exec>
        Exec "SOMEUSER:SOMEGROUP" "/home/SOMEUSER/collectd-yoctopuce/wrapper.sh"
    </Plugin>

And restart collectd

    service collectd restart


Troubleshooting
===============

Device doesn't show up
----------------------

When you plug in the device, `dmesg` should print a line like this:

    hid-generic 0003:24E0:0018.0003: hiddev0,hidraw1: USB HID v1.11 Device [Yoctopuce Yocto-Meteo] on usb-0000:00:14.0-1/input0

If that doesn't happen, make sure the `usbserial` kernel module is loaded by executing `modprobe usbserial` as root.

Insufficient Permissions
------------------------

    init error: the user has insufficient permissions to access USB devices (ypkt_lin:312)

You either forgot to add the `/etc/udev/rules.d` file at all or you may need
to give it a higher number (yoctopuce's examples use 51) so it's executed
later. It can happen that some other rules are executed after your own rules,
changing the permissions so you can't write.

Don't forget to disconnect and re-connect the device just after adding your
rules and restarting udevd.

* Unplug the device
* Execute `udevadm monitor`
* Connect the device and note the shortest path printed, e.g. `/devices/pci0000:00/0000:00:14.0/usb3/3-1`
* Execute `udevadm test /devices/pci0000:00/0000:00:14.0/usb3/3-1`
* Look for lines starting with `MODE` to see what other rules are setting permissions on the file
* Rename your rules file accordingly
* Restart udev and re-connect the device. It should work now.
