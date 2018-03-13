#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This tool allows you to search for default credentials for routers, network devices, web applications and more. 
Authors: Viral Maniar, Dr.Lafa
Twitter: https://twitter.com/maniarviral
Github: https://github.com/Viralmaniar
	https://github.com/DrLafa
LinkedIn: https://au.linkedin.com/in/viralmaniar
CodebyNet: https://codeby.net/forum/members/dr-lafa.69885/
'''
import os, sys
import bs4 as bs
import requests
import json
import argparse
	
logo = '''
  ____   _   _ _   
 |  _ \ __ _ ___ ___| | | |_   _ _ __ | |_ 
 | |_) / _` / __/ __| |_| | | | | '_ \| __|
 |  __/ (_| \__ \__ \  _  | |_| | | | | |_ 
 |_|   \__,_|___/___/_| |_|\__,_|_| |_|\__|

 ░░░░  ███████ ]▄▄▄▄▄▄▄▄  
█▄█████████████▄█  	  	  Authors: Viral Maniar, Dr.Lafa
[████████████████████].   	  Twitter: @ManiarViral
 ..◥ ▲ ▲ ▲ ▲ ▲ ▲ ◤..  	          Codebynet:  https://codeby.net/forum/members/dr-lafa.69885/

				  Description: Tool to search default credentials for routers, network devices, web applications and more. 
								  
 '''

def formatTable(table):
	text = ''
	rows = table.find_all('tr')
	text += '%s\n' % rows[0].text

	for row in rows[1:]:
		data = row.find_all('td')
		text += '%s: %s\n' % (data[0].text, data[1].text)

	return text

def search_vendor(vendor):
	url = "https://cirt.net/passwords?vendor=" + vendor
	response = requests.get(url).text
	soup = bs.BeautifulSoup(response, "html.parser")
	#print(soup.find_all('a'))
	data = [formatTable(links) for links in soup.find_all('table')]
	#print(vendor)
	#print(data)
	return data

def load_db():
	with open("rep.json", "r") as database:
		data = json.loads(database.read())
	return data

def update_db():
	vendors = [vendor.split("\t")[1].replace("\n", "").lower() for vendor in open("vendors.txt")]
	
	print("[*] Downloading database. Please wait, it may take time. Usually around 5-10 minutes.")
	data = {}
	full = len(vendors)
	totally = 0
	for vendor in vendors:
		totally += 1
		data[vendor] = search_vendor(vendor)
		sys.stdout.flush()
		print("\r[*] {0}/{1}".format(totally, full), end="")
	
	print("[*] Saving database...")
	j = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4)
	with open('rep.json', 'w') as rep:
		rep.write(j)
	print("[*] Done")

def main():
	parser = argparse.ArgumentParser(description="")
	
	# Arguments
	parser.add_argument('-v', '--vendor', help = 'Vendor to search', metavar='')
	parser.add_argument('-l', '--list', help = 'List vendors', action='store_true')
	parser.add_argument('-u', '--update', help = 'Update local database', action='store_true')
	parser.add_argument('-L', '--local', help='Search from local database', action='store_true')
	
	args = parser.parse_args()
	
	args_list = [args.vendor, args.list, args.update, args.local]
	
	if not args.vendor and not args.list and not args.update:
		print(logo)
		parser.print_help()
		exit(1)
	
	if args.list:
		vendors = open("vendors.txt", "r").read()
		print(vendors)
		exit(0)

	if args.update:
		update_db()
		exit(0)

	if args.vendor:
		if args.local:
			try:
				database = load_db()
			except FileNotFoundError:
				print("Local database not built yet. Use passhunt --update to download.")
				exit(1)
				
			data = database[args.vendor]
		else:
			data = search_vendor(args.vendor)

		for model in data:
			print(model)
		sys.exit(0)
	
	

if __name__ == "__main__":
	main()
