#!/usr/bin/python3

#import necessary libs
from netaddr import *
from pathlib import Path
import json
import sys
import argparse
import os

#create parser with necessary arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', required=True, help='Source file path')
parser.add_argument('-d', '--destination', required=True, help='Destination folder (conatins ipv4, ipv4-merged, ipv6 and ipv6-merged files')
parser.add_argument('--force', required=False, help='Overwrite destination files', default=False, action='store_const', const=True)
parser.add_argument('-f', '--filter', required=True, help='String to filter in as-name column', type=str)
#get the arguments
args = parser.parse_args()

#set variables
src = args.source
dst = args.destination
force = args.force
dstfiles = ['ipv4.txt', 'ipv4-merged.txt', 'ipv6.txt', 'ipv6-merged.txt']


#check source
if not Path(src).exists():
	exit('Source file does not exist. Exiting.')
#check destination folder and try to create if not exists
if not Path(dst).exists():
	print('Destination folder does not exist. Creating it.')
	try:
		os.mkdir(dst)
		print(f'Destination folder {dst} created successfully.')
	except PermissionError:
		exit('Error creating destination folder: Permission denied')
	except Exception as e:
		print(f'An error occured: {e}')
#check destination files and --force operator if we continue
for dstfile in dstfiles:
	if Path(dst + '/' + dstfile).exists() and not force:
		exit('Destination file exists but --force operator not chosen. Exiting.')

#set further variables
filter = args.filter

#create empty array for networks
networks_v4 = []
networks_v6 = []

#read asndb line for line
with open(src) as file:
	for line in file:
		#load JSON object (each line has to be one object)
		obj = json.loads(line)
		#load asname into variable and lower it
		asname = str(obj['as_name']).lower()
		#load network into variable as IPNetwork (netaddr)
		network = IPNetwork(obj['network'])
		#check if asname (lower) contains AS filter (lower)
		if filter.lower() in asname:
			#skip on failure checking IP-Version, otherwise append network to belonging array
			if network.version == 4:
				networks_v4.append(network)
			elif network.version == 6:
				networks_v6.append(network)

#merge networks
networks_v4_merged = cidr_merge(networks_v4)
networks_v6_merged = cidr_merge(networks_v6)

#write to files (overwrite existing as --force check would have exited the script)
#ipv4.txt
with open(dst + '/' + 'ipv4.txt', 'w') as f:
	for network in networks_v4:
		f.write(str(network) + '\n')
#ipv4-merged.txt
with open(dst + '/' + 'ipv4-merged.txt', 'w') as f:
        for network in networks_v4_merged:
                f.write(str(network) + '\n')
#ipv6.txt
with open(dst + '/' + 'ipv6.txt', 'w') as f:
        for network in networks_v6:
                f.write(str(network) + '\n')
#ipv6-merged.txt
with open(dst + '/' + 'ipv6-merged.txt', 'w') as f:
        for network in networks_v6_merged:
                f.write(str(network) + '\n')
