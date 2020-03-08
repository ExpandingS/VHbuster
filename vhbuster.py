#!/usr/bin/env python3

import argparse, requests, json, random, string, re

banner =\
"""VHbuster running.
Host names:	{}
Ip addresses:	{}
Outfile:	{}
"""

def setup():
	# Setup
	global ips, domains, args, httpIps, output
	parser = argparse.ArgumentParser(description="Find virtual hosts on a list or single ip address.")

	parser.add_argument("-iL",help="Location of file containing ip addresses.",metavar="/path/to/ip/file")
	parser.add_argument("-i",help="List of ip addresses, seperated by commas.",metavar="127.0.0.1")
	parser.add_argument("domains",help="Location of file containing potential virtual hosts.")
	parser.add_argument("-t",help="Amount of threads to run at once.",metavar="5",default=10,type=int)
	parser.add_argument("-o",help="Outfile",metavar="/path/to/outfile")
	parser.add_argument("--timeout",help="Time in seconds to wait for a response.",default=5,type=int)
	parser.add_argument("--http_only",help="Only send http requests.",action="store_true")
	parser.add_argument("--https_only",help="Only send https requests.",action="store_true")
	args = parser.parse_args()

	# Set up a list of ip addresses and virtual hosts.
	ips=[] 
	if args.iL:
		try:
			with open(args.iL,"r") as f:
				ips = [line.rstrip() for line in f]
		except:
			print("Error:	Could not read ip file.")
			exit()
	if args.i:
		ips += args.i.split(",")

	httpIps = [] #add http codes
	for ip in ips:
		if not args.http_only:
			httpIps.append("https://"+ip)
		if not args.https_only:
			httpIps.append("http://"+ip)
		if args.http_only and args.https_only:
			print("Error:	Can not run with both no-http and no-https.")
			exit()

	# Set up a list of domains.
	try:
		with open(args.domains,"r") as f:
			domains = [line.rstrip() for line in f]
	except:
		print("Error: Could not open domain file.")

	#Tests
	if ips == []:
		print("Error:	Ip address required.")
		exit()
	for ip in ips:
		if not re.match('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',ip): #Matches valid ipv4 addresses.
			print(f"Error:	{ip} is not a valid ip address.")
			exit()

	if args.o:
		if args.o[-1] == "/":
			args.o+="vhbuster.out"
	output=""
	



def randomString(Slen):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(Slen))

#A bruteforce class for every ip.
class bruteforcer:
	def __init__(self,ip,vh): #accepts an ip address and a list of potential domain names.
		self.ip=ip
		self.vh=vh

	def bruteforce(self):
		global output


		#Find how server responds to non-exsistent requests.
		try:
			r= requests.get(self.ip,headers={"Host":randomString(10)+".com"},timeout=args.timeout)
			normal = r
		except:
			output+= f"{self.ip} ----> not responding\n"
			print(f"{self.ip} ----> not responding")
			return

		#Find valid virtual hosts.
		for host in self.vh:
			headers	= {"host" : host}
			r = requests.get(self.ip,headers=headers,timeout=args.timeout)
			if r.text != normal.text:
				output+= self.ip + " ----> " + host+"\n"
				print(self.ip + " ----> " + host)


if __name__ == "__main__":
	setup()
	print(banner.format(domains,ips,args.o))
	bf =[]
	for ip in httpIps:
		bf.append(bruteforcer(ip,domains))
	for i in bf:
		i.bruteforce()
	if args.o:
		# try:
			with open(args.o,'w') as f:
				f.write(output)
				f.close()
		# except:
		# 	print("Error:	Could not write to outfile.")