#!/usr/bin/python
from __future__ import division
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import subprocess
import time
import sys
import numpy as np
import serial

devLookup = {}

def preview(data):
	"""
		Show a plot of the data collected in the last run
	"""
	#from: http://stackoverflow.com/questions/5328556/histogram-matplotlib
	hist, bins = np.histogram(data, bins=50)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	#plt.yscale('log', nonposy='clip')
	plt.show()

def toTimestamp(dt, epoch=datetime(1970,1,1)):
	"""
		From: http://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
	"""
	td = dt - epoch
	# return td.total_seconds()
	return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6 

def save(error, data, devID, note = ""):
	"""
		If error is false save the results to a file with a header including:
		#Date and Time
		#identifier of Device Under Test (DUT)
		#note
		[data]
		[data]
		...

		If error is true then file is saved to the 'bad' directory
		with a note
	"""
	prefix = "data_collection/"
	discard = "bad/"
	now = datetime.utcnow()
	fileName = str(toTimestamp(now)) + ".txt"
	fullPath = ""

	print "Saved to: ",
	if not error:
		fullPath = prefix + fileName
	else:
		fullPath = prefix + discard + fileName

	print fullPath

	with open(fullPath, "w") as f:
		f.write("#" + str(now) + "\n")
		f.write("#" + devID + "\n")
		f.write("#" + note + "\n")
		for entry in data:
			f.write (str(entry) + "\n")

def getDevicesToTest ():
	"""
		Determine which devices are available to test by
		scanning the area
	"""
	devCount = 0

	while devCount == 0: 
		child = subprocess.Popen (['node', 'scan.js'], stdout=subprocess.PIPE)
		time.sleep (5) # search for 5 seconds
		child.kill ()
		for line in child.stdout:
			things = line.split()

			query  = "" + things[0] + " " + things[1] + " " + things[2] + ""
			proc = subprocess.Popen(['grep', query, 'ids'], stdout=subprocess.PIPE)
			streamdata = proc.communicate()[0]
			if 0 == proc.returncode:
				devCount += 1
				entry = streamdata
				identifier = entry.split()[0].strip()
				devLookup[identifier] = query

	return list(devLookup.keys())

def collect (dev, numSamples):
	samples = []
	count = 0
	print 'Collecting samples',
	sys.stdout.flush()

	if "UWB" == dev:
		ser = serial.Serial('/dev/ttyUSB0', 115200)
		for line in ser:
			things = line.split(":")
			if things[0] == "Range":
				data = things[1]
				# if len(window) >= 1:
				# 	del window[0]

				print '.',
				sys.stdout.flush()
				samples.append(float(data)) #only number on line
				count += 1

			if count == numSamples:
				ser.close()
				break
		#child = subprocess.Popen (['python', 'collect_uwb.py'], stdout=subprocess.PIPE)
	else:
		child = subprocess.Popen (['node', 'scan.js'], stdout=subprocess.PIPE)
	
		while count < numSamples:
			sys.stdout.flush()

			line = child.stdout.readline()
			sys.stdout.flush()
				
			if devLookup[dev] in line:
				print '.',
				samples.append(int(line.split()[-2]))
				count += 1
		
	
		child.kill()
	return samples

def main():
	response = 'c'

	while (response == 'c'):
		print "1) Test UWB"
		print "2) Test Estimote"
		devChoice = int(raw_input("Choose what to test: "))

		if 1 == devChoice:
			dev = "UWB"
			devList = {}
			devList [dev] = dev
		else:
			devList = getDevicesToTest()

			for i, dev in enumerate (devList):
				print str(i) + ") " + str(dev)

			dev = int (raw_input("Select device to test: "))
			if 0 > dev or len (devList) <= dev:
				print "Bad selection"
				break

		dist = float(raw_input ("Distance: "))
		if dist < 0:
			print "Not possible"
			break

		temp = raw_input ("Number of samples (default = 50) ")
		if '' == temp:
			numSamples = 50
		else:
			numSamples = int (temp)

		print ""
		print "Settings for test:"
		print "************************************"
		print "DUT: " + devList[dev]
		print "Distance: " + str(dist)
		print "Number of samples: " + str(numSamples)
		print "************************************"

		val = raw_input("Press Enter to continue or q to quit...")
		if 'q' == val:
			pass
		else:
			samples = collect (devList[dev], numSamples)
			preview(samples)
			print ""
			doSave = raw_input("Save results (y/n): ");
			if 'y' == doSave.lower():
				note = raw_input("Add'l note? ")
				save(False, samples, devList[dev], str(dist) + " " + note)
			else:
				note = raw_input("Reason for rejection? ");
				save (True, samples, devList[dev], note)

		print ""
		response = raw_input("[c]ontinue or [q]uit? ")


if __name__ == "__main__":
	main()
