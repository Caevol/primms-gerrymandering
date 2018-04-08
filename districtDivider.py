from mapMaker import getEuclideanDistance

# cede territory
def cedeTerritory(regions, claims, districts):
	pass


# Find voronoi regions
def getVoronoiClaims(regions, centers):
	claims = [['_' for x in xrange(len(regions[0]))] for y in xrange(len(regions))]

	for y in xrange(len(regions)):
		for x in xrange(len(regions)):
			minCenter = None
			minDistance = 100000000
			for center in centers:
				newDistance = getEuclideanDistance(x, y, center['x'], center['y'])
				if newDistance < minDistance:
					minDistance = newDistance
					minCenter = center
				claims[y][x] = minCenter['id']
	
	return claims
	pass


# Primm's approach
def getPrimmsClaims(regions, centers, partyThreshold):
	pass
