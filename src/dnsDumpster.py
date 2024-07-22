#!/usr/bin/env python3
import datetime
import requests
from bs4 import BeautifulSoup
import json
import socket
from whois import *
from crt import getCRT
import pandas as pd

import argparse
import sys


class dnsdmpstr():
	"""
	initialization
	this is where the csrf token is fetched & set
	"""
	def __init__(self):
		self.headers = {
			"Referer":"https://dnsdumpster.com"
		}
		r = requests.get("https://dnsdumpster.com", headers=self.headers)
		doc = BeautifulSoup(r.text.strip(), "html.parser")
		try:
			# locate the csrf token
			tag = doc.find("input", {"name":"csrfmiddlewaretoken"})
			self.csrftoken = tag['value']
			# to avoid a 403, the csrftoken cookie has to be set,
			# along with the referer.
			self.headers = {
			"Referer":"https://dnsdumpster.com",
			"Cookie": "csrftoken={0};".format(self.csrftoken)
			}
		except:
			pass

	"""
	filter function for the record tables
	note: make sure txt records are filtered with record_type=1
	      this is because it uses different formatting
	"""
	def _clean_table(self, table, record_type=0):
		retval = {}
		if record_type==1:
			for idx,tag in enumerate(table.find_all('td')):
				retval[idx] = tag.string
		for idx,tag in enumerate(table.find_all('td', { 'class':'col-md-4'})):
			clean_name = tag.text.replace('\n', '')
			clean_ip = tag.a['href'].replace('https://api.hackertarget.com/reverseiplookup/?q=', '')
			retval[idx] = { 'ip':clean_ip, 'host':clean_name}
		return retval

	"""
	return information on given target
	this is where all the records are cleaned and stored
	"""
	def dump(self, target):
		retval = {}
		data = {"csrfmiddlewaretoken": self.csrftoken, "targetip": target}
		r = requests.post("https://dnsdumpster.com", headers=self.headers, data=data)
		doc = BeautifulSoup(r.text.strip(), "html.parser")
		tables = doc.find_all('table')
		try:
			retval['dns'] = self._clean_table(tables[0])
			retval['mx'] = self._clean_table(tables[1])
			retval['txt'] = self._clean_table(tables[2], 1)
			retval['host'] = self._clean_table(tables[3])
			return retval
		except:
			return False

	"""
	execute host search on hackertarget api
	"""
	def hostsearch(self, target):
		try:
			# accepts a domain name
			r = requests.get("https://api.hackertarget.com/hostsearch/?q={}".format(target))
			return(r.text)
		except:
			return("An error occurred.")
	"""
	execute reversedns search on hackertarget api
	"""
	def reversedns(self, target):
		try:
			# accepts an IP, IP range or domain name.
			r = requests.get("https://api.hackertarget.com/reversedns/?q={}".format(target))
			return(r.text)
		except:
			return("An error occurred.")
	


def passive_action(target):
	instance = dnsdmpstr()
	result = ""
	# Use the instance to call methods with the target
	json.dumps(instance.dump(target), indent=1)
	result += "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
	reversedns = (instance.reversedns(target))
	ips = []
	for line in  reversedns.split("\n"):
		# if line.split(",")[1] isnt none
		if line.split(",")[1]:
			name = line.split(",")[0]
			ip = line.split(",")[1]
			dict = {"Domain":name,"IP Address":ip}
			ips.append(dict)
	result += "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
	df = getCRT(target)
	ips_df = pd.DataFrame(ips)
	df = pd.concat([df, ips_df], ignore_index=True)
	# only keep the unique values
	df = df.drop_duplicates(subset=["Domain"])
	# sort on "IP Address"
	df = df.sort_values(by="IP Address")
	# iterate over the values of "IP Address" 
	result += (df.to_string())

	record("dnsDumpster",result)
	return result , df


def passive(target):
	instance = dnsdmpstr()
	result = ""
	# Use the instance to call methods with the target
	result += "starting the dnsdmpstr:\n\n"
	result += (json.dumps(instance.dump(target), indent=1))
	result += ("\nreversedns\n\n\n")
	result += "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
	result += (instance.reversedns(target))

	result += "\n\n\n"
	result += "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
	result += whoIS(target)
	result += "\n\n\n"


	# now we have the ipadress we use it on the whois script
	result += "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
	result += "\nwhois\n\n\n"
	res2 = socket.gethostbyname(target)
	result += (whoIS(res2))

	# getting crt results
	result += "\ncrt\n\n\n"
	result += "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
	result += getCRT(target)
 
	record("dnsDumpster",result)
 

def active_action(target):
	result , df =  passive_action(target)
	for ip in df["IP Address"]:
		# check if the the first value of the ip before "." is 196
		print(ip.split(".")[0])
		if ip.split(".")[0] != "196":
			result	+= "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
			result +=  whoIS(ip)
			res2 = socket.gethostbyname(target)
			result +=  whoIS(res2)
			result	+= "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
			result +=  nmap(ip)
			result	+= "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

	print(df.to_string())
	
 
	record("dnsDumpster",result)


def record(original_filename,result):

	# Get current datetime
	now = datetime.datetime.now()

	# Format datetime into a string (e.g., 2023-04-01_12-30-45)
	timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

	# Append timestamp to the original filename before the extension
	filename_with_timestamp = f"{original_filename}_{timestamp}.txt"

	# Write the results to the file with the timestamp in its name
	with open(filename_with_timestamp, "w") as file:
		file.write(result)
  


def parse_arguments():
    parser = argparse.ArgumentParser(description="Domain Reconnaissance Tool")
    parser.add_argument("domain", help="The domain to perform reconnaissance on")
    parser.add_argument("--mode", choices=['passive', 'active'], default='passive', help="The mode of reconnaissance (passive or active)")
    parser.add_argument("--dictionary", default=None, help="The dictionary file for active scanning (required for active mode)")
    return parser.parse_args()

