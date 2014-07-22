class pyRouterLib:
	'''
	Requirments:
	*** Modules:
		os, getpass, paramiko
	'''
	
	def __init__(self, host):
		self.host = host
	
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
		
		remoteConnectionSetup = paramiko.SSHClient()
		remoteConnectionSetup.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remoteConnectionSetup.connect(host, username=self.username, password=self.password)
		print "SSH connection established to %s" % host
		remoteConnection = remoteConnectionSetup.invoke_shell()
		print "Interactive SSH session established"
