#!/usr/bin/python

import sys
import subprocess
import json

def main():
	try:
		for line in sys.stdin:
			things = line.split()
			query  = "" + things[0] + " " + things[1] + " " + things[2] + ""
			proc = subprocess.Popen(['grep', query, 'ids'], stdout=subprocess.PIPE)
			streamdata = proc.communicate()[0]
			if 0 == proc.returncode:
				entry = streamdata
				identifier = entry.split()[0].strip()
				appId = ""
				with open ("app_id") as f:
					appId = f.readline().replace('\n', '')
				appToken = ""
				with open ("app_token") as f:
					appToken = f.readline().replace ('\n', '')

				cmd = "curl -X GET 'https://cloud.estimote.com/v2/devices/" + identifier + "' -u " + appId + ":" + appToken + " -H 'Accept:application/json'"
				with open ("junk.txt", "w") as junk:
					proc = subprocess.Popen (['curl', '-X', 'GET',
						'https://cloud.estimote.com/v2/devices/' + identifier,
						'-u', appId + ":" + appToken,
						'-H', 'Accept:application/json'], stderr=junk, stdout=subprocess.PIPE)
					streamdata = proc.communicate()[0]
					data = json.loads(streamdata)
					print data["identifier"],
					print data["shadow"]["name"]#data["color"],
					print line
			# else:
			# 	print query + " not found"
				#proc = subprocess.Popen
	except KeyboardInterrupt:
		pass



if __name__ == "__main__":
	main()