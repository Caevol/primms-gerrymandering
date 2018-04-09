from mapMaker import getEuclideanDistance
from random import randint
from Queue import *

def isFrontier(x, y, claims, id):
	if x < 0 or x > len(claims[0]) - 1 or y < 0 or y > len(claims) - 1:
		return False

	if claims[y][x] == id:
		return False
	
	if y < len(claims) - 1 and claims[y+1][x] == id:
		return True
	if x < len(claims[0]) - 1 and claims[y][x + 1] == id:
		return True
	if y > 0 and claims[y-1][x] == id:
		return True
	if x > 0 and claims[y][x-1] == id:
		return True
	else:
		return False
		
# cede territory
def cedeTerritory(regions, claims, centers, MIN_REGIONS):
	sizeY = len(claims)
	sizeX = len(claims[0]) 
	scores = {}
	
	for center in centers:
		scores[center['id']] = 0
	
	for y in claims:
		for x in y:
			scores[x] += 1
			
	print MIN_REGIONS
						
	while min(scores.iteritems(), key = lambda k: k[1])[1] < MIN_REGIONS:
		minId = min(scores.iteritems(), key = lambda k : k[1])[0]
		frontier = []
		
		#print minId, scores[minId], scores

		for y in xrange(sizeY):
			for x in xrange(sizeX):
				if isFrontier(x, y, claims, minId):
					frontier.append({'x':x, 'y':y})
		

		while scores[minId] < MIN_REGIONS and len(frontier) > 0:
			#print scores[minId]
			
			frontier = sorted(frontier, key = lambda g: scores[claims[g['y']][g['x']]])
			frontier = [f for f in frontier if claims[f['y']][f['x']] != minId]
			
			i = 0
			while claims[frontier[i]['y']][frontier[i]['x']] != claims[frontier[-1]['y']][frontier[-1]['x']]:
				i += 1
		
			rnd = randint(i, len(frontier) - 1)
			pos = frontier[rnd]
			del frontier[rnd]
		
			
			
			posX = pos['x']
			posY = pos['y']
						
			scores[claims[posY][posX]] -= 1
			claims[posY][posX] = minId
			
			scores[minId] += 1
			
			if isFrontier(posX + 1, posY, claims, minId):
				frontier.append({'x':posX + 1, 'y':posY})
				
			if isFrontier(posX - 1, posY, claims, minId):
				frontier.append({'x':posX - 1, 'y':posY})
				
			if isFrontier(posX, posY + 1, claims, minId):
				frontier.append({'x':posX, 'y':posY + 1})
				
			if isFrontier(posX, posY - 1, claims, minId):
				frontier.append({'x':posX, 'y':posY - 1})
			
	print MIN_REGIONS, scores

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
	
	#cedeTerritory(regions, claims, centers, int(float(len(regions) * len(regions[0])) / len(centers)) - 150)
	return claims


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
	MIN_REGIONS = int(float(len(regions) * len(regions[0])) / len(centers)) - 150
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
	
	
	#cedeTerritory(regions, claims, centers, MIN_REGIONS)
	return claims
	

	
	
	
