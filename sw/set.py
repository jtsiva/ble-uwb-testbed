#!/usr/bin/python

import sys
import os
import subprocess
import time
import json

proximity = ['immediate', 'near', 'far', 'all']

def getDevices (region):
	"""
		Get a list of devices out to proximity. 
		region = [0(immediate) | 1(near) | 2(far) | 3(all)]

	"""
	listOfIDs = {}
	found = 0
	while 0 == found:
		child = subprocess.Popen (['node', 'scan.js'], stdout=subprocess.PIPE)
		time.sleep (5) # search for 5 seconds
		child.kill ()
		for line in child.stdout:
			things = line.split()

			if region >= proximity.index(things[-1]): #last entry is proximity
				query  = "" + things[0] + " " + things[1] + " " + things[2] + ""
				proc = subprocess.Popen(['grep', query, 'ids'], stdout=subprocess.PIPE)
				streamdata = proc.communicate()[0]
				if 0 == proc.returncode:
					found += 1
					entry = streamdata
					identifier = entry.split()[0].strip()
					listOfIDs[identifier] = None

	return list(listOfIDs.keys())

def set (deviceList, key, value):

	appID = ""
	appToken = ""

	with open ("app_id") as f:
			appID = f.readline().replace('\n', '')

	with open ("app_token") as f:
		appToken = f.readline().replace('\n', '')

	for dev in deviceList:
		with open ("junk.txt", "w") as junk:
			proc = subprocess.Popen (['curl', '-X', 'GET',
							'https://cloud.estimote.com/v2/devices/' + dev,
							'-u', appID + ":" + appToken,
							'-H', 'Accept:application/json'], stderr=junk, stdout=subprocess.PIPE)
			streamdata = proc.communicate()[0]
			data = json.loads(streamdata)

		ibeacon = data["settings"]["advertisers"]["ibeacon"]

		ibeacon[0][key] = value
		tmp = '{"pending_settings": {"advertisers":{}}}'
		newData = json.loads(tmp)

		del ibeacon[0]['security']
		del ibeacon[0]['name']
		del ibeacon[0]['enabled']
	
		newData["pending_settings"]["advertisers"][unicode("ibeacon", "utf-8")] = ibeacon

		proc = subprocess.Popen(['curl', 
				'-X', 
				'POST', 
				'https://cloud.estimote.com/v2/devices/' + dev,
				'-u',
				appID+':'+appToken,
				'-H',
				'Accept:application/json',
				'-H',
				'Content-Type:application/json',
				'-d',
				json.dumps(newData)], stdout=subprocess.PIPE)
		stream = proc.communicate ()[0]
		print json.dumps(newData)

def usage ():
	print 'usage: ./set [property] [proximity] [value]'

def main():
	if 4 > len(sys.argv):
		usage ()
		return ()
	else:
		
		prop = sys.argv[1]
		try:
			region = proximity.index(sys.argv[2])
		except ValueError:
			print 'Invalid region!'
			usage ()
			return ()

		value = int(sys.argv[3])

		deviceList = getDevices (region)

		if "interval" == prop:
			set(deviceList, "interval", value)
		elif "power" == prop:
			set(deviceList, "power", value)
		else:
			'Invalid property!'
			usage ()
			return ()



if __name__ == "__main__":
	main()