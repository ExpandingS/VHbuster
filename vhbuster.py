#!/usr/bin/env python3

import argparse, requests, json, random, string

banner =\
"""VHbuster running.
Host names: {}
Ip addresses: {}
"""

def setup():
	# Setup
	global ips, domains
	parser = argparse.ArgumentParser(description="Find virtual hosts on a list or single ip address.")

	parser.add_argument("-iL",help="Location of file containing ip addresses.",metavar="/path/to/ip/file")
	parser.add_argument("-i",help="List of ip addresses, seperated by commas.",metavar="127.0.0.1")
	parser.add_argument("domains",help="Location of file containing potential virtual hosts.")
	parser.add_argument("-t",help="Amount of threads to run at once.",metavar="5",default=10,type=int)
	parser.add_argument("-l",help="Limit requests to one ip per minute.",metavar="5",type=int)
	args = parser.parse_args()

	ips=[] # Set up a list of ip addresses and virtual hosts.
	if args.iL:
		try:
			with open(args.iL,"r") as f:
				ips = [line.rstrip() for line in f]
		except:
			print("Error:	Could not read ip file.")
			exit()
	if args.i:
		ips += args.i.split(",")

	try:
		with open(args.domains,"r") as f:
			domains = [line.rstrip() for line in f]
	except:
		print("Error: Could not open domain file.")


def randomString(Slen):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(Slen))

#A bruteforce class for every ip.
class bruteforcer:
	def __init__(self,ip,vh): #accepts an ip address and a list of potential domain names.
		self.ip=ip
		self.vh=vh

	def bruteforce(self):
		valid=[]
		#Find how server responds to non-valid requests.
		r= requests.get("http://"+self.ip,headers={"Host":randomString(10)+".com"})
		normal = r

		#Find valid virtual hosts.
		for host in self.vh:
			headers	= {"host" : host}
			r = requests.get("http://"+self.ip,headers=headers)
			if r.text != normal.text:
				valid.append({ip:host})
				print(ip + " ----> " + host)


if __name__ == "__main__":
	setup()
	print(banner.format(domains,ips))
	bf =[]
	for ip in ips:
		bf.append(bruteforcer(ip,domains))
	for i in bf:
		i.bruteforce()