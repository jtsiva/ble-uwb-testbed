#!/usr/bin/python
import sys
import json
import subprocess

def main ():
	data = json.loads(sys.stdin.read())
	#print data
	if len(sys.argv) >= 2:
		pwrThreshold = sys.argv[1]
	else:
		pwrThreshold = -100

	for device in data:
		print device["identifier"],
		print str.lower(str(device["settings"]["advertisers"]["ibeacon"][0]["uuid"]).replace('-', '')),
		print str(device["settings"]["advertisers"]["ibeacon"][0]["major"]),
		print str(device["settings"]["advertisers"]["ibeacon"][0]["minor"])

if __name__ == "__main__":
    main()