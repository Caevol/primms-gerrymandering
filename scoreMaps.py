
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

	
#def getPopulationScores