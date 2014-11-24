from pyRouterLib import *

access_method = RouterLib()

switch = '172.16.0.1'

telnet_test = access_method.use_telnet(switch, RouterLib.username, RouterLib.password)

print "** Telnet Method: "
print telnet_test

telnet_cmd = telnet_test[-1]

telnet_cmd.write('show version\n')
telnet_cmd.write('exit\n')
print telnet_cmd.read_all()

ssh_test = access_method.use_ssh(switch, RouterLib.username, RouterLib.password)

print "** SSH Method: " 
print ssh_test

ssh_cmd = ssh_test[-1]

stdin, stdout, stderr = ssh_cmd.exec_command('show version\n')
for i in stdout:
	print i
ssh_cmd.close()