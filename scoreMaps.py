from logMsg import logMessage
# Scoring mechanisms for gerrymandered maps

# compares map against 'natural' voronoi diagrams map
def getGeographicScore(claims, controlClaims):
	size = len(claims) * len(claims[0])
	
	correctCount = 0
	for y in xrange(len(claims)):
		for x in xrange(len(claims[0])):
			if claims[y][x] == controlClaims[y][x]:
				correctCount += 1
	
	return float(correctCount) / size

	
# def getPopulationScores
# Compared expected population centers to result population centers
def getPopulationScores(regions, claims, centers):
	partySeats = {}
	
	regionPops = {}
	
	totalDistricts = len(centers)
	correctParties = 0
	
	for y in xrange(len(claims)):
		for x in xrange(len(claims[0])):
			id = claims[y][x]
			if id not in regionPops:
				regionPops[id] = {}
			if regions[y][x] not in regionPops[id]:
				regionPops[id][regions[y][x]] = 0
			
			regionPops[id][regions[y][x]] += 1
	
	for center in centers:
		expectedParty = center['alignment']
		resultParty = max(regionPops[center['id']], key = lambda g: regionPops[center['id']][g])
		if expectedParty == resultParty:
			correctParties += 1
		else:
			logMessage(['incorrect party for id', center['id'], 'expected:', expectedParty, 'result:', resultParty])
	
	logMessage(regionPops)
	return float(correctParties) / totalDistricts
	