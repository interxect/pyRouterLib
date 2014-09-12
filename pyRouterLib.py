#!/usr/bin/env python

class RouterLib(object):
	
	def __init__(self, verbose):
		self.verbose = verbose
	
		return self.verbose
	
	""" DEBUG Module """
	def enable_debug(self):
		import logging
		logging.basicConfig(level=logging.DEBUG)
		verbose = True
		
		return verbose
	
	""" CREDENTIALS Module """
	def get_creds(self):
		from os.path import expanduser
		import os.path
		import getpass
		creds_file = expanduser('~/.tacacslogin')
		if os.path.isfile(creds_file):
			f = open(creds_file, 'r')
			self.username = f.readline().strip('\n')
			self.password = f.readline().strip('\n')
			self.enable = f.readline().strip('\n')
			f.close()
		else:
			print "Creating %s" % creds_file
			self.username = raw_input("Username: ")
			self.password = getpass.getpass("User Password: ")
			self.enable = getpass.getpass("Enable Password: ")
			
			f = open(creds_file, 'w')
			f.write(self.username + "\n" + self.password + "\n" + self.enable + "\n")
			f.close()
		
		return self.username, self.password, self.enable

	""" TELNET Module """
	def use_telnet(self, host, username, password):
		import telnetlib
		
		self.host = host
		self.username = username
		self.password = password
		self.access = telnetlib.Telnet(self.host)
		
		return self.access, self.host
	
	""" SSH Module """
	def use_ssh(self, host, username, password):
		import paramiko
		
		self.host = host
		self.username = username
		self.password = password
		self.access = paramiko.SSHClient()
		self.access.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.access.connect(host, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)
		
		return self.host, self.username, self.password, self.access
	
	""" SNMP Module """	
	def use_snmp(self):
		from os.path import expanduser
		import os.path
		import pysnmp
		community_file = expanduser('~/.community')
		if os.path.isfile(community_file):
			f = open(community_file, 'r')
			self.read_only = f.readline().strip('\n')
			self.read_write = f.readline().strip('\n')
			f.close()
		else:
			print "Creating %s" % community_file
			self.read_only = raw_input("Read-only Community: ")
			self.read_write = raw_input("Read-write Community: ")
			
			f = open(community_file, 'w')
			f.write(self.read_only + "\n" + self.read_write + "\n")
			f.close()
		
		return self.read_only, self.read_write


