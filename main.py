from districtDivider import getVoronoiClaims, getPrimmsClaims
from mapMaker import generateRandomMap, generateClusteredMap, getRandomCenters, getManualCenters, assignCenters, assignIndex
from drawMap import drawMap


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
	
	print 'What map would you like to compare?'
	print '1. Prebuilt map'
	print '2. Random map, equal populations between parties'
	print '3. 2 party map with clustered distribution'
	print '4. Build your own map'
	
	result = int(raw_input())
	
	if result == 1:
		regions = simpleArea
	elif result == 2:
		print 'Size of map?'
		size = int(raw_input())
		print 'number of parties?'
		parties = int(raw_input())
		partyRatios = []
		for i in xrange(parties):
			print 'Member ratio for party', colors[i]
			partyRatios.append(float(raw_input()))
		
		regions = generateRandomMap(size, size, colors[:parties], partyRatios)
	elif result == 3:
		print 'Size of map?'
		size = int(raw_input())
		print 'number of clusters?'
		clusters = int(raw_input())
		partyRatios = []
		for i in xrange(2):
			print 'Member ratio for party', colors[i]
			partyRatios.append(float(raw_input()))
		
		regions = generateClusteredMap(size, size, clusters, colors[:2], partyRatios)
	elif result == 4:
		print 'Not yet implemented'
		return None
	else:
		print 'invalid input'
		return None
	
	return regions

def centersMenu(regions):
	print 'How would you like to assign district centers?'
	print '1. Randomly with center radii'
	print '2. Manually'
	result = int(raw_input())
	
	if result == 1:
		print 'What is each district centers radius?'
		rad = int(raw_input())
		print 'How many district centers?'
		centerNum = int(raw_input())
		return getRandomCenters(regions, rad, centerNum)
	elif result == 2:
		return getManualCenters(regions)
	else:
		print 'invalid input'
		return None
	
	
def main():
	
	regions = regionMenu()
	
	if regions is None:
		return
	
	print '\nNow displaying region map, undivided'
	#drawMap(regions, None, None)
	
	centers = centersMenu(regions)
	if centers is None:
		return
		
	print 'For primms agents, what is the threshold ratio the agent must obtain before selecting frontiers randomly?'
	ratio = float(raw_input())
	#drawMap(regions, None, centers)
	
	centers = assignCenters(regions, centers)
	centers = assignIndex(centers)
	
	claimsC = getVoronoiClaims(regions, centers, False)
	claimsV = getVoronoiClaims(regions, centers, True)
	claimsP = getPrimmsClaims(regions, centers, ratio)
	
	drawMap(regions, claimsV, centers)
	drawMap(regions, claimsP, centers)

	
	#get voronoi solution
	#get multiagent solutions
	
	
if __name__ == '__main__':
	main()