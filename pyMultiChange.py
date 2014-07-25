#!/usr/bin/env python

from pyRouterLib import *
import os, argparse, paramiko, time

''' Define hosts file, command file, verbose variables '''
hosts_file = ''
cmd_file = ''
verbose = False

def arguments():
	''' Function to define the script command line arguments '''
	global hosts_file, cmd_file, verbose
	
	parser = argparse.ArgumentParser(description='A Python implementation of MultiChange, which allows you to make mass changes to routers and switches via SSH.')
	parser.add_argument('-d', '--hosts', help='Specify a host file', required=True)
	parser.add_argument('-c', '--commands', help='Specify a commands file', required=True)
	parser.add_argument('-v', '--verbose', nargs='?', default=False, help='Enables a verbose debugging mode')

	args = vars(parser.parse_args())

	if args['hosts']:
		hosts_file = args['hosts']
	if args['commands']:
		cmd_file = args['commands']
	if args['verbose'] == None:
		verbose = True
	
	return hosts_file, cmd_file, verbose

arguments()

''' open the hosts file and commands file and execute each command on every host '''
if os.path.isfile(hosts_file):
	hosts = open(hosts_file, 'r')
	for host in hosts:
		host = host.strip("\n")
		
		''' use pyRouterLib to grab the user authentication credentials '''
		rlib = pyRouterLib(host)
		creds = rlib.get_creds()
		username = creds[0]
		password = creds[1]
		enable = creds[2]
		
		''' Enable verbose debugging '''
		if verbose:
			rlib.debug()
		
		remoteConnectionSetup = paramiko.SSHClient()
		remoteConnectionSetup.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remoteConnectionSetup.connect(host, username=username, password=password, allow_agent=False, look_for_keys=False)
		print "*** SSH connection established to %s" % host
		remoteConnection = remoteConnectionSetup.invoke_shell()
		print "*** Interactive SSH session established"
		cmds = open(cmd_file, 'r')
		for command in cmds:
			remoteConnection.send(command)
			output = remoteConnection.recv(1000)
			time.sleep(2)
			print output
		cmds.close()
	hosts.close()