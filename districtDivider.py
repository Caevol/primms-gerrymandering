from mapMaker import getEuclideanDistance
from random import randint

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


def claimRegion(x, y, id, claims, regions, totalClaims, frontier):
	claims[y][x] = id
	totalClaims[0] -= 1
	
	frontier['totalClaimed'] += 1
	
	if regions[y][x] == frontier['alignment']:
		frontier['aligned'] += 1
	
	
	if y < len(regions) -1 and claims[y+1][x] == '_':
		frontier['frontier'].append({'x':x, 'y':y+1})
	if y > 0 and claims[y-1][x] == '_':
		frontier['frontier'].append({'x':x, 'y':y-1})
	if x < len(regions[0]) - 1 and claims[y][x+1] == '_':
		frontier['frontier'].append({'x':x+1, 'y':y})
	if x > 0 and claims[y][x-1] == '_':
		frontier['frontier'].append({'x':x-1, 'y':y})
	
# Primm's approach to district division. Party threshold determines how many 
# Units of the member's party are recruited before recruiting others
# .5 : majority
# .66 : hyper-majority
def getPrimmsClaims(regions, centers, partyThreshold):
	MIN_REGIONS = int(float(len(regions) * len(regions[0])) / len(centers)) - 15
	THRESHOLD_REGIONS = partyThreshold * MIN_REGIONS
	
	
	claims = [['_' for x in xrange(len(regions[0]))] for y in xrange(len(regions))]
	frontiers = {}

	totalClaims = [(len(regions) * len(regions[0]))]
	
	for center in centers:
		frontiers[center['id']] = {'frontier' : [], 'alignment' : center['alignment'], 'aligned' : 0, 'totalClaimed' : 0, 'active' : True}
		frontier = frontiers[center['id']]
		claimRegion(center['x'], center['y'], center['id'], claims, regions, totalClaims, frontier)	
	
	while totalClaims[0] > 0:
		id = min([f for f in frontiers if frontiers[f]['active'] == True], key = lambda g: frontiers[g]['totalClaimed'])
		
		frontier = frontiers[id]
		#update frontier to only include live members of the frontier
		frontier['frontier'] = [f for f in frontiers[id]['frontier'] if claims[f['y']][f['x']] == '_']
		
		# If there is no frontier, this district cannot claim any more regions
		if len(frontier['frontier']) == 0:
			frontier['active'] = False
			continue
		
		foundAligned = False
		if frontier['aligned'] < THRESHOLD_REGIONS:
			for f in frontier['frontier']:
				if regions[f['y']][f['x']] == frontier['alignment']:
					claimRegion(f['x'], f['y'], id, claims, regions, totalClaims, frontier)
					foundAligned = True
					break

		if foundAligned == False:
			f = randint(0, len(frontier['frontier']) - 1)
			claimRegion(frontier['frontier'][f]['x'], frontier['frontier'][f]['y'], id, claims, regions, totalClaims, frontier)
			
	return claims
	

	
	
	
