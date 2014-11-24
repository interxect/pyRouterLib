pyRouterLib
===========

NOTE: This is still very much a work in progress. Don't expect it to have much functionality at this time.

RouterLib is a python library of commonly used functions for managing routers and switches. The purpose is to stream line the scripting process. As my primary experience is with Cisco, this script is very Cisco centric - particularly the telnet modele as it relies on an expect interaction model -, but can potentially be used with other vendor routers and switches.

Functions currently being written are:

* Accessing a device via telnet
* Accessing a device via ssh
* Accessing a device via snmp

## Using and storing credentials. 

By default, RouterLib assumes that you're going to use the library for automation and orchestration of network components. Thus, it creates a credentials file in ~/.tacacslogin. This file is very simple. The first line is the username, the second line is the user password, and the third line is the enable password. 

Example:

```
username
us3r_p4ssw4rd
3n4bl3_p4ssw0rd
```

I realize that this is a very insecure method of storing credentials and will spend some time coming up with a better solution.

## Telnet Module

The telnet module uses the telnetlib library, which is very expect centric. This means that you need to account for the expected output when interacting and sending commands via telnet.

Here is a example script using the telnet module:

```python

from pyRouterLib import *

access_method = RouterLib()

telnet_test = access_method.use_telnet('172.16.0.1', RouterLib.username, RouterLib.password)

print "** Telnet Method: "
print telnet_test

telnet_cmd = telnet_test[-1]

telnet_cmd.write('show version\n')
telnet_cmd.write('exit\n')
print telnet_cmd.read_all()

```

Here is the output from the telnet module:

```
** Telnet Method: 
('172.16.0.1', 'testuser', 'testpassword', False, <telnetlib.Telnet instance at 0x109f83f38>)
show version

Cisco IOS Software, C3550 Software (C3550-IPSERVICESK9-M), Version 12.2(44)SE6, RELEASE SOFTWARE (fc1)

Copyright (c) 1986-2009 by Cisco Systems, Inc.

Compiled Mon 09-Mar-09 20:28 by gereddy

Image text-base: 0x00003000, data-base: 0x012A99FC



ROM: Bootstrap program is C3550 boot loader



core1a.sat uptime is 9 weeks, 2 days, 21 hours, 10 minutes

System returned to ROM by power-on

System image file is "flash:c3550-ipservicesk9-mz.122-44.SE6.bin"





This product contains cryptographic features and is subject to United

States and local country laws governing import, export, transfer and

use. Delivery of Cisco cryptographic products does not imply

third-party authority to import, export, distribute or use encryption.

Importers, exporters, distributors and users are responsible for

compliance with U.S. and local country laws. By using this product you

agree to comply with applicable laws and regulations. If you are unable

to comply with U.S. and local laws, return this product immediately.



A summary of U.S. laws governing Cisco cryptographic products may be found at:

http://www.cisco.com/wwl/export/crypto/tool/stqrg.html



If you require further assistance please contact us by sending email to

export@cisco.com.



Cisco WS-C3550-24 (PowerPC) processor (revision G0) with 65526K/8192K bytes of memory.

Processor board ID CHK0644W0KC

Last reset from warm-reset

Running Layer2/3 Switching Image



Ethernet-controller 1 has 12 Fast Ethernet/IEEE 802.3 interfaces



Ethernet-controller 2 has 12 Fast Ethernet/IEEE 802.3 interfaces



Ethernet-controller 3 has 1 Gigabit Ethernet/IEEE 802.3 interface



Ethernet-controller 4 has 1 Gigabit Ethernet/IEEE 802.3 interface



24 FastEthernet interfaces

2 Gigabit Ethernet interfaces



The password-recovery mechanism is enabled.

384K bytes of flash-simulated NVRAM.

Base ethernet MAC Address: 00:0B:46:FE:D5:80

Motherboard assembly number: 73-5700-09

Power supply part number: 34-0966-02

Motherboard serial number: CAT064307TM

Power supply serial number: LIT063501PN

Model revision number: G0

Motherboard revision number: A0

Model number: WS-C3550-24-SMI

System serial number: CHK0644W0KC

Configuration register is 0x10F



testdevice#exit



```

