#!/usr/bin/env python

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
			self.username = self.username.strip('\n')
			self.password = credsFileLocation.readline()
			self.password = self.password.strip('\n')
			self.enable = credsFileLocation.readline()
			self.enable = self.enable.strip('\n')
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
