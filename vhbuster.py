#!/usr/bin/env python3

import argparse, requests, json, random, string, re
from multiprocessing import Pool	
banner =\
"""VHbuster running.
Host names:	{}
Ip addresses:	{}
Outfile:	{}
"""

def setup():
	########## Setup
	global domains, args, httpIps, output
	parser = argparse.ArgumentParser(description="Find virtual hosts on a list or single ip address.")

	parser.add_argument("-iL",help="Location of file containing ip addresses.",metavar="/path/to/ip/file")
	parser.add_argument("-i",help="List of ip addresses, seperated by commas.",metavar="127.0.0.1")
	parser.add_argument("domains",help="Location of file containing potential virtual hosts.")
	parser.add_argument("-t",help="Amount of threads to run at once.",metavar="5",default=2,type=int)
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
	

	# Set up a list of domains.
	try:
		with open(args.domains,"r") as f:
			domains = [line.rstrip() for line in f]
	except:
		print("Error: Could not open domain file.")


	############## Tests
	if ips == []:
		print("Error:	Ip address required.")
		exit()
	regex = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
	for ip in ips:
		if not re.match(regex,ip): #Matches valid ipv4 addresses.
			print(f"Error:	{ip} is not a valid ip address.")
			exit()
	#Add default file output, if a directory is specified.
	if args.o:
		if args.o[-1] == "/":
			args.o+="vhbuster.out"
	output=""

	if args.http_only and args.https_only:
		print("Error:	Can not run with both no-http and no-https.")
		exit()
	



def randomString(Slen): # Generate a random string of Slen length.
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(Slen))

def cleanIps(normal_ips): #Check how an ip address responds to invalid host
	global output
	cleaned={}
	for ip in normal_ips:
		try:
			r = requests.get(ip,timeout=args.timeout,headers={"Host":randomString(10)+".com"})
			cleaned[ip] = r
		except:
			print(f"{ip}	----->	not responding")
			output+= f"{ip} ----> not responding\n"
	return cleaned


def bruteforce(domain): #Check which ip addresses respond to this host.
	global valid, CleanedIps
	output = ""
	for ip in CleanedIps.keys():
		r = requests.get(ip,headers={"Host":domain},timeout=10)

		if (r.text + str(r.status_code)) != (CleanedIps[ip].text + str(CleanedIps[ip].status_code)):
			output+= ip + " ----> " + domain+"\n"
			print(f"{ip} ----> {domain}")
	return output

if __name__ == "__main__":
	setup()
	print(banner.format(domains,httpIps,args.o))
	output+=banner.format(domains,httpIps,args.o)+"\n"

	###### Start scan
	valid=[]
	CleanedIps = cleanIps(httpIps)
	#Threads
	p = Pool(args.t)
	results = p.map(bruteforce,domains)
	p.close()
	p.join()	
	
	#Save output
	if args.o:
		for item in results: # Combind results
			if item:
				output+=item

		try: # write to file
			with open(args.o,'w') as f:
				f.write(output)
				f.close()
		except:
			print("Error:	Could not write to outfile.")