In the output of 'print telnet_test', you will see a list item that shows 'False'.

```

('172.16.0.1', 'testuser', 'testpassword', False, <telnetlib.Telnet instance at 0x109f83f38>)

```

This item is the output of the 'is_nexus' variable, which will detect whether the device is an IOS device or a NX-OS device and adjust the expect output accordingly. You could also write scripts that modify both IOS and NX-OS devices in the same run, but having a command syntax for NX-OS and another for IOS. The immediate type of script that comes to mind is modifying access-lists - as the command syntax is different between IOS and NX-OS.

## SSH Module

The SSH module uses paramiko to access devices. With the way that paramiko interacts, it's much more device agnostic than the telnet module.

Here is a simple script using the SSH module:

```python
from pyRouterLib import *

access_method = RouterLib()

print "** SSH Method: " 
print ssh_test

ssh_cmd = ssh_test[-1]

stdin, stdout, stderr = ssh_cmd.exec_command('show version\n')
for i in stdout:
	print i
ssh_cmd.close()
``` 

Here is the output from the SSH module:

```
** SSH Method: 
('172.16.0.1', 'testuser', 'testpassword', <paramiko.client.SSHClient object at 0x10a34cd90>)
Cisco IOS Software, C3550 Software (C3550-IPSERVICESK9-M), Version 12.2(44)SE6, RELEASE SOFTWARE (fc1)


Copyright (c) 1986-2009 by Cisco Systems, Inc.


Compiled Mon 09-Mar-09 20:28 by gereddy


Image text-base: 0x00003000, data-base: 0x012A99FC





ROM: Bootstrap program is C3550 boot loader





core1a.sat uptime is 9 weeks, 2 days, 21 hours, 10 minutes


System returned to ROM by power-on


System image file is "flash:c3550-ipservicesk9-mz.122-44.SE6.bin"








This product contains cryptographic features and is subject to United


States and local country laws governing import, export, transfer and


use. Delivery of Cisco cryptographic products does not imply


third-party authority to import, export, distribute or use encryption.


Importers, exporters, distributors and users are responsible for


compliance with U.S. and local country laws. By using this product you


agree to comply with applicable laws and regulations. If you are unable


to comply with U.S. and local laws, return this product immediately.





A summary of U.S. laws governing Cisco cryptographic products may be found at:


http://www.cisco.com/wwl/export/crypto/tool/stqrg.html





If you require further assistance please contact us by sending email to


export@cisco.com.





Cisco WS-C3550-24 (PowerPC) processor (revision G0) with 65526K/8192K bytes of memory.


Processor board ID CHK0644W0KC


Last reset from warm-reset


Running Layer2/3 Switching Image





Ethernet-controller 1 has 12 Fast Ethernet/IEEE 802.3 interfaces





Ethernet-controller 2 has 12 Fast Ethernet/IEEE 802.3 interfaces





Ethernet-controller 3 has 1 Gigabit Ethernet/IEEE 802.3 interface





Ethernet-controller 4 has 1 Gigabit Ethernet/IEEE 802.3 interface





24 FastEthernet interfaces


2 Gigabit Ethernet interfaces





The password-recovery mechanism is enabled.


384K bytes of flash-simulated NVRAM.


Base ethernet MAC Address: 00:0B:46:FE:D5:80


Motherboard assembly number: 73-5700-09


Power supply part number: 34-0966-02


Motherboard serial number: CAT064307TM


Power supply serial number: LIT063501PN


Model revision number: G0


Motherboard revision number: A0


Model number: WS-C3550-24-SMI


System serial number: CHK0644W0KC


Configuration register is 0x10F



```

Currently, the SNMP module is a work in progress. I'll update the documentation when I have completed it.