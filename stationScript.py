
import urllib2
import json
import time

from time import gmtime, strftime
from functools import partial

iids = [305,290,464,522,2023,367]

def getStations():
	loc = "http://www.citibikenyc.com/stations/json"
	top = urllib2.urlopen(loc).read()
	data = json.loads(top)

	return data["stationBeanList"]
	
def getDetails():
	
	allStations = getStations() 
	
	id = "id"
	ab = "availableBikes"
	
	def parse(s): return (s[id], s[ab])
	#parse = lambda s : (s[id], s[ab])
	def check(s): return s[id] in iids
	#check = lambda s : s[id] in iids
	
	stations = [parse(s) for s in allStations if check(s)] 
	
	return stations
	
def writeLnToFile( filename , text ):
	fl = open(filename, 'a')
	fl.write(text)
	fl.write('\n')
	fl.close()

def getTime():	
	return strftime("%Y-%m-%d %H:%M:%S", gmtime())
	
fname = 'C:\users\karl\bikeStationDataP.txt'
p = partial(writeLnToFile, fname)

def keepGoing( x ):
	while( x > 0 or x == -1 ):
		p( getTime() + str(getDetails() )
		time.sleep(60)
		x -= 1
