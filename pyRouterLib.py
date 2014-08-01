#!/usr/bin/env python

class pyRouterLib:
	'''
	Requirments:
	*** Modules:
		os, getpass, paramiko, logging
	'''
	
	def __init__(self, host, verbose):
		self.host = host
		self.verbose = verbose
	
	''' Granular debugging that assists in trouble shooting issues '''
	def debug(self):
		import logging
		logging.basicConfig(level=logging.DEBUG)
		verbose = True
		
		return verbose
	
	''' Define where to get user credentials '''
	def get_creds(self):
		from os.path import expanduser
		import os.path
		homeDir = expanduser("~")
		credsFile = ".tacacslogin"
		credsFile = homeDir + "/" + credsFile
		
		if os.path.isfile(credsFile):
			print "Using existing credentials file."
			credsFileLocation = open(credsFile)
			self.username = credsFileLocation.readline()
			self.username = self.username.strip()
			self.password = credsFileLocation.readline()
			self.password = self.password.strip()
			self.enable = credsFileLocation.readline()
			self.enable = self.enable.strip()
			credsFileLocation.close()
		else:
			import getpass
			print "You have not created a credentials file. Lets create one..."
			self.username = raw_input("Username: ")
			self.password = getpass.getpass("User Password: ")
			self.enable = getpass.getpass("Enable Password: ")
			
			authFile = open(credsFile, 'w+')
			authFile.write(self.username + "\n")
			authFile.write(self.password + "\n")
			authFile.write(self.enable + "\n")
			authFile.close()
				
			print "Your credentials file has been created and is located at: "
			print credsFile + "\n"

		username = self.username
		password = self.password
		enable = self.enable
		
		return username, password, enable
	
	''' Do not use the below SSH functions, yet. It is not working '''
	
	''' Establish a connection via SSH '''
	def use_ssh(self, host, username, password, verbose):
		import paramiko
		
		global remoteConnection
		
		remoteConnectionSetup = paramiko.SSHClient()
		remoteConnectionSetup.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remoteConnectionSetup.connect(host, username=username, password=password, allow_agent=False, look_for_keys=False)
		
		print "*** SSH connection established to %s" % host
		
		remoteConnection = remoteConnectionSetup.invoke_shell()
		
		if verbose:
			print "*** Interactive SSH session established"
		
		return remoteConnection
		
	''' Once an SSH connection has been established. Enter enable mode '''
	def ssh_enable(self, remoteConnection, username, enable, verbose):
		import time
		
		time.sleep(1)
		
		is_enable = remoteConnection.recv(1000)
		
		if "#" not in is_enable:
			remoteConnection.send("enable\n")
			time.sleep(1)
			if_enable = remoteConnection.recv(1000)
		
			if "Password:" in if_enable:
				if verbose:
					print "*** Sending enable password"
				remoteConnection.send(enable)
				remoteConnection.send("\n")
			time.sleep(2)
			is_enable = remoteConnection.recv(1000)
		
			if "#" in is_enable:
				if verbose:
					print "*** Successfully entered enable mode"
				remoteConnection.send("terminal length 0\n")
			else:
				if verbose:
					print "*** Entering enable mode was unsuccessful"
		else:
			remoteConnection.send("terminal length 0\n")
			if verbose:
				print "*** User: %s already has enable privileges" % username

	''' Send commands to the remote SSH host '''
	def ssh_send(self, remoteConnection, command, verbose):
		import time
		
		command = command.strip()
		
		remoteConnection.send(command)
		remoteConnection.send("\n")
		
		print "*** Executing Command: %s" % command
		
		if verbose:
			time.sleep(2)
			output = remoteConnection.recv(10000)
			print output
		