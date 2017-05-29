#!/usr/bin/python
import sys
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy as np
import math

def logPathLoss (rx):
	#actual 1m measured power (avg) is -67.84, but it doesn't fit well
	dist = 10**((-62 - rx) / (10.0 * 2.0))
	return dist

def main():
	datax = []
	datay = []
	#dataalt = []
	datae = []
	directory = sys.argv[1]
	directory = "data_collection/" + directory

	onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
	
	for file in onlyfiles:
		with open(directory + file) as f:
			count = 0
			valsAtDist = []
			for line in f:
				count += 1
				if count == 3:
					dist = float(line.strip("#").split()[0])
				if "#" not in line:
					valsAtDist.append(float(line))
			
			print np.mean(valsAtDist)
			#dataalt.append(dist)
			datay.append(sorted(valsAtDist)[len(valsAtDist) / 2])
			datae.append(0)#np.std(valsAtDist))
			datax.append(dist)


	fig = plt.figure()
	ax = fig.add_subplot(111)
	#ax.grid(True)
	
	#http://stackoverflow.com/questions/22481854/plot-mean-and-standard-deviation
	plt.errorbar(datax, datay, datae, linestyle='None', marker='o', label="Measured")
	#plt.plot (datax, dataalt, linestyle='None', marker='o', label='Actual')
	plt.xlabel ("Angle (degrees)")
	plt.ylabel ("RSSI (dBm)")
	plt.title ("BLE Horizontal Angle vs Median RSSI (distance=1.5m, TX power=-12dBm)")

	#plt.xticks([i for i in range(len(xAxis))], xAxis, rotation=90)
	plt.legend()
	#fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)
	plt.show()


if __name__ == "__main__":
	main()