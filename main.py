from districtDivider import getVoronoiClaims, getPrimmsClaims
from scoreMaps import getGeographicScore, getPopulationScores
from mapMaker import generateRandomMap, generateClusteredMap, getRandomCenters, getManualCenters, assignCenters, assignIndex
from drawMap import drawMap
from logMsg import logMessage, setRunSilent
import argparse


simpleArea = [
	['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',],
	['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',],
	['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',],
	['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',],
	['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',],
	['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',],
	['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',],
	['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',],
	['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',],
	['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',]
	]

colors = ['g', 'w', 'r', 'b', 'y', 'c']
centers = [{'x':2, 'y':4}, {'x':5, 'y':9}, {'x':1, 'y':8}]

def regionMenu():
# menu settings
	# Compares voronoi and multiagent approaches on the same map
	# 1. Prebuilt map
	# 2. Random Map, equal pops.
	# 3. Random Map, clustered distribution for blue
	# 4. Build Map
	
	
	logMessage('What map would you like to compare?')
	logMessage('1. Prebuilt map')
	logMessage('2. Random map, equal populations between parties')
	logMessage('3. 2 party map with clustered distribution')
	
	result = int(raw_input())
	
	if result == 1:
		regions = simpleArea
	elif result == 2:
		logMessage('Size of map?')
		size = int(raw_input())
		logMessage('number of parties?')
		parties = int(raw_input())
		partyRatios = []
		for i in xrange(parties):
			logMessage(['Member ratio for party', colors[i]])
			partyRatios.append(float(raw_input()))
		
		regions = generateRandomMap(size, size, colors[:parties], partyRatios)
	elif result == 3:
		logMessage( 'Size of map?')
		size = int(raw_input())
		logMessage('number of clusters?')
		clusters = int(raw_input())
		partyRatios = []
		for i in xrange(2):
			logMessage(['Member ratio for party', colors[i]])
			partyRatios.append(float(raw_input()))
		
		regions = generateClusteredMap(size, size, clusters, colors[:2], partyRatios)
	else:
		logMessage('invalid input')
		return None
	
	return regions

def centersMenu(regions):
	logMessage('How would you like to assign district centers?')
	logMessage('1. Randomly with center radii')
	logMessage('2. Manually')
	result = int(raw_input())
	
	if result == 1:
		logMessage('What is each district centers radius?')
		rad = int(raw_input())
		logMessage('How many district centers?')
		centerNum = int(raw_input())
		return getRandomCenters(regions, rad, centerNum)
	elif result == 2:
		return getManualCenters(regions)
	else:
		logMessage('invalid input')
		return None
	
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', action='store_true', help='run program silently, only output results')
	parser.add_argument('-draw', action='store_true', help='draws district division maps')
	args = parser.parse_args()
	setRunSilent(args.s)
	drawGraphs = args.draw
	
	regions = regionMenu()
	
	if regions is None:
		return
	
	
	logMessage('\nNow displaying region map, undivided')
	#drawMap(regions, None, None)
	
	centers = centersMenu(regions)
	if centers is None:
		return
		
	logMessage('For primms agents, what is the threshold ratio the agent must obtain before selecting frontiers randomly?')
	ratio = float(raw_input())
	#drawMap(regions, None, centers)
	
	centers = assignCenters(regions, centers)
	centers = assignIndex(centers)
	
	logMessage('Generating Voronoi (No territory change)...')
	claimsC = getVoronoiClaims(regions, centers, False)
	logMessage('Generating Voronoi (territory change)...')
	claimsV = getVoronoiClaims(regions, centers, True)
	logMessage('Generating Primms')
	claimsP = getPrimmsClaims(regions, centers, ratio)

	logMessage('\n')
	
	logMessage('Getting voronoi scores')
	voronoiScore = { 'GeographicsScore':getGeographicScore(claimsV, claimsC), 
		'LocalPopulationScore':getPopulationScores(regions, claimsV, centers)}
	logMessage('\n')
	
	logMessage('Getting Primms scores')
	primmsScore= { 'GeographicsScore': getGeographicScore(claimsP, claimsC), 
		'LocalPopulationScore':getPopulationScores(regions, claimsP, centers)}
	logMessage('\n')
		
	print 'voronoiScores:', voronoiScore
	print 'Primms Score:', primmsScore
	
	if drawGraphs:
		logMessage('Displaying Voronoi (No Territory change)...')
		drawMap(regions, claimsC, centers)
		logMessage('Displaying Voronoi (Territory change)...')
		drawMap(regions, claimsV, centers)
		logMessage('Displaying Primms')
		drawMap(regions, claimsP, centers)
		
	
	
if __name__ == '__main__':
	main()