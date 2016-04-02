
import urllib2
import json
import time

from time import gmtime, strftime
from functools import partial

iids = [305,290,464,522,2023,367,3155,3134,3132,137]

def getStations():
	loc = "http://www.citibikenyc.com/stations/json"
	top = urllib2.urlopen(loc).read()
	data = json.loads(top)

	return data["stationBeanList"]
	
def getDetails():
	
	try:
		allStations = getStations() 

		id = "id"
		ab = "availableBikes"

		def parse(s): return (s[id], s[ab])
		#parse = lambda s : (s[id], s[ab])
		#def check(s): return s[id] in iids
		#check = lambda s : s[id] in iids
		def check(s): return s[0] in iids # already parsed into tuple

		pAllStations = [parse(s) for s in allStations]
		count = 0
		for s in pAllStations:
			count += s[1]
		
		stations = [s for s in pAllStations if check(s)]
		stations.append(("All",count))

		return stations
	except:
		return "error gettting details"
	
def writeLnToFile( filename , text ):
	fl = open(filename, 'a')
	fl.write(text)
	fl.write('\n')
	fl.close()

def getTime():	
	return strftime("%Y-%m-%d %H:%M:%S", gmtime())
	
def keepGoing( x, fname ):
	p = partial(writeLnToFile, fname)
	while( x > 0 or x == -1 ):
		p( getTime() + str(getDetails()) )
		time.sleep(60)
		if x > 0: x -= 1
