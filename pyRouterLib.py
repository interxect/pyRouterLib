class pyRouterLib:
	'''
	Requirments:
	*** Modules:
		os, getpass, paramiko, logging
	'''
	
	def __init__(self, host):
		self.host = host
	
	''' Granular debugging that assists in trouble shooting issues '''
	def debug(self):
		import logging
		logging.basicConfig(level=logging.DEBUG)
	
	''' Define where to get user credentials '''
	def getCreds(self):
		from os.path import expanduser
		import os.path
		homeDir = expanduser("~")
		credsFile = ".tacacslogin"
		credsFile = homeDir + "/" + credsFile
		
		if os.path.isfile(credsFile):
			print "Using existing credentials file."
			credsFileLocation = open(credsFile)
			self.username = credsFileLocation.readline()
			self.username = self.username.strip('\n')
			self.password = credsFileLocation.readline()
			self.password = self.password.strip('\n')
			self.enable = credsFileLocation.readline()
			self.enable = self.enable.strip('\n')
			credsFileLocation.close()
		else:
			import getpass
			print "You have not created a credentials file."
			self.username = raw_input("Username: ")
			self.password = getpass.getpass("User Password: ")
			self.enable = getpass.getpass("Enable Password: ")
		
		username = self.username
		password = self.password
		enable = self.enable
		
		return username, password, enable
		
	def useSSH(self, host):
		import paramiko
		import time
		
		remoteConnectionSetup = paramiko.SSHClient()
		remoteConnectionSetup.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remoteConnectionSetup.connect(host, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)
		print "SSH connection established to %s" % host
		remoteConnection = remoteConnectionSetup.invoke_shell()
		print "Interactive SSH session established"
		output = remoteConnection.recv(1000)
		print output
		remoteConnection.send("\n")
		remoteConnection.send("show ver\n")
		output = remoteConnection.recv(5000)
		time.sleep(2)
		print output
